from django.db import models
from accounts.models import User

status_entregachoice = [
    ('PREPARANDO...','Preparando...'),
    ('ENVIADO','Enviado'),
    ('ENTREGUE','Entregue')
]

class Pedidos(models.Model):
    nome_pedido = models.CharField(max_length=50)
    preco = models.FloatField()
    email = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    entrega_status = models.CharField(max_length=20, choices=status_entregachoice, default='PREPARANDO...')


    def __str__(self) -> str:
        return self.nome_pedido



