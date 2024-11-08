from django.db import models
from accounts.models import User
from products.models import Produtos

status_entregachoice = [
    ('PREPARANDO...','Preparando...'),
    ('ENVIADO','Enviado'),
    ('ENTREGUE','Entregue')
]

class Pedidos(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, blank=False)
    data_pedido = models.DateTimeField(auto_now_add=True)
    entrega_status = models.CharField(max_length=20, choices=status_entregachoice, default='PREPARANDO...')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.email}"



class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_item(self):
        return self.preco_unitario * self.quantidade

    def __str__(self):
        return f"Item {self.produto.nome} - Pedido {self.pedido.id}"