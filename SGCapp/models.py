from datetime import datetime
from django.db import models
from django.forms import model_to_dict
from SGC.settings import MEDIA_URL, STATIC_URL
from django.conf import settings
from crum import get_current_user
from SGCuser.models import BaseModel
# Create your models here.


class Caja(models.Model):
    ESTADO_ABIERTO = 'A'
    ESTADO_CERRADO = 'C'

    ESTADO_OPCIONES = (
        (ESTADO_ABIERTO, 'Abierta'),
        (ESTADO_CERRADO, 'Cerrada')
    )

    user_caja = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                                  verbose_name='usuario caja', related_name='User_caja')
    estado = models.CharField(max_length=1, choices=ESTADO_OPCIONES)
    fecha_cierre = models.DateField(auto_now=True, verbose_name='Fecha cierre')
    saldo_inicial = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name='Saldo inicial')
    monto_cierre = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Monto cierre')

    def toJSON(self):
        item = model_to_dict(self)
        if item['estado'] == 'C':
            item['fecha_cierre'] = self.fecha_cierre.strftime('%y-%m-%d')
        else:
            item['fecha_cierre'] = None
        return item

    def __str__(self):
        return '{} {} {} {} {}'.format(self.user_caja, self.estado, self.fecha_cierre, self.saldo_inicial, self.monto_cierre)

    class Meta:
        ordering = ['id']


class Cliente (models.Model):

    nombre = models.CharField(max_length=25, null=True, blank=True, verbose_name='Nombre')
    apellido = models.CharField(max_length=25, null=True, blank=True, verbose_name='Apellido')
    dni = models.IntegerField(unique=True, verbose_name='Dni')
    telefono = models.IntegerField(verbose_name='Telefono')
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=40, null=True, blank=True, verbose_name='Dirección')
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.nombre, self.apellido, self.dni, self.telefono, self.email,  self.creado)

    def toJSON(self):
        item = model_to_dict(self, exclude=['creado', 'actualizado'])
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Cobrador (models.Model):
    #    user = models.ForeignKey(User, on_delete=models.CASCADE,
    #                             null=True, related_name='userCobrador')
    nombre = models.CharField(max_length=25, null=True, blank=True, verbose_name='Nombre')
    apellido = models.CharField(max_length=25, null=True, blank=True, verbose_name='Apellido')
    dni = models.IntegerField(unique=True, verbose_name='Dni')
    telefono = models.IntegerField(verbose_name='Telefono', null=True)
    direccion = models.CharField(max_length=40, null=True,
                                 blank=True, verbose_name='Dirección')
    email = models.EmailField(blank=True, null=True)
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateField(auto_now=True)

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.nombre, self.apellido, self.dni, self.telefono, self.email,  self.creado)

    def toJSON(self):
        item = model_to_dict(self, exclude=['creado', 'actualizado'])
        return item

    class Meta:
        verbose_name = 'Cobrador'
        verbose_name_plural = 'Cobradores'
        ordering = ['id']


class Planilla (models.Model):
    ESTADO_ABIERTO = 'A'
    ESTADO_CERRADO = 'C'

    ESTADO_OPCIONES = (
        (ESTADO_ABIERTO, 'Abierta'),
        (ESTADO_CERRADO, 'Cerrada')
    )
    planilla_caja = models.ForeignKey(Caja, on_delete=models.CASCADE, verbose_name='Caja')
    planilla_cobrador = models.ForeignKey(
        Cobrador, on_delete=models.CASCADE, verbose_name='Cobrador id')
    estado = models.CharField(max_length=1, choices=ESTADO_OPCIONES)
    fecha_emision = models.DateField(auto_now_add=True, null=True, verbose_name='Fecha emision')
    fecha_cierre = models.DateField(auto_now=True, blank=True, null=True)
    monto_total = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Monto Total')

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha_emision'] = self.fecha_emision.strftime('%y-%m-%d')
        if item['estado'] == 'C':
            item['fecha_cierre'] = self.fecha_cierre.strftime('%y-%m-%d')
        else:
            item['fecha_cierre'] = None
        return item

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.planilla_caja, self.planilla_cobrador, self.fecha_emision, self.fecha_cierre, self.monto_total, self.estado)

    class Meta:
        verbose_name = 'Planilla'
        verbose_name_plural = 'Planillas'
        ordering = ['id']


