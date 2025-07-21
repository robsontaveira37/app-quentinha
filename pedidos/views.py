# Em pedidos/views.py - SUBSTITUA SUA FUNÇÃO INDEX INTEIRA POR ESTA

from django.shortcuts import render, redirect
from django.db import transaction
from .models import TamanhoQuentinha, ItemCardapio, Adicional, Pedido, Configuracao
from decimal import Decimal


def index(request):
    # Lógica para quando o cliente envia o formulário (método POST)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # 1. Pegar dados do cliente e do formulário
                cliente = request.POST.get('cliente')
                telefone = request.POST.get('telefone')
                endereco_rua = request.POST.get('endereco_rua')
                endereco_numero = request.POST.get('endereco_numero')
                endereco_bairro = request.POST.get('endereco_bairro')
                endereco_referencia = request.POST.get('endereco_referencia')
                metodo_pagamento = request.POST.get('metodo_pagamento')
                valor_troco_para = request.POST.get('valor_troco_para')
                tamanho_id = request.POST.get('tamanho_quentinha')

                # Pega a lista de IDs de adicionais que o usuário MARCOU no formulário
                adicionais_ids = request.POST.getlist('adicionais')

                # 2. Juntar os IDs de todos os itens da quentinha
                todos_os_itens_ids = []

                # Pega o ID do arroz e adiciona à lista
                id_do_arroz = request.POST.get('itens_cardapio_arroz')
                if id_do_arroz:
                    todos_os_itens_ids.append(id_do_arroz)

                # Pega o ID do feijão e adiciona à lista
                id_do_feijao = request.POST.get('itens_cardapio_feijao')
                if id_do_feijao:
                    todos_os_itens_ids.append(id_do_feijao)

                # Pega a lista de IDs das guarnições e proteínas que o usuário MARCOU
                ids_dos_checkboxes = request.POST.getlist('itens_cardapio')
                if ids_dos_checkboxes:
                    todos_os_itens_ids.extend(ids_dos_checkboxes)

                # 3. Buscar os objetos no banco de dados
                tamanho_quentinha_obj = TamanhoQuentinha.objects.get(id=tamanho_id)
                config = Configuracao.objects.first()

                # Filtra o modelo ItemCardapio para pegar APENAS os objetos cujos IDs estão na nossa lista
                itens_obj = ItemCardapio.objects.filter(id__in=todos_os_itens_ids)

                # Filtra o modelo Adicional para pegar APENAS os objetos cujos IDs estão na lista de adicionais
                adicionais_obj = Adicional.objects.filter(id__in=adicionais_ids)

                # 4. Calcular o preço total
                preco_total = tamanho_quentinha_obj.preco_base
                for adicional in adicionais_obj:
                    preco_total += adicional.preco

                taxa_entrega = config.taxa_entrega_padrao if config else Decimal('0.00')
                preco_total += taxa_entrega

                # 5. Criar o objeto Pedido
                novo_pedido = Pedido(
                    cliente=cliente,
                    telefone=telefone,
                    endereco_rua=endereco_rua,
                    endereco_numero=endereco_numero,
                    endereco_bairro=endereco_bairro,
                    endereco_referencia=endereco_referencia,
                    metodo_pagamento=metodo_pagamento,
                    tamanho_quentinha=tamanho_quentinha_obj,
                    taxa_entrega=taxa_entrega,
                    preco_total=preco_total
                )

                if metodo_pagamento == 'DINHEIRO' and valor_troco_para:
                    novo_pedido.valor_troco_para = Decimal(valor_troco_para)

                novo_pedido.save()

                # Salva as relações com os QuerySets JÁ FILTRADOS
                novo_pedido.itens_escolhidos.set(itens_obj)
                novo_pedido.adicionais_escolhidos.set(adicionais_obj)

            return redirect('pedidos:sucesso')

        except Exception as e:
            print(f"Ocorreu um erro ao processar o pedido: {e}")
            return redirect('pedidos:index')

    # Lógica para carregar a página (método GET)
    context = {
        'tamanhos': TamanhoQuentinha.objects.all(),
        'arroz_opcoes': ItemCardapio.objects.filter(tipo_item='ARROZ'),
        'feijao_opcoes': ItemCardapio.objects.filter(tipo_item='FEIJAO'),
        'guarnicoes_opcoes': ItemCardapio.objects.filter(tipo_item='GUARNICAO'),
        'proteinas_opcoes': ItemCardapio.objects.filter(tipo_item='PROTEINA'),
        'adicionais_opcoes': Adicional.objects.filter(disponivel=True),
    }
    return render(request, 'pedidos/index.html', context)


# View para a página de sucesso
def sucesso(request):
    return render(request, 'pedidos/sucesso.html')
