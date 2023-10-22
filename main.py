from bs4 import BeautifulSoup
import requests
import sqlite3
import re

def Scrap_Nombre_Comunas(url):
    
    comunas = []
    
    Wikipedia = requests.get(url)

    if Wikipedia.status_code == 200:
        
        soup = BeautifulSoup(Wikipedia.text, 'html.parser')
        mapa_Region = soup.find('div', {'class': "nounderlines noresize"}) 
        
        for title in mapa_Region.find_all('a',title=True):
            comuna = title.text
            print(comuna)
            comunas.append(comuna)
        #print(comunas)
    else:
        print("No se pudo realizar conexion a Wikipedia - Comunas")

    return comunas

def Scrap_Coordenadas_Comunas(url):

    coordenadas = []

    Wikipedia = requests.get(url)

    if Wikipedia.status_code == 200:
        soup = BeautifulSoup(Wikipedia.text, 'html.parser')
        mapa_Region = soup.find('div', {'class': "nounderlines noresize"})
        
        enlaces = mapa_Region.find_all('a', href=True)

        for enlace in enlaces[1:]:
            url = ("https://es.wikipedia.org/" + enlace['href'])
            #print(url)
            
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
    return coordenadas
        
def Scrap_Poblacion_Comunas(url):

    poblacion_numeros = []

    Wikipedia = requests.get(url)

    if Wikipedia.status_code == 200:
        soup = BeautifulSoup(Wikipedia.text, 'html.parser')
        mapa_Region = soup.find('div', {'class': "nounderlines noresize"})
        
        enlaces = mapa_Region.find_all('a', href=True)

        for enlace in enlaces[1:]:
            url = ("https://es.wikipedia.org/" + enlace['href'])
            #print(url)
            
            #Ahora ingresamos a las url de cada ciudad para obtener sus coordenadas
            response_ciudad = requests.get(url)

            if response_ciudad.status_code == 200:

                ciudad = BeautifulSoup(response_ciudad.text, 'html.parser')
                
                tabla_poblacion = ciudad.find('table', class_='infobox')

                if tabla_poblacion:
                    
                    for fila in tabla_poblacion.find_all('tr'):

                                            
                        if 'hab.' in fila.text:
                            poblacion_text = fila.find('td').text.strip()

                            poblacion_sin_corchetes = re.sub(r'\[[0-9]+\]', '', poblacion_text)

                            poblacion_numero = ''.join(filter(str.isdigit, poblacion_sin_corchetes))
                            poblacion_numeros.append(poblacion_numero)
                            #print(poblacion_numero)
                    


            else:
                print("No se encontró un elemento <table> con clase 'infobox'.")
    return poblacion_numeros


def Alcaldes_Comuna(url):


    Comuna_alcalde = []
    Wikipedia = requests.get(url)
    
    if Wikipedia.status_code == 200:
        soup = BeautifulSoup(Wikipedia.text, 'html.parser')
        Alcaldes_tabla = soup.find('div', {'class': "wikitable"})
        print(Alcaldes_tabla)


    return Comuna_alcalde


if __name__ == "__main__":
    url = 'https://es.wikipedia.org/wiki/Regi%C3%B3n_de_Los_Lagos'
    Comunas       = Scrap_Nombre_Comunas(url) # LISTO SE HIZO SCRAP PARA OBTENER LAS COMUNAS
    Coordenadas   = Scrap_Coordenadas_Comunas(url) 
    Poblacion     = Scrap_Poblacion_Comunas(url)
    Alcaldes      = Alcaldes_Comuna(url)


    try:
        sqliteConnection = sqlite3.connect('C:\\Proyectos\\Beautiful\\coor.db')
        cursor = sqliteConnection.cursor()

        # Verificar si la tabla Comunas contiene datos
        cursor.execute("SELECT count(*) FROM Comunas")
        data_count = cursor.fetchone()[0]

        if data_count > 0:
            # Si hay datos, elimina los registros existentes en la tabla Comunas
            cursor.execute("DELETE FROM Comunas")
            print("Eliminando registros anteriores.")

        for i in range(len(Comunas)):
            nombre_comuna = Comunas[i]
            latitud, longitud = Coordenadas[i]
            poblacion = Poblacion[i]
            # Inserta el registro en la tabla 'Comunas'
            cursor.execute("INSERT INTO Comunas(Comuna, Latitud, Longitud, Poblacion) VALUES (?, ?, ?, ?)", (nombre_comuna, latitud, longitud,poblacion,))
        

        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error al insertar datos:", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


