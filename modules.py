from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import os
import streamlit as st
import pandas as pd
import plotly.express as px

from datetime import datetime
import time
import sqlite3


CLEANED_DATA_FOLDER = "data/data_clean"

@st.cache_data(ttl=300)
def load_cleaned_data(filename):
    """Charge un fichier CSV nettoyé depuis data/data_clean/"""
    filepath = f"data/data_clean/{filename}"
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    return None

def get_cleaned_files():
    """Récupère la liste des fichiers CSV nettoyés"""
    if os.path.exists(CLEANED_DATA_FOLDER):
        files = [f for f in os.listdir(CLEANED_DATA_FOLDER) if f.endswith('_cleaned.csv')]
        return files
    return []



def init_db():
    """Initialise la structure de la BDD"""
    conn = sqlite3.connect('data_collector.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scraped_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            nom TEXT,
            prix TEXT,
            adresse TEXT,
            url_image TEXT,
            date_scraped TIMESTAMP,
            page_number INTEGER
        )
    ''')
    conn.commit()
    conn.close()



def clear_db():
    """Vide complètement la table scraped_data"""
    conn = sqlite3.connect('data_collector.db', check_same_thread=False)
    try:
        conn.execute("DELETE FROM scraped_data")
        conn.commit()
    finally:
        conn.close()


def save_to_db(df, category, page_number):
    """Sauvegarde un DataFrame dans la BDD (après vidage préalable)"""
    df_copy = df.copy()
    df_copy['category'] = category
    df_copy['date_scraped'] = datetime.now()
    df_copy['page_number'] = page_number
    
    cols_to_keep = ['category', 'nom', 'prix', 'adresse', 'url_image', 'date_scraped', 'page_number']
    cols_available = [c for c in cols_to_keep if c in df_copy.columns]
    df_clean = df_copy[cols_available]
    
    conn = sqlite3.connect('data_collector.db', check_same_thread=False)
    try:
        df_clean.to_sql('scraped_data', conn, if_exists='append', index=False)
        conn.commit()
    finally:
        conn.close()


@st.cache_data(ttl=300)
def load_scraped_data():
    """Charge les données scrapées depuis la BDD"""
    init_db()
    conn = sqlite3.connect('data_collector.db', check_same_thread=False)
    try:
        df = pd.read_sql_query("SELECT * FROM scraped_data", conn)
        return df
    finally:
        conn.close()


# -------- Chargement des fichier csv
@st.cache_data(ttl=300)
def load_existing_data(filename):
    filepath = f"data/{filename}"
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    return None

def get_available_files():
    """Récupère la liste des fichiers CSV dans le dossier data/"""
    data_folder = "data"
    if os.path.exists(data_folder):
        files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]
        return files
    return []

# -------- Scraping des données 
def scrape_category(base_url, category_name, num_pages, progress_bar, status_text):
    """Fonction de scraping avec Selenium"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    all_data = []
    
    try:
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)
        
        for page in range(1, num_pages + 1):
            url = f"{base_url}?page={page}"
            status_text.text(f"{category_name} | Page {page}/{num_pages}")
            
            try:
                driver.get(url)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.ad__card')))
                containers = driver.find_elements(By.CSS_SELECTOR, '.ad__card')
                
                for container in containers:
                    def safe_find(selector, attr='text'):
                        try:
                            elem = container.find_element(By.CSS_SELECTOR, selector)
                            return elem.get_attribute('src') if attr == 'src' else elem.text
                        except:
                            return "N/A"
                    
                    all_data.append({
                        "nom": safe_find('.ad__card-description'),
                        "prix": safe_find('.ad__card-price'),
                        "adresse": safe_find('.ad__card-location span'),
                        "url_image": safe_find('img.ad__card-img', attr='src')
                    })
                
                progress_bar.progress(page / num_pages)
                time.sleep(2)
                
            except TimeoutException:
                status_text.text(f"Timeout page {page}")
                continue
            except Exception as e:
                status_text.text(f"Erreur page {page}")
                continue
        
        return pd.DataFrame(all_data)
        
    finally:
        driver.quit()