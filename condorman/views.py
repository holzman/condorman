# Create your views here.
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from condorman.models import CondorUser, PrioFactor, LogAction
from condorman.forms import PrioFactorForm
from condorman.util import getUserList
from django.http import HttpResponse, HttpResponseRedirect
import md5
from datetime import datetime
from condorman.admin import PrioFactorAdmin

# to do: build backend to auth users based on REMOTE_USER
#   build unauth pages

def log(request):
    logtable = LogAction.objects.all()
    return HttpResponse(logtable)

def test(request):
    userList = getUserList()
    user = request.META['REMOTE_USER']
    return render_to_response('condorman/testindex.html', {'userList': userList, 'remote_user': user,
                                                       'userHash':  md5.new(user).hexdigest()[0:30],
                                                       'can_add': request.user.has_perm('condorman.add_priofactor'),
                                                       'can_del': request.user.has_perm('condorman.delete_priofactor')})
    
def index(request):
    userList = getUserList()
    user = request.META['REMOTE_USER']
    return render_to_response('condorman/index.html', {'userList': userList, 'remote_user': user,
                                                       'userHash':  md5.new(user).hexdigest()[0:30],
                                                       'can_add': request.user.has_perm('condorman.add_priofactor'),
                                                       'can_del': request.user.has_perm('condorman.delete_priofactor')})

def add(request):
    if not request.user.has_perm('condorman.add_priofactor'):
        return HttpResponseRedirect(reverse('condorman.views.index'))

    userList = getUserList()
    a = PrioFactorForm()
    return render_to_response('condorman/add.html',
                              {'form': a, 'userList': userList},
                              )

def log_this(authuser, action):
    l = LogAction(authuser=authuser, action=action, action_date=datetime.now())
    l.save()
    
def process(request):
    if request.method == 'POST' and request.POST.keys():
        if request.POST.has_key('remove'):
            if not request.user.has_perm('condorman.delete_priofactor'):
                return HttpResponseRedirect(reverse('condorman.views.index'))
            for item in request.POST.getlist('remove'):
                pf = PrioFactor.objects.get(id=item)
                pf.delete()

        else:
            # add lines
            if not request.user.has_perm('condorman.add_priofactor'):
                return HttpResponseRedirect(reverse('condorman.views.index'))
            form = PrioFactorForm(request.POST)
            if not form.is_valid():
                userList = getUserList()
                return render_to_response('condorman/add.html',
                                          {'form': form,
                                           'userList': userList},
                                          context_instance=RequestContext(request)
                                          )
            else:
                data = form.cleaned_data
                p =  PrioFactor(user=data.get('user'),
                                factor=data.get('factor'),
                                start_date=data.get('start_date'),
                                end_date= data.get('end_date'))
                
                p.save()
                log_this(request.user, 'add')

    return HttpResponseRedirect(reverse('condorman.views.index'))
