import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def buscar_recursos_educativos(palabra_clave):
    """
    Realiza scraping de recursos educativos basados en una palabra clave
    Busca en Wikipedia en español para obtener información educativa
    """
    resultados = []
    
    try:
        # Búsqueda en Wikipedia
        url_busqueda = f"https://es.wikipedia.org/w/index.php?search={quote_plus(palabra_clave)}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url_busqueda, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Si nos redirige directamente a un artículo
        if 'Special:Search' not in response.url:
            titulo_elemento = soup.find('h1', {'id': 'firstHeading'})
            titulo = titulo_elemento.text if titulo_elemento else 'Sin título'
            
            # Obtener primer párrafo
            contenido_div = soup.find('div', {'id': 'mw-content-text'})
            primer_parrafo = ''
            if contenido_div:
                parrafos = contenido_div.find_all('p')
                for p in parrafos:
                    if p.text.strip():
                        primer_parrafo = p.text.strip()[:300] + '...'
                        break
            
            resultados.append({
                'titulo': titulo,
                'descripcion': primer_parrafo,
                'url': response.url,
                'fuente': 'Wikipedia'
            })
        else:
            # Si muestra resultados de búsqueda
            resultados_busqueda = soup.find_all('div', {'class': 'mw-search-result-heading'})
            
            for resultado in resultados_busqueda[:5]:  # Limitar a 5 resultados
                link = resultado.find('a')
                if link:
                    titulo = link.text
                    url = 'https://es.wikipedia.org' + link['href']
                    
                    # Intentar obtener descripción
                    descripcion = ''
                    resultado_parent = resultado.find_parent('div', {'class': 'mw-search-result'})
                    if resultado_parent:
                        desc_div = resultado_parent.find('div', {'class': 'searchresult'})
                        if desc_div:
                            descripcion = desc_div.text.strip()[:200] + '...'
                    
                    resultados.append({
                        'titulo': titulo,
                        'descripcion': descripcion,
                        'url': url,
                        'fuente': 'Wikipedia'
                    })
        
        # Si no hay resultados, buscar en otro sitio educativo
        if not resultados:
            # Búsqueda alternativa en un sitio educativo general
            url_alternativa = f"https://www.example.com/search?q={quote_plus(palabra_clave)}"
            resultados.append({
                'titulo': f'Búsqueda: {palabra_clave}',
                'descripcion': 'No se encontraron resultados específicos. Intenta con otras palabras clave.',
                'url': url_alternativa,
                'fuente': 'Sistema'
            })
    
    except requests.RequestException as e:
        resultados.append({
            'titulo': 'Error en la búsqueda',
            'descripcion': f'No se pudo completar la búsqueda: {str(e)}',
            'url': '#',
            'fuente': 'Error'
        })
    except Exception as e:
        resultados.append({
            'titulo': 'Error inesperado',
            'descripcion': f'Ocurrió un error: {str(e)}',
            'url': '#',
            'fuente': 'Error'
        })
    
    return resultados