from django.contrib import admin
from SGCapp.models import *

# Register your models here.


class CobradorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'dni', 'telefono',
                    'email', 'direccion', 'creado', 'actualizado')
    search_fields = ('dni',)
    list_filter = ('id',)
    date_hierarchy = 'creado'


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'dni', 'telefono',
                    'email', 'direccion', 'creado', 'actualizado')
    search_fields = ('dni',)
    list_filter = ('id',)
    date_hierarchy = 'creado'


# @admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_caja', 'estado', 'fecha_cierre',
                    'saldo_inicial', 'monto_cierre')

# @admin.register(Planilla)


class PlanillaAdmin(admin.ModelAdmin):
    list_display = ('id', 'planilla_caja', 'planilla_cobrador',
                    'fecha_emision', 'fecha_cierre',
                    'monto_total', 'estado')
    search_fields = ('planilla_caja', 'planilla_cobrador')
    list_filter = ('estado',)
    date_hierarchy = 'fecha_emision'

# @admin.register(Comprobante)


class ComprobanteAdmin(admin.ModelAdmin):
    list_display = ('id', 'comprobante_cliente', 'fecha_comprobante',
                    'monto')
    search_fields = ('monto', 'comprobante_cliente')
    date_hierarchy = 'fecha_comprobante'

# @admin.register(Recibo)


class ReciboAdmin(admin.ModelAdmin):
    list_display = ('id', 'recibo_planilla', 'recibo_caja', 'efectivo',
                    'subtotalComp', 'subtotalCheq', 'total', 'fecha',
                    'estado', 'comprobantes', 'cheque')
    search_fields = ('total',)
    list_filter = ('estado',)
    date_hierarchy = 'fecha'


# @admin.register(Banco)


class BancoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre',)
    search_fields = ('nombre',)
    list_filter = ('id',)

# @admin.register(Cheque)


class ChequeAdmin(admin.ModelAdmin):
    list_display = ('id', 'cheque_banco', 'fecha', 'monto', 'imagen')
    search_fields = ('monto', 'id', 'fecha')
    list_filter = ('id', 'monto', 'fecha')


admin.site.register(Cobrador, CobradorAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Planilla, PlanillaAdmin)
admin.site.register(Caja, CajaAdmin)
admin.site.register(Comprobante, ComprobanteAdmin)
admin.site.register(Recibo, ReciboAdmin)
admin.site.register(Banco, BancoAdmin)
admin.site.register(Cheque, ChequeAdmin)
