from django.db import models
from accounts.models import User
from products.models import Produtos

status_entregachoice = [
    ('PREPARANDO...','Preparando...'),
    ('ENVIADO','Enviado'),
    ('ENTREGUE','Entregue')
]

class Pedidos(models.Model):
    produto_id = models.ForeignKey(Produtos, on_delete=models.CASCADE, related_name='products')
    nome_pedido = models.CharField(max_length=255, blank=False)
    preco = models.FloatField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    email = models.EmailField(max_length=255)
    entrega_status = models.CharField(max_length=20, choices=status_entregachoice, default='PREPARANDO...')


    def __str__(self) -> str:
        return self.nome_pedido



