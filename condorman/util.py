from condorman.models import CondorUser

def getUserList():
    return CondorUser.objects.filter(isAdmin__exact=False)
