from django.contrib import admin
from uspgrade.models import Sugestao, Usuario

class SugestaoAdmin(admin.ModelAdmin):
    pass

class UsuarioAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sugestao, SugestaoAdmin)
admin.site.register(Usuario, UsuarioAdmin)