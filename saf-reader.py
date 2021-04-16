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
from cartera_methods import get_cartera, get_fondos, click_buscar, id_cartera, get_months, excel_sh_name, get_resumen
#import joblib

# Archivo para cargar fondos, meses particulares, solo resumenes, pruebas

#cartera_cons = joblib.load('data/cartera_dict.sav')

peer_group = pd.read_csv('input/peer_group.csv', sep=',', index_col= 'saf_name', encoding = "latin1")
target_safs = list(peer_group.index.unique())

chromedriver = 'C:/Users/P900017/Documents/Chromedriver/chromedriver.exe'
url = "https://www.smv.gob.pe/Frm_ResumenValorizacionCartera?data=59C6C53987D41333DC7375CD83EBB8CA01B1BF5776"

browser = webdriver.Chrome(chromedriver)
browser.maximize_window()
browser.get(url)

#SAF_search.send_keys(SAF_lista[8] + Keys.RETURN)
#time.sleep(2)
#fondos_lista = []
#Fondos = Select(browser.find_element_by_id("MainContent_cboFondo"))
#for fondo in Fondos.options:
#    fondos_lista.append(fondo.text)
#
#Fondos = Select(browser.find_element_by_id("MainContent_cboFondo"))
#time.sleep(2)
#Fondos.select_by_visible_text(fondos_lista[24])
# 16: SURA ACCIONES
# 24: RENTA DÓLARES
time.sleep(3)
resumen_cons = {}
for saf in target_safs[1:]: #[1:]
    try:
        SAF_search = browser.find_element_by_id("MainContent_TextBox1")
        SAF_search.send_keys(saf + Keys.RETURN)        
        time.sleep(3)
        target_fondos = get_fondos(peer_group, saf) #Returns a list
        print('Exportando SAF: ' + saf + '...')
        for t_fondo in target_fondos:
            Fondos = Select(browser.find_element_by_id("MainContent_cboFondo"))
            time.sleep(3)
            Fondos.select_by_visible_text(t_fondo)
            time.sleep(4)
            print('Exportando fondo [' + str(target_fondos.index(t_fondo)+1) + '/' + str(len(target_fondos)) + ']:')
            print(t_fondo)
            for yr in ["2019"]:
                Year = Select(browser.find_element_by_id("MainContent_lisAnio"))
                try:
                    Year.select_by_visible_text(yr)
                    time.sleep(4)
                    # get_months listo para iteración
                    for mon in [2,3]:
                        Month = Select(browser.find_element_by_id("MainContent_lisMes"))
                        try:
                            Month.select_by_index(mon)
                            time.sleep(2)
                            click_buscar(browser)
                            time.sleep(2)
                            tabla_resumen = id_cartera(get_resumen(browser), saf, t_fondo, yr, get_months(mon))
                            try:
                                resumen_cons['Resumen'] = pd.concat([resumen_cons['Resumen'].copy(), tabla_resumen.copy()])
                            except:
                                resumen_cons['Resumen'] = tabla_resumen.copy()
#                            for r in range(0, len(filas_tabla)):
#                                asset_class = filas_tabla[r].text
#                                boton_detalle = browser.find_element_by_id("MainContent_gdrResumenValorizacion_HyperLink1_" + str(r))
#                            # Obteniendo tabla de composición de cartera
#                                hold_df = get_cartera(browser, boton_detalle)
#                                id_cartera(hold_df, 'SAF', yr, mon)
                        except:
                            print('Error en ' + str(get_months(mon)) + '/' + yr)
#                            error_log.append('Error: ' + str(get_months(mon)) + '/' + yr + ' ' + t_fondo)
                            pass
                    print('Finalizado ' + yr)
                except:
#                    error_log.append('Error: Full ' + yr + ' ' + t_fondo)
                    pass
    except:
        print('Error en ' + saf + '!')
#        error_log.append('Error iniciando ' + saf)
        pass            
             
# Save cartera_cons to excel
#cart_keys = list(cartera_cons.keys())
#sheet_names = excel_sh_name(cart_keys)
with pd.ExcelWriter('resumenes.xlsx') as writer:  # doctest: +SKIP
    dummydf = resumen_cons['Resumen']
    for col in dummydf.columns:
        try:
            dummydf[col] = dummydf[col].astype(float)
        except:
            pass
    dummydf.to_excel(writer, sheet_name='Resumen', index=False)

# hold_df.to_csv('cartera_test.csv') ### PRUEBA    
#t = browser.find_element_by_xpath("//div[@id='MainContent_gdrResumenValorizacion']/tr[" + str(r + 1) + "]")
#xpath("//th[@data-field='current_ranking']/div[1]")
   

# Asset class cartera test

#boton_detalle = browser.find_element_by_id("MainContent_gdrResumenValorizacion_HyperLink1_0")
#cartera_url = boton_detalle.get_attribute('href')
#WindowHandler = browser.current_window_handle
#browser.execute_script("window.open('');")
#time.sleep(4)
#browser.switch_to.window(browser.window_handles[1])
#browser.get(cartera_url)            
#time.sleep(2)
#
#holdings = browser.find_element_by_xpath("//table[@class='contenedor_centrado']/tbody/tr[3]")
#hold_df = pd.read_html(holdings.get_attribute('outerHTML'))[0]
#if 'Unnamed: 2' in list(hold_df.columns):
#    hold_df = hold_df.rename(columns=hold_df.iloc[0]).drop(hold_df.index[0])
#hold_df.dropna(thresh=len(hold_df.columns)*2/3, inplace=True)
#print(hold_df)
#browser.close() #closes new tab
#browser.switch_to_window(WindowHandler)
