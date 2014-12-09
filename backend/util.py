#!/usr/bin/python

import popen2
import cStringIO
import fcntl
import os
import time
import select

def runCommand(cmd):
    child = popen2.Popen3(cmd, capturestderr=True)

    stdout = child.fromchild
    stderr = child.childerr

    outfd = stdout.fileno()
    errfd = stderr.fileno()

    outeof = erreof = 0
    outdata = cStringIO.StringIO()
    errdata = cStringIO.StringIO()

    fdlist = [outfd, errfd]
    for fd in fdlist: # make stdout/stderr nonblocking
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    while fdlist:
        time.sleep(.001) # prevent 100% CPU spin 
        ready = select.select(fdlist, [], [])
        if outfd in ready[0]:
            outchunk = os.read(outfd, 4096)
            if outchunk == '':
                fdlist.remove(outfd)
            else:
                outdata.write(outchunk)
        if errfd in ready[0]:
            errchunk = os.read(errfd, 4096)
            if errchunk == '':
                fdlist.remove(errfd)
            else:
                errdata.write(errchunk)

    exitStatus = child.wait()
    outdata.seek(0)
    errdata.seek(0)

    return outdata, errdata
