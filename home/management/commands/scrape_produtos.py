import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from home.models import Produto  # substitui "app" pelo nome do seu app

class Command(BaseCommand):
    help = "Faz scraping de produtos e salva no banco"

    def handle(self, *args, **kwargs):
        self.scrape_kabum()
        self.scrape_mercadolivre()

    def scrape_kabum(self):
        url = "https://www.kabum.com.br/hardware/processadores"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for item in soup.select("div.productCard"):
            nome = item.select_one("span.nameCard").get_text(strip=True)
            preco = item.select_one("span.priceCard").get_text(strip=True).replace("R$", "").replace(".", "").replace(",", ".").strip()
            link = "https://www.kabum.com.br" + item.a["href"]

            Produto.objects.get_or_create(
                nome=nome,
                loja="Kabum",
                defaults={
                    "descricao": nome,
                    "precoNormal": float(preco),
                    "precoDesconto": float(preco),
                    "tipoDeProduto": "processador",
                    "cupom": "",
                    "imagem": "",
                    "link": link,
                }
            )

        self.stdout.write(self.style.SUCCESS("Kabum importado!"))

    def scrape_mercadolivre(self):
        url = "https://api.mercadolibre.com/sites/MLB/search?q=processador"
        response = requests.get(url).json()

        for item in response["results"]:
            Produto.objects.get_or_create(
                nome=item["title"],
                loja="Mercado Livre",
                defaults={
                    "descricao": item["title"],
                    "precoNormal": item["price"],
                    "precoDesconto": item["price"],
                    "tipoDeProduto": "processador",
                    "cupom": "",
                    "imagem": item.get("thumbnail", ""),
                    "link": item["permalink"],
                }
            )

        self.stdout.write(self.style.SUCCESS("Mercado Livre importado!"))
