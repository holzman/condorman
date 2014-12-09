from condorman.models import CondorUser, PrioFactor
from django.contrib import admin
import reversion.admin

class CondorUserAdmin(reversion.admin.VersionAdmin):
    model = CondorUser
    pass

class PrioFactorAdmin(reversion.admin.VersionAdmin):
    model = PrioFactor
    pass
#    list_display = ('username', 'isAdmin')

admin.site.register(CondorUser, CondorUserAdmin)
admin.site.register(PrioFactor, PrioFactorAdmin)


