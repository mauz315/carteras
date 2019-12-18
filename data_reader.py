from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from datetime import datetime
from cartera_methods import get_safs, get_fondos, get_cartera, click_buscar
#import xlsxwriter

def copy_table(driver):
    table = driver.find_element_by_id("grdResumen01")
    head = table.find_element_by_tag_name('th')
    body = table.find_element_by_tag_name('tbody')
    
    file_data = []
    file_header = []
    head_line = head.find_element_by_tag_name("tr")
    file_header = [header.text.encode("utf8") for header in head_line.find_elements_by_tag_name('th')]
    file_data.append(",".join(file_header))
    
    body_rows = body.find_elements_by_tag_name('tr')
    for row in body_rows:
        data = row.find_elements_by_tag_name('td')
        file_row = []
        for datum in data:
            datum_text = datum.text.encode('utf8')
            file_row.append(datum_text)
        file_data.append(",".join(file_row))
    print(file_data)
    
    
chromedriver = 'C:/Users/P900017/Documents/Chromedriver/chromedriver.exe'
#options = Options()
#options.add_argument("--ignore-certificate-errors")
#options.headless = True
#capabilities = DesiredCapabilities.CHROME.copy()
#capabilities['acceptSslCerts'] = True 
#capabilities['acceptInsecureCerts'] = True

url = "https://www.smv.gob.pe/Frm_ResumenValorizacionCartera?data=59C6C53987D41333DC7375CD83EBB8CA01B1BF5776"

# browser = webdriver.Chrome(chromedriver, options=options, desired_capabilities=capabilities)
browser = webdriver.Chrome(chromedriver)
browser.maximize_window()
browser.get(url)

# Obteniendo lista de SAFs

SAF_lista = get_safs(browser)

####################################################### Lista total de fondos
#prnt = {}
#for saf in SAF_lista:
#    SAF_search = browser.find_element_by_id("MainContent_TextBox1")
#    SAF_search.send_keys(saf + Keys.RETURN)
#    time.sleep(3)
#    fondos_lista = []
#    Fondos = Select(browser.find_element_by_id("MainContent_cboFondo"))
#    for fondo in Fondos.options:
#        fondos_lista.append(fondo.text)
#    prnt.update([(saf, fondos_lista[1:])])
#    
#workbook = xlsxwriter.Workbook('data.xlsx')
#worksheet = workbook.add_worksheet()
#row = 0
#col = 0
#
#for key in prnt.keys():
#    row += 1
#    worksheet.write(row, col, key)
#    for item in prnt[key]:
#        worksheet.write(row, col + 1, item)
#        row += 1
#
#workbook.close()
####################################################### Lista total de fondos

SAF_search = browser.find_element_by_id("MainContent_TextBox1")

SAF_search.send_keys(SAF_lista[1] + Keys.RETURN)
time.sleep(2)
fondos_lista = []
Fondos = Select(browser.find_element_by_id("MainContent_cboFondo"))
for fondo in Fondos.options:
    fondos_lista.append(fondo.text)
    
Fondos.select_by_visible_text(fondos_lista[6])
time.sleep(2)

# Seleccionando año y mes
cartera_hist = []
for yr in ["2019"]:
    Year = Select(browser.find_element_by_id("MainContent_lisAnio"))
    Year.select_by_visible_text(yr)
    time.sleep(2)
    # get_months listo para iteración
    for mnth in [1]:
        Month = Select(browser.find_element_by_id("MainContent_lisMes"))
        Month.select_by_index(mnth)
        click_buscar(browser)
        # Falta implementar un loop para el botón de cada asset class!!!
        boton_detalle = browser.find_element_by_id("MainContent_gdrResumenValorizacion_HyperLink1_2")
        # Obteniendo tabla de composición de cartera
        hold_df = get_cartera(browser, boton_detalle)
        cartera_hist.append(hold_df)
        hold_df.to_csv('cartera_test.csv')

#########
#for i in range(0,100):
#    try:
#        element = browser.find_element_by_id(empresa_id + str(i))
#        print(element.text)
#    except:
#        pass
#
#browser.quit()
#a = currentHoldings.find_element_by_xpath("//th[@data-field='current_ranking']/div[1]")
#a.click()
# browser.find_element_by_xpath("//button[@type'submit']").click()
# for i, df in enumerate(pd.read_html(url)):
# df.to_csv('myfile_%s.csv' % i)
# html = browser.get("").content
# df_list = pd.read_html(html)
# df = df_list[-1]
# print(df)
