from django.urls import path
from SGCapp import views
from SGCapp.views import *
from django.conf.urls import url


app_name = 'SGCapp'
urlpatterns = [
    # url home
    path('dashboard/', dashboardView.as_view(), name='dashboard'),
    # urls clientes
    path('list2/', views.clientes_list, name='clientes_list'),
    path('list/', views.ClienteListView.as_view(), name='ClienteListView'),
    path('add/', views.ClienteCreateView.as_view(), name='ClienteCreateView'),
    path('edit/<int:pk>/', views.ClienteUpdateView.as_view(), name='ClienteUpdateView'),
    path('delete/<int:pk>/', views.ClienteDeleteView.as_view(), name='ClienteDeleteView'),
    # urls cobrador
    path('formcliente/', views.ClienteFormView.as_view(), name='ClienteFormView'),
    path('listcobrador/', views.CobradorListView.as_view(), name='CobradorListView'),
    path('addcobrador/', views.CobradorCreateView.as_view(), name='CobradorCreateView'),
    path('editcobrador/<int:pk>/', views.CobradorUpdateView.as_view(), name='CobradorUpdateView'),
    path('deletecobrador/<int:pk>/', views.CobradorDeleteView.as_view(), name='CobradorDeleteView'),
    # urls Bancos
    path('listbanco/', views.BancoListView.as_view(), name='BancoListView'),
    path('addbanco/', views.BancoCreateView.as_view(), name='BancoCreateView'),
    path('editbanco/<int:pk>/', views.BancoUpdateView.as_view(), name='BancoUpdateView'),
    path('deletebanco/<int:pk>/', views.BancoDeleteView.as_view(), name='BancoDeleteView'),
    # urls Cheques
    path('listcheque/', views.ChequeListView.as_view(), name='ChequeListView'),
    path('addcheque/', views.ChequeCreateView.as_view(), name='ChequeCreateView'),
    path('editcheque/<int:pk>/', views.ChequeUpdateView.as_view(), name='ChequeUpdateView'),
    path('deletecheque/<int:pk>/', views.ChequeDeleteView.as_view(), name='ChequeDeleteView'),

    # urls Comprobantes
    path('listcomprobante/', views.ComprobanteListView.as_view(), name='ComprobanteListView'),
    path('addcomprobante/', views.ComprobanteCreateView.as_view(), name='ComprobanteCreateView'),
    path('editcomprobante/<int:pk>/', views.ComprobanteUpdateView.as_view(), name='ComprobanteUpdateView'),
    path('deletecomprobante/<int:pk>/', views.ComprobanteDeleteView.as_view(), name='ComprobanteDeleteView'),

    # urls Recibos_facturas
    path('listReciboFactura/', views.ReciboFacturaListView.as_view(),
         name='ReciboFacturaListView'),
    path('addReciboFactura/', views.ReciboFacturaCreateView.as_view(),
         name='ReciboFacturaCreateView'),
    path('deleteReciboFactura/<int:pk>/',
         views.ReciboFacturaDeleteView.as_view(), name='ReciboFacturaDeleteView'),

    # urls Caja
    path('listCaja/', views.CajaListView.as_view(),
         name='CajaListView'),
    path('addCaja/', views.CajaCreateView.as_view(),
         name='CajaCreateView'),
    path('editCaja/<int:pk>/', views.CajaUpdateView.as_view(),
         name='CajaUpdateView'),
    path('deleteCaja/<int:pk>/',
         views.CajaDeleteView.as_view(), name='CajaDeleteView'),

    # urls Planilla
    path('listPlanilla/', views.PlanillaListView.as_view(),
         name='PlanillaListView'),
    path('addPlanilla/', views.PlanillaCreateView.as_view(),
         name='PlanillaCreateView'),
    path('editPlanilla/<int:pk>/', views.PlanillaUpdateView.as_view(),
         name='PlanillaUpdateView'),
    path('deletePlanilla/<int:pk>/',
         views.PlanillaDeleteView.as_view(), name='PlanillaDeleteView'),

]
