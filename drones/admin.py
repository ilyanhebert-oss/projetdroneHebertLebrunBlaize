from django.contrib import admin
from .models import Utilisateur, Drone, Mission, Alerte, RapportAudit, EcartInventaire

admin.site.register(Utilisateur)
admin.site.register(Drone)
admin.site.register(Mission)
admin.site.register(Alerte)
admin.site.register(RapportAudit)
admin.site.register(EcartInventaire)
