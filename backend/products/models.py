from django.db import models


choices_categorias = [
    ('APARELHOS', 'Aparelhos'),
    ('ROUPAS', 'Roupas'),
]

class Produtos(models.Model):
    produto_imagem = models.ImageField(upload_to='produtos')
    nome = models.CharField(max_length=50, null=False, blank=False, unique=True)
    descricao = models.TextField(blank=False, null=False)
    categoria = models.CharField(max_length=50, null=False, blank=False, choices=choices_categorias)
    preco = models.FloatField(default=1.00)


    def __str__(self) -> str:
        return self.nome
