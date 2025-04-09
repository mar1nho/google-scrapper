from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def google_search_engine():
    # Configurações do navegador
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--log-level=3')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    products_list = []
    try:
        query = input("Digite o que deseja pesquisar no Google Shopping: ")
        result = query.replace(' ', '+')
        search_link = f'https://www.google.com/search?sca_esv=1ed5a24754748f85&sxsrf=AHTn8zo8SpuhsRD8V4mdHbpXO_WGW68nYQ:1744220546116&q={result}&tbm=shop&source=lnms&fbs=ABzOT_BYhiZpMrUAF0c9tORwPGlsASvANxUN_4u1oltdAlXXukJgrc8Sd9VQnu1m4CeFWCV1NFbj-Y0EivjyBcIM3oBQwXKIHetBIfJSp9D7p-3kxBrpagoTQLztGa6Nv5ZlDjulzpvQmDkY4VJEKHUsGoTOk5ZFfdzIyx0T9bFBg5uzqhjsmuJBmIIgKujST8BzF4iQUzzkQIdPbEd1BPOIHikxVCDFdA&ved=1t:200715&ictx=111&biw=1024&bih=687&dpr=1'
        driver.get(search_link)
        sleep(5)
        products = driver.find_elements(By.CSS_SELECTOR, "div.sh-dgr__grid-result")
        for i, produto in enumerate(products):
            try:
                titulo = produto.find_element(By.CSS_SELECTOR, "div.EI11Pd").text
            except:
                titulo = "Não encontrado"

            try:
                preco = produto.find_element(By.CSS_SELECTOR, "span.a8Pemb").text
            except:
                preco = "Não encontrado"

            try:
                loja = produto.find_element(By.CSS_SELECTOR, "div.aULzUe").text
            except:
                loja = "Não encontrado"

            try:
                link = produto.find_element(By.CSS_SELECTOR, "a.shntl").get_attribute("href")
            except:
                link = "Não encontrado"

            try:
                reviews = produto.find_element(By.CSS_SELECTOR, "span.QIrs8").text
            except:
                reviews = "Não encontrado"

            _product = {
                "titulo": titulo,
                "preco": preco,
                "loja": loja,
                "link": link,
                "reviews": reviews,
            }
            products_list.append(_product)

    finally:
        _total = f'Total de produtos raspados: {len(products_list)}'
        print(_total)
        driver.quit()
        return products_list


if __name__ == '__main__':
    _founded = google_search_engine()
    for product in _founded:
        try:
            preco_str = product.get('preco', '').replace("R$", "").replace(".", "").replace(",", ".").strip()
            product['preco_num'] = float(preco_str)
        except:
            product['preco_num'] = float('inf')

    _founded.sort(key=lambda x: x['preco_num'])

    ordem = 1
    for product in _founded:
        print(f"{ordem} - Título: {product.get('titulo')}")
        print(f"Preço: {product.get('preco')}")
        print(f"Reviews: {product.get('reviews')}")
        print(f"Loja:: {product.get('loja')}")
        print(f"URL: {product.get('link')}\n")
        ordem += 1

