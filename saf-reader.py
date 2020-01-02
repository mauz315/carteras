# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 08:40:41 2020

@author: P900017
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
from cartera_methods import get_safs, get_fondos, get_cartera, click_buscar, id_cartera, excel_sh_name


# Testing methods

chromedriver = 'C:/Users/P900017/Documents/Chromedriver/chromedriver.exe'
url = "https://www.smv.gob.pe/Frm_ResumenValorizacionCartera?data=59C6C53987D41333DC7375CD83EBB8CA01B1BF5776"

browser = webdriver.Chrome(chromedriver)
browser.maximize_window()
browser.get(url)

SAF_lista = get_safs(browser)

SAF_search = browser.find_element_by_id("MainContent_TextBox1")

SAF_search.send_keys(SAF_lista[8] + Keys.RETURN)
time.sleep(2)
fondos_lista = []
Fondos = Select(browser.find_element_by_id("MainContent_cboFondo"))
for fondo in Fondos.options:
    fondos_lista.append(fondo.text)

Fondos = Select(browser.find_element_by_id("MainContent_cboFondo"))
time.sleep(2)
Fondos.select_by_visible_text(fondos_lista[24])
# 16: SURA ACCIONES
# 24: RENTA DÓLARES
time.sleep(3)
cartera_cons = {} # Cartera consolidada, cada key es un asset class

for yr in ["2019","2018"]:
    Year = Select(browser.find_element_by_id("MainContent_lisAnio"))
    try:
        Year.select_by_visible_text(yr)
        time.sleep(3)
        # get_months listo para iteración
        for mon in [2]:
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
                    id_cartera(hold_df, 'SAF', yr, mon)
                    try:
                        cartera_cons[asset_class] = pd.concat([cartera_cons[asset_class].copy(), hold_df.copy()])
                    except:
                        cartera_cons[asset_class] = hold_df.copy()

            except:
                pass
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

# hold_df.to_csv('cartera_test.csv') ### PRUEBA    
#t = browser.find_element_by_xpath("//div[@id='MainContent_gdrResumenValorizacion']/tr[" + str(r + 1) + "]")
#xpath("//th[@data-field='current_ranking']/div[1]")
   

# Asset class cartera test

boton_detalle = browser.find_element_by_id("MainContent_gdrResumenValorizacion_HyperLink1_0")
cartera_url = boton_detalle.get_attribute('href')
WindowHandler = browser.current_window_handle
browser.execute_script("window.open('');")
time.sleep(4)
browser.switch_to.window(browser.window_handles[1])
browser.get(cartera_url)            
time.sleep(2)

holdings = browser.find_element_by_xpath("//table[@class='contenedor_centrado']/tbody/tr[3]")
hold_df = pd.read_html(holdings.get_attribute('outerHTML'))[0]
if 'Unnamed: 2' in list(hold_df.columns):
    hold_df = hold_df.rename(columns=hold_df.iloc[0]).drop(hold_df.index[0])
hold_df.dropna(thresh=len(hold_df.columns)*2/3, inplace=True)
print(hold_df)
browser.close() #closes new tab
browser.switch_to_window(WindowHandler)
