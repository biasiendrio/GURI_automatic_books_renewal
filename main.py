from selenium import webdriver
import sys, argparse, os
import warnings, time
from sistema_guri import sistemaGURI
warnings.filterwarnings("ignore")

ap = argparse.ArgumentParser()
ap.add_argument("-l", "--login", required=True, help="Número de matrícula")
ap.add_argument("-s", "--senha", required=True, help="Senha institucional")
ap.add_argument("-so", "--sis_operacional", type=int, default=0, help="Sistema operacional da maquina (64 bits) default Linux. 1 - Windows; 2 - Mac")
ap.add_argument("-v", "--visualizar", type=bool, default=False, help="True para visualizar a renovação")

args = vars(ap.parse_args())

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
    sistemaGURI(browser, args["login"], args["senha"]).run()


if __name__ == '__main__':
    main()
    os.system("rm ghostdriver.log")
    