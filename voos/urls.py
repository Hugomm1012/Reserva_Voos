from django.urls import path
from . import views

app_name = 'voos'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    # Voos — 'novo' TEM de vir ANTES de <str:numero> para não ser capturado como número de voo
    path('voos/', views.VooListView.as_view(), name='flights'),
    path('voos/novo/', views.VooCreateView.as_view(), name='voo-create'),
    path('voos/<str:numero>/', views.VooDetailView.as_view(), name='voo-detail'),
    path('voos/<str:numero>/editar/', views.VooUpdateView.as_view(), name='voo-update'),
    path('voos/<str:numero>/eliminar/', views.VooDeleteView.as_view(), name='voo-delete'),

    # Passageiros — 'novo' TEM de vir ANTES de <int:pk>
    path('passageiros/', views.PassageiroListView.as_view(), name='passageiro-list'),
    path('passageiros/novo/', views.PassageiroCreateView.as_view(), name='passageiro-create'),
    path('passageiros/<int:pk>/', views.PassageiroDetailView.as_view(), name='passageiro-detail'),
    path('passageiros/<int:pk>/editar/', views.PassageiroUpdateView.as_view(), name='passageiro-update'),
    path('passageiros/<int:pk>/eliminar/', views.PassageiroDeleteView.as_view(), name='passageiro-delete'),

    # Reservas — 'novo' TEM de vir ANTES de <int:pk>
    path('reservas/', views.ReservaListView.as_view(), name='reserva-list'),
    path('reservas/novo/', views.ReservaCreateView.as_view(), name='reserva-create'),
    path('reservas/<int:pk>/', views.ReservaDetailView.as_view(), name='reserva-detail'),
    path('reservas/<int:pk>/editar/', views.ReservaUpdateView.as_view(), name='reserva-update'),
    path('reservas/<int:pk>/eliminar/', views.ReservaDeleteView.as_view(), name='reserva-delete'),
    path('reservas/<int:pk>/confirmar/', views.ReservaConfirmView.as_view(), name='reserva-confirm'),
    path('reservas/<int:pk>/cancelar/', views.ReservaCancelView.as_view(), name='reserva-cancel'),

    # Autenticação
    path('login/', views.VoosLoginView.as_view(), name='login'),
    path('logout/', views.VoosLogoutView.as_view(), name='logout'),
    path('registar/', views.RegisterView.as_view(), name='register'),

    # Área do cliente (ver as suas reservas)
    path('conta/', views.AccountView.as_view(), name='account'),

    # Reservar um voo específico
    path('reservar/<str:numero>/', views.BookingView.as_view(), name='booking'),

    # Painel de administração customizado
    path('admin-painel/', views.AdminPanelView.as_view(), name='admin-panel'),
]
