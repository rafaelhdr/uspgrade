from django.contrib import admin
from uspgrade.models import Sugestao, Usuario, Comentario, Resposta, Voto

class SugestaoAdmin(admin.ModelAdmin):
    pass

class UsuarioAdmin(admin.ModelAdmin):
    pass

admin.site.register(Sugestao, SugestaoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Comentario)
admin.site.register(Resposta)
admin.site.register(Voto)
