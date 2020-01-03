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

def get_safs(browser):
    
    SAF = Select(browser.find_element_by_id("MainContent_cboDenominacionSocial"))
    SAF_lista =[]
    for opt in SAF.options:
        SAF_lista.append(opt.text)
    return SAF_lista[1:]

def get_fondos(peer_group, saf):
    
    fondos = peer_group['fondo_name'].loc[saf]
    if isinstance(fondos, str):
        target_fondos = []
        target_fondos.append(fondos)
        return target_fondos
    else:
        return list(fondos)
    
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
    if 'Unnamed: 2' in list(hold_df.columns):
        hold_df = hold_df.rename(columns=hold_df.iloc[0]).drop(hold_df.index[0])
    hold_df.dropna(thresh=len(hold_df.columns)*2/3, inplace=True)
    browser.close() #closes new tab
    time.sleep(1)
    browser.switch_to_window(WindowHandler)
    return hold_df

def id_cartera(df, saf, fondo, yr, mon):
    df['SAF'] = saf
    df['Año'] = yr
    df['Mes'] = mon
    df['Fondo'] = fondo
    cols = df.columns.tolist()
    cols = cols[-4:] + cols[:-4]
    return df[cols]
#    df['Asset_class'] = ac

def text_search(browser, boton_detalle, fondo, yr, mnth):
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

def get_months(m):
    mnts = list(range(1,13))
    mon_base = {}
    for i in range(0,12):
        mon_base[mnts[i]] = mnts[-i-1]
    
    return mon_base[m]

def excel_sh_name(keys):
    names = []
    for key in keys:
        k = key.replace('/', '-')
        if len(key)> 30:
            names.append(k[:30])
        else:
            names.append(k)
    
    return names

#def cod_saf(SAF_lista):
#    for saf in 
#    
#    return SAF_cod
     
    