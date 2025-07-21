from django.db import models
from django.core.validators import MinValueValidator


# Model para guardar configurações gerais do sistema
class Configuracao(models.Model):
    taxa_entrega_padrao = models.DecimalField(
        "taxa da Entrega Padrão (R$)",
        max_digits=5,
        decimal_places=2,
        default=5.00,
        validators=[MinValueValidator(0.0)]
    )

    def __str__(self):
        return f"Configurações Gerais"

    class Meta:
        verbose_name = "Configuração do Sistema"
        verbose_name_plural = "Configurações do Sistema"


# Model para os tamanhos das quentinhas
class TamanhoQuentinha(models.Model):
    nome = models.CharField("Nome do Tamanho", max_length=50, unique=True)
    preco_base = models.DecimalField("Preço Base (R$)", max_digits=5, decimal_places=2,
                                     validators=[MinValueValidator(0.0)])
    limite_proteinas = models.PositiveIntegerField("Limite de Proteínas", default=1)

    def __str__(self):
        return f"{self.nome} - R$ {self.preco_base}"


# Model para todos os itens do cardápio (Guarnições e proteínas)
class ItemCardapio(models.Model):
    class Tipo(models.TextChoices):
        ARROZ = 'ARROZ', 'Arroz'
        FEIJÃO = 'FEIJAO', 'Feijao'
        GUARNICAO = 'GUARNICAO', 'Guarnicao'
        PROTEINA = 'PROTEINA', 'proteina'

    nome = models.CharField('Nome do ítem', max_length=100)
    tipo_item = models.CharField("Tipo do Item", max_length=10, choices=Tipo.choices)

    def __str__(self):
        # Retorna o nome do item e sua categoria entre colchetes
        return f'{self.nome} [{self.get_tipo_item_display()}]'


# Model para os itens adicionais pagos
class Adicional(models.Model):
    nome = models.CharField('Nome do Adicional', max_length=100)
    preco = models.DecimalField(
        'Preço (R$)',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.0)]
    )
    disponivel = models.BooleanField("Disponível?", default=True)

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"

# Model principal que representa o pedido do cliente
class Pedido(models.Model):
    class Status(models.TextChoices):
        RECEBIDO = 'RECEBIDO', 'Recebido'
        EM_PREPARO = 'EM_PREPARO', 'Em preparo'
        SAIU_PARA_ENTREGA = 'SAIU_PARA_ENTREGA', 'Saiu para Entrega'
        CONCLUIDO = 'CONCLUIDO', 'Concluido'

    class MetodoPagamento(models.TextChoices):
        DINHEIRO = 'DINHEIRO', 'Dinheiro'
        PIX = 'PIX', 'Pix'
        CREDITO = 'CREDITO', 'Credito'
        DEBITO = 'DEBITO', 'Debito'

    # Informações do Cliente e Entrega
    cliente = models.CharField("Nome do Cliente", max_length=100)
    telefone = models.CharField("Telefone (Whatsapp)", max_length=20)
    endereco_rua = models.CharField("Rua/Avenida", max_length=200)
    endereco_numero = models.CharField("Número", max_length=20)
    endereco_bairro = models.CharField("Bairro", max_length=100)
    endereco_referencia = models.CharField(
        "Ponto de referência",
        max_length=200,
        blank=True
    )


    # Itens do Pedido
    tamanho_quentinha = models.ForeignKey(
        TamanhoQuentinha,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Tamanho da Quentinha"
    )
    itens_escolhidos = models.ManyToManyField(
        ItemCardapio,
        verbose_name="Itens Escolhidos"
    )
    adicionais_escolhidos = models.ManyToManyField(
        Adicional,
        blank=True,
        verbose_name="Adicionais"
    )

    # Model para metodo de pagamento
    metodo_pagamento = models.CharField(
        "Método de Pagamento",
        max_length=20,
        choices=MetodoPagamento.choices,
        default=MetodoPagamento.PIX
    )

    valor_troco_para = models.DecimalField(
        "Troco para (R$)",
        max_digits=7,
        decimal_places=2,
        null=True, # Permite que o campo seja nulo no banco de dados
        blank=True # Permite que o campo não seja preenchido no formulário
    )

    # Valores e Status
    taxa_entrega = models.DecimalField("Taxa de Entrega (R$)", max_digits=5, decimal_places=2, default=0.00)
    preco_total = models.DecimalField("Preço total (R$)", max_digits=6, decimal_places=2, default=0.00)
    data_hora = models.DateTimeField("Data e Hora do Pedido", auto_now_add=True)
    status = models.CharField("Status do Pedido", max_length=20, choices=Status.choices, default=Status.RECEBIDO)

    # Futuramente, podemos adicionar um método save() para calcular o preço total automaticamente

    def __str__(self):
        return f"Pedido de {self.cliente} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"
