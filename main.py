import requests as r
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


def clear_text(text):
    return text.replace('\n', '').replace('\t', '').replace('\r', '').strip()


base_url = 'https://franquias.portaldofranchising.com.br/'

tipos = ["franquias-ate-5-mil",
         "franquias-ate-10-mil",
         "franquias-ate-25-mil",
         "franquias-ate-50-mil",
         "franquias-ate-75-mil",
         "franquias-ate-100-mil",
         "franquias-de-100-ate-200-mil",
         "franquias-de-200-ate-300-mil",
         "franquias-de-300-ate-400-mil",
         "franquias-de-400-ate-500-mil",
         "franquias-de-500-ate-750-mil",
         "franquias-acima-de-750-mil",
         ]
franquias = []

for tipo in tipos:
    search_page = r.get(f'https://franquias.portaldofranchising.com.br/{tipo}/',
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'},)
    # r = r.get('https://franquias.portaldofranchising.com.br/franquia-wizard-servicos-educacionais/')
    links = []

    soup = BeautifulSoup(search_page.text, 'html.parser')

    urls = soup.find('div', attrs={'class': 'col-xl-8 col-12'}).findAll(
        'div', attrs={'class': 'card card-catafranchise mb-2'})
    for url in urls:
        links.append(url.find('a')['href'])

    blue_urls = soup.find('div', attrs={'class': 'col-xl-8 col-12'}).findAll(
        'div', attrs={'class': 'card card-catafranchise adv mb-2'})

    for blue_url in blue_urls:
        links.append(blue_url.find('a')['href'])

    for link in tqdm(links):
        resultado = {}
        franq_page = r.get(link, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'},)
        soup = BeautifulSoup(franq_page.text, 'html.parser')

        about = soup.find('div', attrs={'class': 'tab-content about'})
        stores = soup.find('div', attrs={'class': 'tab-content Lojas d-none'})
        if stores:
            table = stores.find('table').findAll('th')

            index = 0
            for index in range(len(table)):
                if (index % 2 == 0):
                    key = clear_text(table[index].text)
                    resultado[key] = ""
                else:
                    resultado[key] = clear_text(table[index].text)
            items = stores.find(
                'div', attrs={'class': 'column-icons'}).findAll('p')
            index = 0
            for index in range(len(items)):
                if (index % 2 == 0):
                    key = clear_text(items[index].text)
                    resultado[key] = ""
                else:
                    resultado[key] = clear_text(items[index].text)
            index = 0
            topics = soup.findAll('p', attrs={'class': 'p-title-default my-0'})
            # for topic in stores:
            #     resultado[topic.text] = clear_text(
            #         topic[index].parent.strong.text)
            #     index += 1
            # falta pegar uns dados de loja

        # permalink = link
        # name = soup.find('h1').text
        # miminum_invest = clear_text(topics[0].parent.strong.text)
        # retorno = clear_text(topics[1].parent.strong.text)
        # unids_brazil = clear_text(topics[2].parent.strong.text)
        # contact = clear_text(topics[3].parent.strong.text)

# escreva uma funcao que crie um dicionario a partir de cada chave do topico
# e o valor do strong

        index = 0
        resultado["name"] = soup.find('h1').text
        resultado["permalink"] = link
        for topic in topics:
            if "SELO DE EXCELÊNCIA EM FRANCHISING" in topics[index].parent.text:
                continue
            resultado[topic.text] = clear_text(
                topics[index].parent.strong.text)
            index += 1

        franquias.append(resultado)
        # resultado.append({
        #     'permalink': permalink,
        #     'name': name,
        #     'miminum_invest': miminum_invest,
        #     'retorno': retorno,
        #     'unids_brazil': unids_brazil,
        #     'contact': contact,
        #     'price_range': tipo
        # })


df = pd.DataFrame(franquias)
df.to_excel('crawler_franquias/out/franquias2.xlsx', index=False)
