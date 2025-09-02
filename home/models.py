from django.db import models
from decimal import Decimal

# Create your models here.
class Produto(models.Model):
    loja = models.CharField(verbose_name='Loja', max_length=50)
    nome = models.CharField(verbose_name='Nome', max_length=255)
    descricao = models.TextField(verbose_name='Descrição', blank=True)
    precoNormal = models.FloatField(verbose_name='Preço normal')
    precoDesconto = models.FloatField(verbose_name='Preço com desconto')
    tipoDeProduto = models.SlugField(verbose_name='Tipo de produto')
    cupom = models.CharField(verbose_name='Cupom', blank=True)
    imagem = models.FileField(verbose_name='Imagem',upload_to='imagens_produto', blank=True, max_length=255)
    link = models.TextField(verbose_name='Link')

    def __str__(self):
        return self.nome
    
    @property
    def preco_normal_formatado(self):
        """Retorna o preço normal formatado em Real brasileiro"""
        try:
            return f"R$ {Decimal(self.precoNormal):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except:
            return "R$ 0,00"
    
    @property
    def preco_desconto_formatado(self):
        """Retorna o preço com desconto formatado em Real brasileiro"""
        try:
            if self.precoDesconto:
                return f"R$ {Decimal(self.precoDesconto):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            return "Não há desconto"
        except:
            return "R$ 0,00"
    
    def save(self, *args, **kwargs):
        # Garante que os preços sempre tenham 2 casas decimais
        if isinstance(self.precoNormal, str):
            self.precoNormal = self.precoNormal.replace('.', '').replace(',', '.')
        if isinstance(self.precoDesconto, str):
            self.precoDesconto = self.precoDesconto.replace('.', '').replace(',', '.')
        super().save(*args, **kwargs)