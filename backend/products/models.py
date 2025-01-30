from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User

choices_categorias = [
    ('APARELHOS', 'Aparelhos'),
    ('ROUPAS', 'Roupas'),
]

def validar_quantidade(value):
    if value < 0:
        raise ValidationError('Quantidade não pode ser negativa!')

def validar_preco(value):
    if value <= 0:
        raise ValidationError('Preço deve ser maior que zero!')

class Produtos(models.Model):
    produto_imagem = models.ImageField(upload_to='produtos')
    nome = models.CharField(max_length=50, null=False, blank=False, unique=True)
    descricao = models.TextField(blank=False, null=False)
    categoria = models.CharField(max_length=50, null=False, blank=False, choices=choices_categorias)
    quantidade = models.IntegerField(validators=[validar_quantidade], null=False, blank=False)
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,  
        default=0.000,
        validators=[validar_preco]
    )


    def __str__(self) -> str:
        return self.nome

class Avaliacao(models.Model):
    produto = models.ForeignKey(Produtos, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estrelas = models.PositiveIntegerField(default=5)
    comentario = models.TextField(null=True, blank=True)
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.produto.nome}'