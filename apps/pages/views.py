from django.shortcuts import render
from pages.models import Blocos


import logging

logger = logging.getLogger(__name__)


def index(request):
	
	return render(request, 'index.html')

def paginas_view(request):
    logger.info(">>> paginas_view chamada")
    url_name = request.resolver_match.url_name
    logger.info(f"url_name recebido na view: {url_name}")

    pagina = {
        'home': Blocos.objects.filter(pagina__nome__iexact='inicio', ativo=True).order_by('ordem'),
        'sobre': Blocos.objects.filter(pagina__nome__iexact='sobre', ativo=True).order_by('ordem'),
    }

    blocos = pagina.get(url_name, [])
    logger.info(f"Blocos encontrados para {url_name}: {blocos.count() if hasattr(blocos, 'count') else 0}")

    context = {'blocos': blocos}
    return render(request, 'index.html', context)



