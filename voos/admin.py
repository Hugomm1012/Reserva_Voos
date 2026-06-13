from django.contrib import admin
from .models import Companhia, Aeroporto, Voo, Passageiro, Reserva

@admin.register(Companhia)
class CompanhiaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Aeroporto)
class AeroportoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'cidade', 'pais')
    search_fields = ('codigo', 'cidade')
    list_filter = ('pais',)

@admin.register(Voo)
class VooAdmin(admin.ModelAdmin):
    list_display = ('numero', 'companhia', 'origem', 'destino', 'data_partida', 'preco')
    list_filter = ('companhia', 'data_partida')
    search_fields = ('numero',)
    readonly_fields = ()

@admin.register(Passageiro)
class PassageiroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'documento', 'data_criacao')
    search_fields = ('nome', 'email', 'documento')
    list_filter = ('data_criacao',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('passageiro', 'voo', 'status', 'data_reserva')
    list_filter = ('status', 'data_reserva')
    search_fields = ('passageiro__nome', 'voo__numero')
    readonly_fields = ('data_reserva',)