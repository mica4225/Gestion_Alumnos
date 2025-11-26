# scraper/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup
from django.core.mail import EmailMessage
from django.conf import settings
import csv
from io import StringIO
from .forms import BuscarForm

@login_required
def buscar(request):
    resultados = []
    form = BuscarForm()

    if request.method == 'POST':
        form = BuscarForm(request.POST)
        if form.is_valid():
            keyword = form.cleaned_data['palabra_clave']
            enviar = form.cleaned_data['enviar_email']

            # --- scraping ------------------
            url = f"https://html.duckduckgo.com/html/?q={keyword}"
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(r.text, 'html.parser')

            for a in soup.select('a.result__a')[:10]:
                resultados.append({
                    'titulo': a.get_text(),
                    'descripcion': 'Sin descripción',
                    'fuente': 'DuckDuckGo',
                    'url': a.get('href')
                })

            # guardar en sesión para enviar CSV
            request.session['last_scrape'] = resultados

            # si el usuario marcó "enviar por email"
            if enviar:
                return redirect('scraper:scraper_enviar')

    return render(request, 'scraper/buscar.html', {
        'form': form,
        'resultados': resultados
    })
@login_required
def enviar_scrape(request):
    results = request.session.get('last_scrape', [])
    if not results:
        return redirect('scraper_buscar')
    # crear CSV en memoria
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['title','link'])
    for r in results:
        writer.writerow([r['title'], r['link']])
    si.seek(0)
    email = EmailMessage('Resultados de scraping', 'Adjunto CSV', to=[request.user.email])
    email.attach('scrape.csv', si.read(), 'text/csv')
    email.send(fail_silently=False)
    return redirect('scraper_buscar')
