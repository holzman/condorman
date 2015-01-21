#!/usr/bin/python

import psycopg2
import subprocess
import popen2
import sys
import datetime
import pytz
import re
import string
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
import settings_local

password = settings_local.passwords['default']
frontend_host = settings_local.frontend_host
logfile = settings_local.logfile

from util import runCommand

userprio_bin = '/usr/bin/condor_userprio -pool 127.0.0.1'

class condorman:
    cursor = ''
    conn = ''
    condor_usermap = {}
    debug = False
    default_prio = 100000.0

    def __init__(self):
        self.conn = psycopg2.connect("dbname='condorman' user='condoradmin' "
                                "host='%s' password='%s' " % (frontend_host, password))
        self.cursor = self.conn.cursor()
        self.logfile = logfile

        logging.basicConfig(filename=self.logfile, level=logging.DEBUG,
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    def log(self, msg):
        n = datetime.datetime.now()
        print '%s - %s' (n.ctime, msg)
    
    def _get_info_from_condor(self):
        if self.condor_usermap:
            return self.condor_usermap
        
        if self.debug:
            o = open('/tmp/z')
        else:
            (o, e)  = runCommand('%s -allusers -all' % userprio_bin)
            stderr = e.readlines()
            if stderr: logging.error(stderr)
        skip = True

        # strip header and trailer, it looks like
        # headerheaderheader
        # ----------
        # user1
        # user2
        # ----------
        # trailertrailertrailer

        for line in o.readlines():
            if line.startswith('--'):
                skip = not skip
                continue

            if not skip:
                splitline = line.strip().split()

                user = splitline[0]
                factor = splitline[3]
                if '@' not in user: continue # no groups in list
                if user.startswith('group'): continue  # no group quotas in list
                if user.startswith('nice-user'): continue  # no condor niced users in list
                self.condor_usermap[user] = float(factor)

        return self.condor_usermap

    def get_users_from_condor(self):
        ''' Return a set of users from the Condor negotiator'''
        return set(self._get_info_from_condor().keys())
    def get_factors_from_condor(self):
        ''' Return a dictionary {user: priofactor} from the Condor negotiator'''
        return self._get_info_from_condor()

    def get_users_from_db(self):
        ''' Return a list of Condor users from the django DB '''
        self.cursor.execute("select username from condorman_condoruser;")
        rows = self.cursor.fetchall()

        users_in_db = [x[0] for x in rows]
        return users_in_db

    def get_admin_users_from_db(self):
        ''' Return a list of Condor users with isAdmin set in the django DB '''
        self.cursor.execute('select username from condorman_condoruser WHERE '
                            '"isAdmin" = True;')
        rows = self.cursor.fetchall()
        users_in_db = [x[0] for x in rows]
        return users_in_db

    def get_factors_from_db(self, drop_invalid=True):
        ''' Return a dictionary {user: factor} of Condor users from the Django DB '''
        self.cursor.execute("SELECT condorman_condoruser.username,factor,start_date,end_date FROM "
                            "condorman_priofactor, condorman_condoruser "
                            "WHERE condorman_condoruser.id = condorman_priofactor.user_id;")
        rows = self.cursor.fetchall()
        priotable = {}
        # django is timezone-aware.  That's ok!
        central = pytz.timezone("US/Central")
        now = central.localize(datetime.datetime.now())
        for row in rows:
            (username, factor, start_date, end_date) = row
            if now < end_date and now > start_date:
                priotable[username] = float(factor)
        return priotable
        return rows

    def update_users(self):
        ''' Compare lists of Condor users from Condor and the Django DB.
        Add any missing entries to Django. '''
        
        users = self.get_users_from_condor()
        users_in_db = self.get_users_from_db()
        statement = ''
        for user in users.difference(users_in_db):
            statement += '''insert into condorman_condoruser (username, "isAdmin") VALUES ('%s', False);''' % user

        if statement:
            self.cursor.execute(statement)
            self.conn.commit()

    def adjust_condor_prio(self):
        ''' Modify the Condor priority factors based on entries in the Django DB
        (Also reset to default any that are expired or not listed in Django). '''
     
        dbmap = self.get_factors_from_db()
        condormap = self._get_info_from_condor()
        adminList = self.get_admin_users_from_db()

        for k in condormap:
            if k in adminList:
                continue
            condorfactor = condormap[k]
            dbfactor = dbmap.get(k, self.default_prio)

            if condorfactor != dbfactor:
                k = self.sanitize(k, str)
                dbfactor = self.sanitize(dbfactor, float)
                logging.info('Adjusting user %s to %s' % (k, dbfactor))
                (o, e)  = runCommand('%s -setfactor %s %s' % (userprio_bin, k, dbfactor))
                stderr = e.readlines()
                if stderr: logging.error(stderr)

    def sanitize(self, item, type):
        ''' Sanitize input which are arguments for a shell command '''
        if type == float:
            try:
                item = float(item)
            except  ValueError:
                item = 0.0

        if type == str:  # only valid chars for usernames...x
            allowed = set(string.ascii_lowercase + string.digits + "." + "_" + "-" + "@" + "-")
            if not (set(item) <= allowed):
                item = ''

        return item

if __name__ == '__main__':
    c = condorman()
    logging.debug("Beginning Condorman invocation")
    c.debug = False
    c.update_users()
    c.adjust_condor_prio()
    logging.debug("Ending Condorman invocation")

