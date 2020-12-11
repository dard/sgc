from django.forms import *
from SGCapp.models import *
from datetime import datetime


class ClienteForm (ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cliente
        fields = '__all__'
        # permite widgets personalizar
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un Nombre',
                }
            ),
            'apellido': TextInput(
                attrs={
                    'placeholder': 'Ingrese un Apellido',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nº de dni',
                }
            ),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nº de telefono',
                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder': 'Ingrese un Email',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese una direccón',
                }
            ),

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CobradorForm (ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cobrador
        fields = '__all__'
        # permite widgets personalizar
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un Nombre',
                }
            ),
            'apellido': TextInput(
                attrs={
                    'placeholder': 'Ingrese un Apellido',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nº de dni',
                }
            ),
            'telefono': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nº de telefono',
                }
            ),
            'email': TextInput(
                attrs={
                    'placeholder': 'Ingrese un Email',
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese una direccón',
                }
            ),

        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# BANCO form


class BancoForm (ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Banco
        fields = '__all__'
        # permite widgets personalizar
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un Nombre',
                }
            ),
        }
        exclude = ['user_creation', 'user_update']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

# Formulario Cheque


class ChequeForm (ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['cheque_banco'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cheque
        fields = '__all__'
        # permite widgets personalizar
        widgets = {
            'Numero cheque': TextInput(
                attrs={
                    'placeholder': 'Ingrese numero de cheque',
                }
            ),
            'monto': TextInput(
                attrs={
                    'placeholder': 'Ingrese el monto del cheque',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

# formulario Comprobante


class ComprobanteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['comprobante_cliente'].widget.attrs['autofocus'] = True

    class Meta:
        model = Comprobante
        fields = '__all__'
        # permite widgets personalizar
        widgets = {
            'monto_original': TextInput(
                attrs={
                    'placeholder': 'Ingrese el monto del comprobante',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# formulario Recibo


class ReciboFacturaForm (ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['recibo_cliente'].widget.attrs['autofocus'] = True
        self.fields['recibo_cliente'].widget.attrs['class'] = 'form-control select2'
        self.fields['recibo_cliente'].widget.attrs['style'] = 'width: 100%'
        self.fields['recibo_planilla'].widget.attrs['autofocus'] = False
        self.fields['recibo_planilla'].widget.attrs['class'] = 'form-control select2'
        self.fields['recibo_planilla'].widget.attrs['style'] = 'width: 100%'
        self.fields['recibo_caja'].widget.attrs['autofocus'] = False
        self.fields['recibo_caja'].widget.attrs['class'] = 'form-control select2'
        self.fields['recibo_caja'].widget.attrs['style'] = 'width: 100%'
        self.fields['comprobantes'].widget.attrs['autofocus'] = False
        self.fields['comprobantes'].widget.attrs['class'] = 'form-control select2'
        self.fields['comprobantes'].widget.attrs['style'] = 'width: 100%'
        self.fields['cheque'].widget.attrs['autofocus'] = False
        self.fields['cheque'].widget.attrs['class'] = 'form-control select2'
        self.fields['cheque'].widget.attrs['style'] = 'width: 100%'
        self.fields['estado'].widget.attrs['autofocus'] = False
        self.fields['estado'].widget.attrs['class'] = 'form-control select2'
        self.fields['estado'].widget.attrs['style'] = 'width: 100%'

    class Meta:
        model = Recibo
        fields = '__all__'
        # permite widgets personalizar
        widgets = {
            'fecha': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'fecha',
                    'data-target': '#fecha',
                    'data-toggle': 'datetimepicker'
                }),
            'subtotalComp': TextInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control select2',
                }),
            'subtotalCheq': TextInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control select2',
                }),
            'efectivo': TextInput(
                attrs={
                    'class': 'form-control select2',
                }),
            'total': TextInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control select2',
                }),
        }


# formulario Recibo


class ReciboForm (ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['recibo_cliente'].widget.attrs['autofocus'] = True
        self.fields['recibo_planilla'].widget.attrs['autofocus'] = False
        self.fields['recibo_caja'].widget.attrs['autofocus'] = False
        self.fields['comprobantes'].widget.attrs['autofocus'] = False
        self.fields['cheque'].widget.attrs['autofocus'] = False
        self.fields['estado'].widget.attrs['autofocus'] = False

    class Meta:
        model = Recibo
        fields = '__all__'
        # permite widgets personalizar
        widgets = {
            'total': TextInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control',
                }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# formulario Caja---------------
class CajaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['user_caja'].widget.attrs['autofocus'] = True
        self.fields['estado'].widget.attrs['autofocus'] = False

    class Meta:
        model = Caja
        fields = '__all__'
        # permite widgets personalizar
        widgets = {
            'saldo_inicial': TextInput(
                attrs={
                    'placeholder': 'Ingrese el saldo inicial',
                }
            ),
            'monto_cierre': TextInput(
                attrs={
                    'placeholder': 'Ingrese el saldo de cierre',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


# formulario Planilla---------------
class PlanillaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['planilla_caja'].widget.attrs['autofocus'] = True
        self.fields['planilla_cobrador'].widget.attrs['autofocus'] = False
        self.fields['estado'].widget.attrs['autofocus'] = False

    class Meta:
        model = Planilla
        fields = '__all__'
        # permite widgets personalizar
        widgets = {
            'monto_total': TextInput(
                attrs={
                    'placeholder': 'Ingrese el monto',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                # if self.fields['estado'] == 'C':
                #     self.fecha_cierre.strftime('%y-%m-%d')
                # else:
                #     self.fecha_cierre = None
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
