from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
import pandas as pd

produto = input("DIGITE O PRODUTO SOBRE O QUAL DESEJA FAZER A ANALISE DE PREÇO: ")
navegador = webdriver.Chrome()

def inicializandoprograma():
    navegador.get("https://www.mercadolivre.com.br/")
    campo_de_pesquisa=navegador.find_element(By.ID, "cb1-edit")
    campo_de_pesquisa.send_keys(produto,Keys.ENTER)
def coletadedados():

    print("iniciando coleta de dados")

    produtos = navegador.find_elements(By.CLASS_NAME,"ui-search-result__wrapper")

    print(len(produtos))

    precoscodificados=[]
    nomescodificados=[]
    links=[]

    for produt in produtos:
        indicadoresdepreco = produt.find_element(By.CLASS_NAME, "poly-price__current")
        nomescodificados.append(produt.find_element(By.CLASS_NAME, "poly-component__title"))
        links.append(produt.find_element(By.CSS_SELECTOR, "andes-carousel-snapped__controls-wrapper").get_attribute("href"))
        precoscodificados.append(indicadoresdepreco.find_element(By.CLASS_NAME, "andes-money-amount__fraction"))
    
    precos = [precs.text for precs in precoscodificados]
    nomes = [noms.text for noms in nomescodificados]
    print(links)
        

inicializandoprograma()
coletadedados()

