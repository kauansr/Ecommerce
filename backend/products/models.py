from django.db import models
from django.core.exceptions import ValidationError


choices_categorias = [
    ('APARELHOS', 'Aparelhos'),
    ('ROUPAS', 'Roupas'),
]

def validar_quantidade(value):
    if value < 0:
        raise ValidationError('Quantidade não pode ser negativa!')

class Produtos(models.Model):
    produto_imagem = models.ImageField(upload_to='produtos')
    nome = models.CharField(max_length=50, null=False, blank=False, unique=True)
    descricao = models.TextField(blank=False, null=False)
    categoria = models.CharField(max_length=50, null=False, blank=False, choices=choices_categorias)
    quantidade = models.IntegerField(validators=[validar_quantidade], null=False, blank=False)
    preco = models.FloatField(default=1.00)


    def __str__(self) -> str:
        return self.nome
