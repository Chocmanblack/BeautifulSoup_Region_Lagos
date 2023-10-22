import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://es.wikipedia.org/wiki/Regi%C3%B3n_de_Los_Lagos"

df_pandas=pd.read_html(url, attrs = {'class': 'wikitable'})[0]
#print(df_pandas)
print(df_pandas["Alcalde"])
print(df_pandas["Alcalde.1"])