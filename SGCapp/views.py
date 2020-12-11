import json

from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.utils.decorators import method_decorator
from SGCapp.models import Cliente, Cobrador, Banco, Cheque, Comprobante, Recibo, Caja, Planilla
from SGCuser.models import User
from SGCapp.forms import ClienteForm, CobradorForm, BancoForm, ChequeForm, ComprobanteForm, CajaForm, PlanillaForm, ReciboFacturaForm, ReciboForm

# Create your views here.


class dashboardView(TemplateView):
    template_name = 'SGCapp/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administración'

        return context


# vista basada en funcion


def clientes_list(request):
    data = {
        'title': 'Listado de Clientes-vista basada en funcion',
        'clientes': Cliente.objects.all()
    }
    return render(request, 'SGCapp/clientes/list.html', data)

# vista basada en Clase - con el decorador (login_required) valido que el
# usuario este logueado para ver la vista


class ClienteListView(ListView):
    model = Cliente
    template_name = 'SGCapp/clientes/list.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        # data = Cliente.objects.get(pk=request.POST['id']).toJSON
        # return JsonResponse(data)
        # el siguiente codigo es para renderizar con ayax cuando son miles de
        # filas en la tabla se utiliza con el list.js y el toJson
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Cliente.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Litado de Clientes'
        context['create_url'] = reverse_lazy('SGCapp:ClienteCreateView')
        context['list_url'] = reverse_lazy('SGCapp:ClienteListView')
        context['entity'] = 'Clientes'
        return context


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'SGCapp/clientes/create.html'
    success_url = reverse_lazy('SGCapp:ClienteListView')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

        #  print(request.POST)
        #  form = ClienteForm(request.POST)
        #  if form.is_valid():
        #      form.save()
        #      return HttpResponseRedirect(self.success_url)
        #  self.object = None
        #  context = self.get_context_data(**kwargs)
        #  context['form'] = form
        #  return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = reverse_lazy('SGCapp:ClienteListView')
        context['action'] = 'add'
        return context


class ClienteUpdateView(UpdateView):

    model = Cliente
    form_class = ClienteForm
    template_name = 'SGCapp/clientes/create.html'
    success_url = reverse_lazy('SGCapp:ClienteListView')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post')
        print(request.POST)
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        print(self.get_object())
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = reverse_lazy('SGCapp:ClienteListView')
        context['action'] = 'edit'
        return context


class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'SGCapp/clientes/delete.html'
    success_url = reverse_lazy('SGCapp:ClienteListView')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post')
        print(request.POST)
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

        print(request.POST)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        print(self.success_url)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar cliente'
        context['entity'] = 'Cliente'
        context['list_url'] = self.success_url
        return context


# vista form Cliente
class ClienteFormView(FormView):
    form_class = ClienteForm
    template_name = 'SGCapp/clientes/create.html'
    success_url = reverse_lazy('SGCapp:ClienteListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formulario cliente'
        context['entity'] = 'Cliente'
        context['list_url'] = self.success_url
        return context

# vistas Cobrador


class CobradorListView(ListView):

    model = Cobrador
    template_name = 'SGCapp/cobradores/list.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post')
        print(request.POST)
        # data = Cobrador.objects.get(pk=request.POST['id']).toJSON
        # return JsonResponse(data)
        # el siguiente codigo es para renderizar con ayax cuando son miles de
        # registros en la tabla
        # se utiliza con el list.js y el toJson
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Cobrador.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cobradores'
        context['create_url'] = reverse_lazy('SGCapp:CobradorCreateView')
        context['list_url'] = reverse_lazy('SGCapp:CobradorListView')
        context['entity'] = 'Cobradores'
        print(reverse_lazy('SGCapp:CobradorListView'))
        return context


