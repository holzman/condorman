from django.contrib.auth.backends import RemoteUserBackend
import md5
class MyBackend(RemoteUserBackend):
    create_unknown_user = True

    def clean_username(self, username):
        return md5.new(username).hexdigest()[0:30]
    
