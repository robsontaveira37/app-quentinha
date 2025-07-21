from django.contrib import admin
from .models import Configuracao, TamanhoQuentinha, ItemCardapio, Adicional, Pedido

# Classe para melhorar a visualização dos Itens do Cardápio
class ItemCardapioAdmin(admin.ModelAdmin):
    # Colunas que aparecerão
    list_display = ('nome', 'tipo_item')

    # Filtros na lateral direita
    list_filter = ('tipo_item',)
    search_fields = ('nome',) # Campo de busca


class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'telefone', 'data_hora', 'status', 'preco_total')
    list_filter = ('status', 'data_hora')
    search_fields = ('cliente', 'telefone')

    # Deixa os campos ManyToMany mais fáceis de usar
    filter_horizontal = ('itens_escolhidos', 'adicionais_escolhidos')

# Registrando os models no admin
admin.site.register(Configuracao)
admin.site.register(TamanhoQuentinha)
admin.site.register(ItemCardapio, ItemCardapioAdmin)
admin.site.register(Adicional)
admin.site.register(Pedido, PedidoAdmin)