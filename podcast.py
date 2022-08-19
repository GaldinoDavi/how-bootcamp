# %%
# # Importando as bibliotecas
from os import link
import requests
from bs4 import BeautifulSoup as bs
import logging
import pandas as pd


# %%

# Realizando o request no site.
url = 'https://portalcafebrasil.com.br/todos/podcasts/'
r = requests.get(url)
print(r.text)

# Melhorando a organização com BeautifullSoup
soup = bs(r.text)
soup

# Com base na inspeção do navegador iremos agora obter o título e o link
soup.find('h5')
soup.find('h5').text
soup.find('h5').a['href']


# %%

# Realizando uma extrutura de repetição para trazer todos os podcasts e links
podcasts = soup.find_all('h5')
for x in podcasts:
    print(f"EP: {x.text} - link: {x.a['href']}")


# %%

# Para poder extrair todos os episódios o link da url ficará variavel no numero da pagina
url = 'https://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true'


# %%

# Transformando a extração em funcao
def get_podcast(url):
    ret = requests.get(url)
    soup = bs(ret.text)
    return soup.find_all('h5')


# %%

# Realizando um teste para a página 10
url.format(10)
get_podcast(url.format(10))


# %%

# Criando um log para poder utilizar o nosso loop sem medo
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)


# %%

# Montando o loop para extrair todos os dados de podcast
i = 1
podcasts_total = []
podcast_get = get_podcast(url.format(i))
log.debug(f'Coletado {len(podcast_get)} episódios do link {url.format(i)}')

while len(podcast_get) > 0:
    podcasts_total = podcasts_total + podcast_get
    i += 1
    podcast_get = get_podcast(url.format(i))
    log.debug(f'Coletado {len(podcast_get)} episódios do link {url.format(i)}')

# %%

# Verificando o tamanho
len(podcasts_total)


# %%

# Verificando se as informacoes estao correta
podcasts_total


# %%

# Criando um dataframe para adicionar a lista de podcast
df = pd.DataFrame(columns=['Nome', 'link'])


# %%

# Realizando a transformação
for item in podcasts_total:
    df.loc[df.shape[0]] = [item.text, item.a['href']]


# %%

# Verificando o tamanho
df.shape


# %%

# Visualizando o dataframe
df


# %%

# Gerando uma extração em csv
df.to_csv('podcast_cafe_brasil', sep=';', index=False)
