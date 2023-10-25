from bs4 import BeautifulSoup
import pandas as pd
import requests
import sqlite3
import re

#hacemos la solicitud para que ingrese a este html
link_wikipedia = requests.get('https://es.wikipedia.org/wiki/Regi%C3%B3n_de_Los_Lagos')

if link_wikipedia.status_code == 200:

    soup = BeautifulSoup(link_wikipedia.text, 'html.parser')
    region = soup.find('div', {'class': "nounderlines noresize"})
    
    comunas = []

    for title in region.find_all('a',title=True):
        comuna = title.text
        print(comuna)
        comunas.append(comuna)

    
    #Prueba con solo un enlace para ver la forma de reedireccionamiento.
    enlaces = region.find_all('a', href=True)

    
    coordenadas = []
    poblacion_numeros = []
    #Tomamos los links en cada href y le añadimos la pag de wikipedia oficial

    for enlace in enlaces[1:]:

        url = ("https://es.wikipedia.org/" + enlace['href'])
        
        #Ahora ingresamos a las url de cada ciudad para obtener sus coordenadas
        response_ciudad = requests.get(url)



        if response_ciudad.status_code == 200:

            ciudad = BeautifulSoup(response_ciudad.text, 'html.parser')
            
            span_geo = ciudad.find('span', class_='geo')

            if span_geo:

                span_latitude = span_geo.find('span', class_='latitude')

                span_longitude = span_geo.find('span', class_='longitude')
                
                if span_latitude and span_longitude:
                    
                    #Tomamos lo valores de cada atributo latitud y longitud ademas borramos los espacios(strip) y los elementos rstrip que tiene una COMA
                    latitud = span_latitude.text.strip().rstrip(',')
                    longitud = span_longitude.text.strip().rstrip(',')
                    #print("Latitud:", latitud)
                    #print("Longitud:", longitud)

                    coordenada = (latitud, longitud)
                    coordenadas.append(coordenada)
                    #print(coordenada)
                    

                else:
                    print("No se encontraron los elementos <span> con clases 'latitude' y 'longitude' dentro de <span> con clase 'geo'.")
            else:
                print("No se encontró un elemento <span> con clase 'geo'.")
            

            tabla_poblacion = ciudad.find('table', class_='infobox')

            if tabla_poblacion:
                
                for fila in tabla_poblacion.find_all('tr'):

                                        
                    if 'hab.' in fila.text:
                        poblacion_text = fila.find('td').text.strip()

                        poblacion_sin_corchetes = re.sub(r'\[[0-9]+\]', '', poblacion_text)

                        poblacion_numero = ''.join(filter(str.isdigit, poblacion_sin_corchetes))
                        poblacion_numeros.append(poblacion_numero)
                        

                    


            else:
                print("No se encontró un elemento <table> con clase 'infobox'.")

        else:
            print("No se pudo acceder a los enlaces en el mapa.")
    print(coordenadas)

else:
    print("No se pudo acceder a Wikipedia")



#Alcaldes
df_pandas=pd.read_html('https://es.wikipedia.org/wiki/Regi%C3%B3n_de_Los_Lagos', attrs = {'class': 'wikitable'})[0]
alcaldes = df_pandas["Alcalde"].tolist() + df_pandas["Alcalde.1"].tolist()



data = list(zip(comunas, coordenadas, poblacion_numeros))
data.sort(key=lambda x: x[0])

try:
    sqliteConnection = sqlite3.connect('C:\\Proyectos\\BeautifulSoup_Region_Lagos\\coor.db')
    cursor = sqliteConnection.cursor()

    # Verificar si la tabla Comunas contiene datos
    cursor.execute("SELECT count(*) FROM Comunas")
    data_count = cursor.fetchone()[0]

    if data_count > 0:
        # Si hay datos, elimina los registros existentes en la tabla Comunas
        cursor.execute("DELETE FROM Comunas")
        print("Eliminando registros anteriores.")

    
    for i in range(len(comunas)):
        nombrecomuna, (latitud, longitud), poblacion = data[i]
        alcalde = alcaldes[i]
        cursor.execute("INSERT INTO Comunas(Comuna, Latitud, Longitud, Poblacion, Alcaldes) VALUES (?, ?, ?, ?, ?)",
                       (nombrecomuna, latitud, longitud, poblacion, alcalde))


    sqliteConnection.commit()
    cursor.close()

except sqlite3.Error as error:
    print("Error al insertar datos:", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()




   