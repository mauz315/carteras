# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 15:12:36 2019

@author: P900017
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
#from datetime import datetime
from cartera_methods import get_safs, get_cartera, click_buscar, id_cartera, get_months, excel_sh_name

# Importando peer group

peer_group = pd.read_csv('peer_group.csv', sep=',', index_col= 'saf_name', encoding = "latin1")
target_safs = list(peer_group.index.unique())

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

cartera_cons = {} # Cartera consolidada, cada key es un asset class
for saf in target_safs[1:]:
    SAF_search = browser.find_element_by_id("MainContent_TextBox1")
    SAF_search.send_keys(saf + Keys.RETURN)        
    time.sleep(2)
    target_fondos = peer_group['fondo_name'].loc[saf]
    print('Exportando SAF: ' + saf + '...')
    for t_fondo in target_fondos:
        Fondos = Select(browser.find_element_by_id("MainContent_cboFondo"))
        # for fondo in Fondos.options:
        #    fondos_lista.append(fondo.text)
        time.sleep(2)
        Fondos.select_by_visible_text(t_fondo)
        time.sleep(3)
        print('Exportando fondo: ' + t_fondo + '...')
        for yr in ["2019"]:
            Year = Select(browser.find_element_by_id("MainContent_lisAnio"))
            try:
                Year.select_by_visible_text(yr)
                time.sleep(3)
                # get_months listo para iteración
                for mon in [2]: ### range(1:13)
                    Month = Select(browser.find_element_by_id("MainContent_lisMes"))
                    try:
                        Month.select_by_index(mon)
                        click_buscar(browser)
                        # Falta implementar un loop para el botón de cada asset class!!! #######
                        filas_tabla = browser.find_elements_by_xpath("//tr[@class='item-grid']/td[1]")
                        for r in range(0, len(filas_tabla)):
                            asset_class = filas_tabla[r].text
                            boton_detalle = browser.find_element_by_id("MainContent_gdrResumenValorizacion_HyperLink1_" + str(r))
                        # Obteniendo tabla de composición de cartera
                            hold_df = get_cartera(browser, boton_detalle)
                            id_cartera(hold_df, saf, t_fondo, yr, get_months(mon))
                            try:
                                cartera_cons[asset_class] = pd.concat([cartera_cons[asset_class].copy(), hold_df.copy()])
                            except:
                                cartera_cons[asset_class] = hold_df.copy()
        
                    except:
                        print('Error en ' + str(get_months(mon)) + '/' + yr + '!!!')
                        pass
                print('Exportación ' + yr + ' exitosa')
            except:
                pass

# Save cartera_cons to excel
cart_keys = list(cartera_cons.keys())
sheet_names = excel_sh_name(cart_keys)
with pd.ExcelWriter('carteras.xlsx') as writer:  # doctest: +SKIP
    for i in range(0,len(sheet_names)):
        dummydf = cartera_cons[cart_keys[i]].copy()
        for col in dummydf.columns:
            try:
                dummydf[col] = dummydf[col].astype(float)
            except:
                pass
            
        dummydf.to_excel(writer, sheet_name=sheet_names[i], index=False)

#NoSuchElementException:

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
