from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.chrome.options import Options
import pandas as pd

produto = input("DIGITE O PRODUTO SOBRE O QUAL DESEJA FAZER A ANALISE DE PREÇO: ")
Options().add_argument("--headless")
navegador = webdriver.Chrome()

def inicializandoprograma():

    navegador.get("https://www.mercadolivre.com.br/")
    campo_de_pesquisa=navegador.find_element(By.ID, "cb1-edit")
    campo_de_pesquisa.send_keys(produto,Keys.ENTER)   
def coleta_e_processamento_de_dados():

    print("\033[34mINICIANDO COLETA DE DADOS\033[0m")

    WDW(navegador, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"ui-search-result__wrapper")))
    produtos = navegador.find_elements(By.CLASS_NAME,"ui-search-result__wrapper")

    precoscodificados=[]
    nomescodificados=[]
    links=[]

    for produt in produtos:
        indicadoresdepreco = produt.find_element(By.CLASS_NAME, "poly-price__current")
        links.append(produt.find_element(By.CSS_SELECTOR, "a.poly-component__title").get_attribute("href"))
        nomescodificados.append(produt.find_element(By.CLASS_NAME, "poly-component__title"))
        precoscodificados.append(indicadoresdepreco.find_element(By.CLASS_NAME, "andes-money-amount__fraction"))
   
    print("\033[32mCOLETA DE DADOS CONCLUÍDA\033[0m")

    navegador.quit

    print("\033[34mPROCESSANDO DADOS\033[0m")

    precos = [precs.text for precs in precoscodificados]
    precos=[float(x) for x in precos]
    nomes = [noms.text for noms in nomescodificados]

    dados={
        
        "PRODUTOS":nomes,
        "PREÇOS":precos,
        "LINKS":links
    }
    return dados
def criaçãodaplanilha():
    planilha=pd.DataFrame(coleta_e_processamento_de_dados())
    print("\033[34mCRIANDO PLANILHA\033[0m")
    planilhaordenada=planilha.sort_values("PREÇOS").reset_index(drop=True)
    planilhaordenada.to_excel("PREÇOS_DO_PRODUTO_"+produto+".xlsx", index=False)
    print("\033[32mPLANILHA CRIADA COM SUCESSO\033[0m")
inicializandoprograma()
criaçãodaplanilha()