class CobradorCreateView(CreateView):
    model = Cobrador
    form_class = CobradorForm
    template_name = 'SGCapp/cobradores/create.html'
    success_url = reverse_lazy('SGCapp:CobradorListView')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(request.POST)
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear cobrador'
        context['entity'] = 'Cobradores'
        context['list_url'] = reverse_lazy('SGCapp:CobradorListView')
        context['action'] = 'add'
        return context


class CobradorUpdateView(UpdateView):

    model = Cobrador
    form_class = CobradorForm
    template_name = 'SGCapp/cobradores/create.html'
    success_url = reverse_lazy('SGCapp:CobradorListView')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post')
        print(request.POST)
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        print(self.get_object())
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar cobrador'
        context['entity'] = 'Cobradores'
        context['list_url'] = reverse_lazy('SGCapp:CobradorListView')
        context['action'] = 'edit'
        return context


class CobradorDeleteView(DeleteView):
    model = Cobrador
    template_name = 'SGCapp/cobradores/delete.html'
    success_url = reverse_lazy('SGCapp:CobradorListView')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

        print(request.POST)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar cobrador'
        context['entity'] = 'Cobrador'
        context['list_url'] = self.success_url
        return context


# VISTAS BANCO ------------------------------------


class BancoListView (ListView):
    model = Banco
    template_name = 'SGCapp/bancos/list.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post')
        print(request.POST)

        try:
            action = request.POST['action']
            if action == 'searchdata':
                print(request.POST)
                data = []
                for i in Banco.objects.all():
                    print('data')
                    print(data)
                    print('i')
                    print(i)
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Bancos'
        context['create_url'] = reverse_lazy('SGCapp:BancoCreateView')
        context['list_url'] = reverse_lazy('SGCapp:BancoListView')
        context['entity'] = 'Bancos'
        print(reverse_lazy('SGCapp:BancoListView'))
        return context

# vista form Banco -------------------


class BancoFormView(FormView):
    form_class = BancoForm
    template_name = 'SGCapp/bancos/create.html'
    success_url = reverse_lazy('SGCapp:BancoListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formulario banco'
        context['entity'] = 'Bancos'
        context['list_url'] = self.success_url
        return context


class BancoCreateView(CreateView):
    model = Banco
    form_class = BancoForm
    template_name = 'SGCapp/bancos/create.html'
    success_url = reverse_lazy('SGCapp:BancoListView')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(request.POST)
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear banco'
        context['entity'] = 'Bancos'
        context['list_url'] = reverse_lazy('SGCapp:BancoListView')
        context['action'] = 'add'
        return context


class BancoUpdateView(UpdateView):

    model = Banco
    form_class = BancoForm
    template_name = 'SGCapp/bancos/create.html'
    success_url = reverse_lazy('SGCapp:BancoListView')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post')
        print(request.POST)
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        print(self.get_object())
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar bancos'
        context['entity'] = 'Bancos'
        context['list_url'] = reverse_lazy('SGCapp:BancoListView')
        context['action'] = 'edit'
        return context


class BancoDeleteView(DeleteView):
    model = Banco
    template_name = 'SGCapp/bancos/delete.html'
    success_url = reverse_lazy('SGCapp:BancoListView')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

        print(request.POST)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar banco'
        context['entity'] = 'Bancos'
        context['list_url'] = self.success_url
        return context


#  VISTAS Cheques --------------------------------


class ChequeListView (ListView):
    model = Cheque
    template_name = 'SGCapp/cheques/list.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post')
        print(request.POST)
        # print(request.FILE)

        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Cheque.objects.all()[:]:
                    # print(i)
                    # print(data)
                    cheque = i.toJSON()
                    # asigno el nombre del campo en el diccionario
                    cheque['cheque_banco'] = i.cheque_banco.nombre
                    print(cheque)
                    data.append(cheque)
                    # data.append(i.toJSON())
                # for i in Cheque.objects.all():
                #     data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cheques'
        context['create_url'] = reverse_lazy('SGCapp:ChequeCreateView')
        context['list_url'] = reverse_lazy('SGCapp:ChequeListView')
        context['entity'] = 'Cheques'
        print(reverse_lazy('SGCapp:ChequeListView'))
        return context

