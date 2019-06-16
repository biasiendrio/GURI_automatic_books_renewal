from selenium import webdriver
import time


class sistemaGURI:
    def __init__(self, browser, login, senha):
        self.browser = browser
        self.login = login
        self.senha = senha
    
    def run(self):
        self.realiza_login()
        self.seleciona_livros()
        self.renova_livros()
    
    # realiza login na pagina do GURI
    def realiza_login(self):
        login = self.browser.find_element_by_id('login')
        login.send_keys(self.login)

        password = self.browser.find_element_by_id('senha')
        password.send_keys(self.senha)

        entrar = self.browser.find_element_by_id('entrar')
        entrar.click()
    
    # seleciona livros a serem renovados e os que atingiram o limite de renovacoes
    def seleciona_livros(self):
        time.sleep(1)
        self.browser.get("https://guri.unipampa.edu.br/bib/biblioteca/consultarSituacao/")

        itens_tabela = self.browser.find_elements_by_css_selector("td")
        para_renovar = self.browser.find_elements_by_css_selector("input.chkEmprestimo")

        livros = []
        for iten in itens_tabela:
            if iten.text != "":
                livros.append(iten.text)

        livros = livros[9:]

        for nome, vancimento, renovar in zip(range(0,len(itens_tabela),6), range(4,len(itens_tabela),6), para_renovar):
            if livros[vancimento][0] != '10':
                renovar.click()
            else:
                print(f"DEVOLVER: {livros[nome][:-2]}")
    
    # renovar livros selecionados
    def renova_livros(self):
        renovar = self.browser.find_element_by_css_selector("span.button_text")
        renovar.click()
        print("Livros renovados")