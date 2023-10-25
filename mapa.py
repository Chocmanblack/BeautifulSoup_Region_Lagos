# Integrantes: Leonardo Acum

from flask import Flask
import folium
import sqlite3

app = Flask(__name__)

Region_de_los_Lagos = (-42.00897942011642, -72.95094152292147)

server='localhost'

@app.route("/")
def base():
    # this is base map
    map = folium.Map(
        location=Region_de_los_Lagos,
        zoom_start=8
    )
    
    try:
        sqliteConnection = sqlite3.connect('C:\\Proyectos\\BeautifulSoup_Region_Lagos\\coor.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT Comuna, latitud, longitud, Poblacion, Alcaldes FROM Comunas;"""
    
        cursor.execute(sqlite_select_query)
    
        items = cursor.fetchall()

        max_poblacion = max(item[3] for item in items)
        min_poblacion = min(item[3] for item in items)
        
        for item in items:
            poblacion_radius = (item[3] - min_poblacion) / (max_poblacion - min_poblacion)
            radius = 2000 + int(poblacion_radius * 4000)  # Ajusta el rango de tamaño deseado
            
            '''
            folium.Marker(
                location=(item[1],item[2]),
                tooltip=item[0],
                
            ).add_to(map)
            '''
            folium.Circle(
                
                location=(item[1],item[2]),
                radius=radius,
                color="black",
                fill_opacity=0.2,
                opacity=0.7,
                fill_color="orange",
                fill=False,  # gets overridden by fill_color
                popup=' <h4><b><u>Comuna</u>: <b>{}</h4> <br> <h4><b><u>Habitantes</u>: <b>{}</h4> <br><h4><b><u> Alcalde</u>:</b> {}</h4>'.format(item[0],item[3],item[4]),
                tooltip='<h3><b> Comuna:</b> {} </3>' .format(item[0]),
            ).add_to(map)


        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
    return map._repr_html_()


if __name__ == "__main__":
    app.run(debug=True, host=server)