# cheque form


class ChequeFormView(FormView):
    form_class = ChequeForm
    template_name = 'SGCapp/cheques/create.html'
    success_url = reverse_lazy('SGCapp:ChequeListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formulario cheque'
        context['entity'] = 'Cheques'
        context['list_url'] = self.success_url
        return context


class ChequeCreateView(CreateView):
    model = Cheque
    form_class = ChequeForm
    template_name = 'SGCapp/cheques/create.html'
    success_url = reverse_lazy('SGCapp:ChequeListView')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear cheque'
        context['entity'] = 'Cheques'
        context['list_url'] = reverse_lazy('SGCapp:ChequeListView')
        context['action'] = 'add'
        return context


class ChequeUpdateView(UpdateView):

    model = Cheque
    form_class = ChequeForm
    template_name = 'SGCapp/cheques/create.html'
    success_url = reverse_lazy('SGCapp:ChequeListView')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post')
        print(request.POST)
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        print(self.get_object())
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar cheques'
        context['entity'] = 'Cheques'
        context['list_url'] = reverse_lazy('SGCapp:ChequeListView')
        context['action'] = 'edit'
        return context


class ChequeDeleteView(DeleteView):
    model = Cheque
    template_name = 'SGCapp/cheques/delete.html'
    success_url = reverse_lazy('SGCapp:ChequeListView')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

        print(request.POST)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar cheque'
        context['entity'] = 'Cheques'
        context['list_url'] = self.success_url
        return context


#  VISTAS Comprobantes --------------------------------


class ComprobanteListView (ListView):
    model = Comprobante
    template_name = 'SGCapp/comprobantes/list.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        # data = Comprobante.objects.get(pk=request.POST['id']).toJSON
        # return JsonResponse(data)
        # el siguiente codigo es para renderizar con ayax cuando son miles de
        # filas en la tabla se utiliza con el list.js y el toJson
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Comprobante.objects.all()[:]:
                    # print(i)
                    # print(data)
                    comprobante = i.toJSON()
                    # asigno el nombre del campo en el diccionario
                    comprobante['comprobante_cliente'] = i.comprobante_cliente.dni
                    print(comprobante)
                    data.append(comprobante)
                    # data.append(i.toJSON())
                # for i in Cheque.objects.all():
                #     data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Comprobantes'
        context['create_url'] = reverse_lazy('SGCapp:ComprobanteCreateView')
        context['list_url'] = reverse_lazy('SGCapp:ComprobanteListView')
        context['entity'] = 'Comprobantes'
        return context


class ComprobanteCreateView(CreateView):
    model = Comprobante
    form_class = ComprobanteForm
    template_name = 'SGCapp/comprobantes/create.html'
    success_url = reverse_lazy('SGCapp:ComprobanteListView')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear comprobante'
        context['entity'] = 'Comprobantes'
        context['list_url'] = reverse_lazy('SGCapp:ComprobanteListView')
        context['action'] = 'add'
        return context


class ComprobanteUpdateView(UpdateView):

    model = Comprobante
    form_class = ComprobanteForm
    template_name = 'SGCapp/comprobantes/create.html'
    success_url = reverse_lazy('SGCapp:ComprobanteListView')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post')
        print(request.POST)
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        print(self.get_object())
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar comprobante'
        context['entity'] = 'Comprobantes'
        context['list_url'] = reverse_lazy('SGCapp:ComprobanteListView')
        context['action'] = 'edit'
        return context


class ComprobanteDeleteView(DeleteView):
    model = Comprobante
    template_name = 'SGCapp/comprobantes/delete.html'
    success_url = reverse_lazy('SGCapp:ComprobanteListView')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post')
        print(request.POST)
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

        print(request.POST)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        print(self.success_url)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar comprobante'
        context['entity'] = 'Comprobantes'
        context['list_url'] = self.success_url
        return context


# vista form Comprobante
class ComprobanteFormView(FormView):
    form_class = ComprobanteForm
    template_name = 'SGCapp/comprobantes/create.html'
    success_url = reverse_lazy('SGCapp:ComprobanteListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formulario comprobante'
        context['entity'] = 'Comprobantes'
        context['list_url'] = self.success_url
        return context


# VISTAS RECIBO FACTURA------------------------------------------------------
class ReciboFacturaListView(ListView):
    model = Recibo
    template_name = 'SGCapp/recibos_facturas/list.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        # data = Comprobante.objects.get(pk=request.POST['id']).toJSON
        # return JsonResponse(data)
        # el siguiente codigo es para renderizar con ayax cuando son miles de
        # filas en la tabla se utiliza con el list.js y el toJson
        try:
            action = request.POST['action']
            print('1 action')
            print(action)
            if action == 'searchdata':
                print('2 action')
                print(action)
                data = []
                for i in Recibo.objects.all()[:]:
                    print('i')
                    print(i)

                    recibo = i.toJSON()
                # asigno el nombre del campo en el diccionario
                    recibo['recibo_cliente'] = i.recibo_cliente.dni
                    print('recibo')
                    print(recibo)
                    data.append(recibo)
                # detalle del recibo, nc
            elif action == 'search_details_recibo':
                print('3 action')
                print(action)
                data = []
                print('data')
                print(data)
                for i in Recibo.objects.filter(recibo_cliente=request.POST['id']):
                    recibo = i.toJSON()

                    print('++++++')
                    # print(recibo['comprobantes'])
                    print(recibo['subtotalComp'])
                    # print(recibo['cheque'])
                    print(recibo['subtotalCheq'])
                    recibo['comprobantes'] = i.comprobantes
                    recibo['subtotalComp'] = i.subtotalComp
                    recibo['cheque'] = i.cheque
                    recibo['subtotalCheq'] = i.subtotalCheq
                    print('data')
                    print(data)
                    data.append(recibo)
                # for i in Cheque.objects.filter(cheque_banco_id=request.POST['id']):
                #     data.append(i.toJSON())

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Recibos Facturas'
        context['create_url'] = reverse_lazy('SGCapp:ReciboFacturaCreateView')
        context['list_url'] = reverse_lazy('SGCapp:ReciboFacturaListView')
        context['entity'] = 'Recibos'
        return context


class ReciboFacturaCreateView(CreateView):
    model = Recibo
    form_class = ReciboFacturaForm
    template_name = 'SGCapp/recibos_facturas/create.html'
    success_url = reverse_lazy('SGCapp:ReciboFacturaListView')

    # con estos decoradores desactivo metodos de defensa

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print('* action')
            print(action)
            if action == 'search_comprobantes':
                data = []
                comprobantes = Comprobante.objects.filter(
                    comprobante_cliente=request.POST['term'])
                for i in comprobantes:
                    item = i.toJSON()
                    item['value'] = i.comprobante_cliente.dni
                    data.append(item)
            elif action == 'search_cheques':
                data = []
                print('request.POST')
                print(request.POST)
                cheques = Cheque.objects.filter(
                    cheque_banco__nombre__icontains=request.POST['term'])
                for i in cheques:
                    item = i.toJSON()
                    item['value'] = i.cheque_banco.nombre
                    # item['value'] = str(i.id)
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    detComprobante = json.loads(request.POST['detComprobante'])
                    detCheques = json.loads(request.POST['detCheques'])
                    print('1 subtotalCheq')
                    print(detCheques['subtotalCheq'])
                    print(detComprobante['comprobantes'])
                    # print(detCheques['cheque'])
                    recibo = Recibo()

                    recibo.fecha = detComprobante['fecha']
                    recibo.fecha = detCheques['fecha']
                    print('1 detComprobante')
                    print(detComprobante)
                    print('2 detCheques')
                    print(detCheques)
                    recibo.recibo_cliente = Cliente.objects.get(pk=detComprobante['recibo_cliente'])
                    recibo.recibo_planilla = Planilla.objects.get(
                        pk=detComprobante['recibo_planilla'])
                    recibo.recibo_caja = Caja.objects.get(
                        pk=detComprobante['recibo_caja'])
                    recibo.estado = detComprobante['estado']
                    # recibo.comprobantes = Comprobante.objects.get(pk=detComprobante['comprobantes'])
                    recibo.subtotalComp = float(detComprobante['subtotalComp'])
                    recibo.efectivo = float(detComprobante['efectivo'])
                    # recibo.cheque = Cheque.objects.get(pk=detCheques['cheque'])
                    recibo.subtotalCheq = float(detCheques['subtotalCheq'])
                    recibo.total = float(detComprobante['total'])
                    recibo.save()

            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        finally:
            print('data recibo Factura')
            print(data)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Recibo Factura'
        context['entity'] = 'Recibos'
        context['list_url'] = reverse_lazy('SGCapp:ReciboFacturaListView')
        context['action'] = 'add'
        return context


class ReciboFacturaDeleteView(DeleteView):
    model = Recibo
    template_name = 'SGCapp/recibos_facturas/delete.html'
    success_url = reverse_lazy('SGCapp:ReciboFacturaListView')

    @ method_decorator(login_required)
    @ method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post')
        print(request.POST)
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

        print(request.POST)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        print(self.success_url)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Recibo'
        context['entity'] = 'Recibos'
        context['list_url'] = self.success_url
        return context

# vista form Recibo Factura


class ReciboFormView(FormView):
    form_class = ReciboForm
    template_name = 'SGCapp/recibos_facturas/create.html'
    success_url = reverse_lazy('SGCapp:ReciboFacturaListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formulario Recibo'
        context['entity'] = 'Recibo'
        context['list_url'] = self.success_url
        return context


# vista Caja--------------------------------


class CajaListView(ListView):
    model = Caja
    template_name = 'SGCapp/cajas/list.html'

    @ method_decorator(login_required)
    @ method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post')
        print(request.POST)
        # print(request.FILE)

        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Caja.objects.all()[:]:
                    # print(i)
                    # print(data)
                    caja = i.toJSON()
                    # asigno el nombre del campo en el diccionario
                    caja['user_caja'] = i.user_caja.username
                    print(caja)
                    data.append(caja)
                    # data.append(i.toJSON())
                # for i in Cheque.objects.all():
                #     data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cajas'
        context['create_url'] = reverse_lazy('SGCapp:CajaCreateView')
        context['list_url'] = reverse_lazy('SGCapp:CajaListView')
        context['entity'] = 'Cajas'
        print(reverse_lazy('SGCapp:CajaListView'))
        return context

# caja form


class CajaFormView(FormView):
    form_class = CajaForm
    template_name = 'SGCapp/cajas/create.html'
    success_url = reverse_lazy('SGCapp:CajaListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formulario caja'
        context['entity'] = 'Cajas'
        context['list_url'] = self.success_url
        return context


class CajaCreateView(CreateView):
    model = Caja
    form_class = CajaForm
    template_name = 'SGCapp/cajas/create.html'
    success_url = reverse_lazy('SGCapp:CajaListView')

    @ method_decorator(login_required)
    @ method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear caja'
        context['entity'] = 'Cajas'
        context['list_url'] = reverse_lazy('SGCapp:CajaListView')
        context['action'] = 'add'
        return context


class CajaUpdateView(UpdateView):

    model = Caja
    form_class = CajaForm
    template_name = 'SGCapp/cajas/create.html'
    success_url = reverse_lazy('SGCapp:CajaListView')

    @ method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post')
        print(request.POST)
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        print(self.get_object())
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar cajas'
        context['entity'] = 'Cajas'
        context['list_url'] = reverse_lazy('SGCapp:CajaListView')
        context['action'] = 'edit'
        return context


class CajaDeleteView(DeleteView):
    model = Caja
    template_name = 'SGCapp/cajas/delete.html'
    success_url = reverse_lazy('SGCapp:CajaListView')

    @ method_decorator(login_required)
    @ method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

        print(request.POST)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar caja'
        context['entity'] = 'Caja'
        context['list_url'] = self.success_url
        return context


# vista planilla--------------------------------
class PlanillaListView(ListView):
    model = Planilla
    template_name = 'SGCapp/planillas/list.html'

    @ method_decorator(login_required)
    @ method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post planilla')
        print(request.POST)
        # print(request.FILE)

        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Planilla.objects.all()[:]:
                    print(i)
                    print(data)
                    planilla = i.toJSON()
                    # asigno el nombre del campo en el diccionario
                    planilla['planilla_cobrador'] = i.planilla_cobrador.nombre
                    # if planilla['estado'] == 'C':
                    #     planilla['fecha_cierre'] = i.fecha_cierre.strftime('%y-%m-%d')
                    # else:
                    #     planilla['fecha_cierre'] = None
                    print(planilla)
                    data.append(planilla)

            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Planillas'
        context['create_url'] = reverse_lazy('SGCapp:PlanillaCreateView')
        context['list_url'] = reverse_lazy('SGCapp:PlanillaListView')
        context['entity'] = 'Planillas'
        print(reverse_lazy('SGCapp:PlanillaListView'))
        return context

# Planillas form


class PlanillaFormView(FormView):
    form_class = CajaForm
    template_name = 'SGCapp/planilas/create.html'
    success_url = reverse_lazy('SGCapp:PlanillaListView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formulario planilla'
        context['entity'] = 'Planillas'
        context['list_url'] = self.success_url
        return context


class PlanillaCreateView(CreateView):
    model = Planilla
    form_class = PlanillaForm
    template_name = 'SGCapp/planillas/create.html'
    success_url = reverse_lazy('SGCapp:PlanillaListView')

    @ method_decorator(login_required)
    @ method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = []
                # for i in Planilla.objects.all()[:]:
                #     print(i)
                #     print(data)
                #     planilla = i.toJSON()
                #     # asigno el nombre del campo en el diccionario
                #     planilla['planilla_cobrador'] = i.planilla_cobrador.nombre
                #     if planilla['estado'] == 'C':
                #         planilla['fecha_cierre'] = i.fecha_cierre.strftime('%y-%m-%d')
                #     else:
                #         planilla['fecha_cierre'] = None
                #     print(planilla)
                #     data.append(planilla)
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear planilla'
        context['entity'] = 'Planillas'
        context['list_url'] = reverse_lazy('SGCapp:PlanillaListView')
        context['action'] = 'add'
        return context


class PlanillaUpdateView(UpdateView):

    model = Planilla
    form_class = PlanillaForm
    template_name = 'SGCapp/planillas/create.html'
    success_url = reverse_lazy('SGCapp:PlanillaListView')

    @ method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        print('imprimir post')
        print(request.POST)
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        print(self.get_object())
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar planillas'
        context['entity'] = 'Planillas'
        context['list_url'] = reverse_lazy('SGCapp:PlanillaListView')
        context['action'] = 'edit'
        return context


class PlanillaDeleteView(DeleteView):
    model = Planilla
    template_name = 'SGCapp/planillas/delete.html'
    success_url = reverse_lazy('SGCapp:PlanillaListView')

    @ method_decorator(login_required)
    @ method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

        print(request.POST)
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar planilla'
        context['entity'] = 'Planillas'
        context['list_url'] = self.success_url
        return context
