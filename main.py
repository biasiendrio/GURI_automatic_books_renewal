from selenium import webdriver
import sys, argparse, os
import warnings, time
warnings.filterwarnings("ignore")

ap = argparse.ArgumentParser()
ap.add_argument("-l", "--login", required=True, help="Número de matrícula")
ap.add_argument("-s", "--senha", required=True, help="Senha institucional")
ap.add_argument("-so", "--sis_operacional", type=int, default=0, help="Sistema operacional da maquina (64 bits) default Linux. 1 - Windows; 2 - Mac")
ap.add_argument("-v", "--visualizar", type=bool, default=False, help="True para visualizar a renovação")
args = vars(ap.parse_args())


class Renovador:
    def __init__(self, browser):
        self.browser = browser
        self.login = args["login"]
        self.senha = args["senha"]
    
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

def main():
    if args["visualizar"]:
        browser = webdriver.Chrome("web_drivers/chromedriver")
    else:
        if args["sis_operacional"] == 0:
            browser = webdriver.PhantomJS("web_drivers/phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
        elif args["sis_operacional"] == 1:
            browser = webdriver.PhantomJS("web_drivers/phantomjs-2.1.1-windows/bin/phantomjs.exe")
        elif args["sis_operacional"] == 2:
            browser = webdriver.PhantomJS("web_drivers/phantomjs-2.1.1-macosx/bin/phantomjs")
        else:
            print("Sistema operacional deve ser 0, 1 ou 2")
            sys.exit()
    
    browser.get("https://guri.unipampa.edu.br/ptl/sistema/showLogin")
    Renovador(browser).run()

if __name__ == '__main__':
    main()
    os.system("rm ghostdriver.log")
    print("Livros renovados")