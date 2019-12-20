# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 15:12:36 2019

@author: P900017
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from datetime import datetime

def get_safs(browser):
    
    SAF = Select(browser.find_element_by_id("MainContent_cboDenominacionSocial"))
    SAF_lista =[]
    for opt in SAF.options:
        SAF_lista.append(opt.text)
    return SAF_lista[1:]

def get_fondos(browser, SAF_lista):
    
    SAF_search = browser.find_element_by_id("MainContent_TextBox1")
    SAF_search.send_keys(SAF_lista[8])
    SAF_search.send_keys(Keys.RETURN)
    time.sleep(2)
    fondos_lista = []
    Fondos = Select(browser.find_element_by_id("MainContent_cboFondo"))
    for fondo in Fondos.options:
        fondos_lista.append(fondo.text)
    return fondos_lista[1:]

def get_date(browser, yr, mth):
    
    Year = Select(browser.find_element_by_id("MainContent_lisAnio"))
    for i in [1,2,3]:
        Year.select_by_index(i)
        time.sleep(2)

    Month = Select(browser.find_element_by_id("MainContent_lisMes"))
    Month.select_by_index(mth)
    
def click_buscar(browser):
    
    time.sleep(2)
    browser.find_element_by_id("MainContent_btnBuscar").click()
    time.sleep(2)    

def get_cartera(browser, boton_detalle):

    cartera_url = boton_detalle.get_attribute('href')
    WindowHandler = browser.current_window_handle
    browser.execute_script("window.open('');")
    time.sleep(4)
    browser.switch_to.window(browser.window_handles[1])
    browser.get(cartera_url)            
    time.sleep(2)
    holdings = browser.find_element_by_xpath("//table[@class='contenedor_centrado']/tbody/tr[3]")
    hold_df = pd.read_html(holdings.get_attribute('outerHTML'))[0]
    browser.close() #closes new tab
    time.sleep(1)
    browser.switch_to_window(WindowHandler)
    return hold_df

def id_cartera(df, saf, yr, mon):
    df['SAF'] = saf
    df['Año'] = yr
    df['Mes'] = mon

def get_cartera_text(browser, boton_detalle, fondo, yr, mnth):
    cartera_url = boton_detalle.get_attribute('href')
    WindowHandler = browser.current_window_handle
    browser.execute_script("window.open('');")
    time.sleep(4)
    browser.switch_to.window(browser.window_handles[1])
    browser.get(cartera_url)            
    time.sleep(2)
    #
    # PULIR SELECCION DE ID de TABLA (cambia para cada asset class)
    #
    if 'CENTENARIO' in browser.page_source:
        print ('Centenario en ' + fondo + ' ' + yr + ' ' + mnth)
    browser.close() #closes new tab
    time.sleep(1)
    browser.switch_to_window(WindowHandler)

def get_months(i):
    mon_base = ['DICIEMBRE', 'NOVIEMBRE', 'OCTUBRE',
                'SEPTIEMBRE', 'AGOSTO', 'JULIO', 'JUNIO',
                'MAYO', 'ABRIL', 'MARZO', 'FEBRERO', 'ENERO']
    mon_base.reverse()
    if int(i) == datetime.now().year:
        act_mon = datetime.now().month - 2 # delay de 3 meses + 1 de index
        return mon_base[0:act_mon]
    else:
        return mon_base

#def cod_saf(SAF_lista):
#    for saf in 
#    
#    return SAF_cod
     
    