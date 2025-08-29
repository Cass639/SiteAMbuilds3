from django.shortcuts import render, redirect
from home.models import Produto

# Create your views here.

def calcular_desconto(produto):
    try:
        preco_normal = float(produto.precoNormal)
        preco_desconto = float(produto.precoDesconto)
        if preco_normal > 0 and preco_desconto < preco_normal:
            return round(((preco_normal - preco_desconto) / preco_normal) * 100)
        else:
            return 0
    except (ValueError, TypeError):
        return 0


def index(request):

    produtos_novos = Produto.objects.all().order_by('-id')[:10]
    produtos_random = Produto.objects.order_by('?')[:10]
    modelos_pc = Produto.objects.filter(tipoDeProduto="PC Gamer").order_by('-id')[:10]

    for produto in produtos_novos:
        produto.desconto = calcular_desconto(produto)
    for produto in produtos_random:
        produto.desconto = calcular_desconto(produto)
    for produto in modelos_pc:
        produto.desconto = calcular_desconto(produto)

    
    ORDEM_PERSONALIZADA = [
        "Processador", "Placa Mãe", "Memoria RAM", "Placa de Vídeo",
        "HD/SSD", "Gabinete", "Fonte"
    ]
    
    categorias_distintas = Produto.objects.values_list('tipoDeProduto', flat=True).distinct()
    categorias_existentes = [cat for cat in categorias_distintas if cat]
    
    categorias_data = []
    
    for categoria in categorias_existentes:
        # Encontra o primeiro produto desta categoria que tenha imagem
        produto_com_imagem = Produto.objects.filter(
            tipoDeProduto=categoria
        ).exclude(
            imagem__isnull=True
        ).exclude(
            imagem=''
        ).first()
        
        if produto_com_imagem and produto_com_imagem.imagem:
            img_url = produto_com_imagem.imagem.url
        else:
            # Se não tiver imagem, usa um placeholder
            img_url = "https://placehold.co/800?text=" + categoria.replace(' ', '+')
        
        categorias_data.append({
            "nome": categoria,
            "img": img_url
        })
    
    # Ordena conforme sua preferência
    categorias_ordenadas = []
    for categoria_nome in ORDEM_PERSONALIZADA:
        for cat_data in categorias_data:
            if cat_data["nome"] == categoria_nome:
                categorias_ordenadas.append(cat_data)
                break
    
    # Adiciona as categorias restantes
    for cat_data in categorias_data:
        if cat_data not in categorias_ordenadas:
            categorias_ordenadas.append(cat_data)
    
    context = {
        "produtos_novos": produtos_novos,
        "categorias": categorias_ordenadas,
        "produtos_random": produtos_random,
        "modelos_pc": modelos_pc
    }    
    return render(request, "home/index.html", context)


def detail(request, pk, tipoDeProduto):
    produto_especifico = Produto.objects.get(id=pk)
    produtos_relacionado = Produto.objects.filter(tipoDeProduto=tipoDeProduto).order_by('-id').exclude(id=produto_especifico.id)

    produto_especifico.desconto = calcular_desconto(produto_especifico)
    for produto in produtos_relacionado:
        produto.desconto = calcular_desconto(produto)

    context = {
        "produto_especifico": produto_especifico,
        "produtos_relacionado": produtos_relacionado,
    }
    return render(request, "home/detail.html", context)


def category(request, tipoDeProduto):
    produtos = Produto.objects.filter(tipoDeProduto=tipoDeProduto).order_by('-id')

    for produto in produtos:
        produto.desconto = calcular_desconto(produto)

    context = {
        "tipo": tipoDeProduto,
        "produtos": produtos,
    }
    return render(request, "home/category.html", context)