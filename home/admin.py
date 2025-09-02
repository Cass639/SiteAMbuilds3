from django.contrib import admin
from home.models import Produto

# Register your models here.
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('loja', 'nome', 'precoNormal', 'precoDesconto', 'tipoDeProduto', 'imagem', 'link',)
    list_filter = ('loja', 'tipoDeProduto')
    ordering = ('loja', 'tipoDeProduto')
    search_fields = ('nome',)