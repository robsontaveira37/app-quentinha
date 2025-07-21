from django.urls import path
from . import views

# Este é um "namespace" para evitar conflito de nomes com outros apps
app_name = 'pedidos'

urlpatterns = [
    # A URL raiz vai chamar a view index
    path('', views.index, name='index'),

    # Uma nova URL para a página de SUCESSO após o pedido.
    path('sucesso/', views.sucesso, name='sucesso'),
]