class Banco(BaseModel):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')

    def __str__(self):
        return '{}'.format(self.nombre)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    # audito quien hace cambios en el modelo
    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     user = get_current_user()
    #     if user is not None:
    #         if not self.pk:
    #             self.user_creation = user
    #         else:
    #             self.user_update = user
    #
    #     super(Banco, self).save()

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        ordering = ['id']


class Cheque(models.Model):
    cheque_banco = models.ForeignKey(
        Banco, on_delete=models.CASCADE, verbose_name='Banco')
    fecha = models.DateField(auto_now_add=True, verbose_name='Fecha')
    # cheque_recibo = models.ForeignKey(
    #     Recibo, on_delete=models.CASCADE, verbose_name='Recibo', null=True, blank=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Monto')
    imagen = models.ImageField(upload_to='cheque/%Y/%m/%d', null=True, blank=True)

    def get_imagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        else:
            return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha'] = self.fecha.strftime('%y-%m-%d')
        item['cheque_banco'] = self.cheque_banco.toJSON()
        item['monto'] = format(self.monto, '.2f')
        item['imagen'] = self.get_imagen()  # Parseo el campo imagen
        return item

    def __str__(self):
        return '{} {} {} {}'.format(self.cheque_banco, self.fecha, self.monto, self.imagen)

    class Meta:
        verbose_name = 'Cheque'
        verbose_name_plural = 'Cheques'
        ordering = ['id']


class Comprobante (models.Model):
    comprobante_cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    fecha_comprobante = models.DateField(auto_now_add=True, verbose_name='Fecha')
    monto = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Monto')

    class Meta:
        ordering = ['id']

    def toJSON(self):
        # model_to_dict devuelve un diccionario del modelo
        # propiedad exclude para excluir datos (self, exclude=['campoFecha']
        item = model_to_dict(self)
        # parseo el campo fecha
        item['fecha_comprobante'] = self.fecha_comprobante.strftime('%y-%m-%d')
        item['monto'] = format(self.monto, '.2f')
        return item

    def __str__(self):
        return '{} {} {}'.format(self.comprobante_cliente, self.fecha_comprobante, self.monto)


class Recibo(models.Model):
    ESTADO_ABIERTO = 'A'
    ESTADO_CERRADO = 'C'

    ESTADO_OPCIONES = (
        (ESTADO_ABIERTO, 'Abierta'),
        (ESTADO_CERRADO, 'Cerrada')
    )
    fecha = models.DateField(default=datetime.now, verbose_name='Fecha')
    recibo_cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Cliente DNI')
    recibo_planilla = models.ForeignKey(
        Planilla, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Planilla')
    recibo_caja = models.ForeignKey(Caja, on_delete=models.CASCADE,
                                    null=True, blank=True, verbose_name='Caja')
    estado = models.CharField(max_length=1, choices=ESTADO_OPCIONES)
    comprobantes = models.ForeignKey(
        Comprobante, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name='Comprobantes')
    cheque = models.ForeignKey(Cheque, on_delete=models.CASCADE, null=True,
                               blank=True, verbose_name='Cheque')
    efectivo = models.DecimalField(default=0.0, max_digits=8,
                                   decimal_places=2, verbose_name='Efectivo')
    subtotalComp = models.DecimalField(default=0.0, max_digits=8,
                                       decimal_places=2, verbose_name='Subtotal Comprobantes')
    subtotalCheq = models.DecimalField(default=0.0, max_digits=8,
                                       decimal_places=2, verbose_name='Subtotal Cheques')
    total = models.DecimalField(default=0.00, max_digits=8, decimal_places=2, verbose_name='Total')

    def toJSON(self):
        item = model_to_dict(self, exclude=['comprobantes', 'cheque'])
        item['recibo_cliente'] = self.recibo_cliente.toJSON()
        item['subtotalComp'] = format(self.subtotalComp, '.2f')
        item['subtotalCheq'] = format(self.subtotalCheq, '.2f')
        if item['estado'] == 'C':
            item['fecha'] = self.fecha.strftime('%y-%m-%d')
        else:
            item['fecha'] = None
        return item

    def __str__(self):
        return '{} {} {} {} {} {} {} {} {} {} {} {}'.format(self.recibo_caja,
                                                            self.fecha,
                                                            self.recibo_cliente,
                                                            self.efectivo,
                                                            self.comprobantes,
                                                            self.subtotalComp,
                                                            self.cheque,
                                                            self.subtotalCheq,
                                                            self.total,
                                                            self.estado,
                                                            self.comprobantes,
                                                            self.cheque)

    class Meta:
        verbose_name = 'Recibo'
        verbose_name_plural = 'Recibos'
        ordering = ['id']
