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
        sqliteConnection = sqlite3.connect('C:\\Proyectos\\Beautiful\\coor.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT Comuna, latitud, longitud, Poblacion FROM Comunas;"""
    
        cursor.execute(sqlite_select_query)
    
        items = cursor.fetchall()

        
        
        for item in items:

            valor = item[3]
            folium.Marker(
                location=(item[1],item[2]),
                tooltip=item[0],
                
            ).add_to(map)
            folium.Circle(
                
                location=(item[1],item[2]),
                radius=(valor / 10),
                color="black",
                fill_opacity=0.5,
                opacity=1,
                fill_color="orange",
                fill=False,  # gets overridden by fill_color
                popup=' <h3> {} habitantes.</h3>'.format(item[3]),
                tooltip=item[0],
            ).add_to(map)


        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
            if (sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
    return map._repr_html_()
'''
@app.route("/open-street-map")
def open_street_map():
    # this map using stamen toner
    map = folium.Map(
        location=[45.52336, -122.6750],
        tiles='Stamen Toner',
        zoom_start=13
    )
    
    folium.Circle(
        location=[-27.551667, -48.478889],
        radius=radius,
        color="black",
        weight=1,
        fill_opacity=0.6,
        opacity=1,
        fill_color="green",
        fill=False,  # gets overridden by fill_color
        popup="{} meters".format(radius),
        tooltip="I am in meters",
    ).add_to(m)

    folium.Marker(
        location=[45.52336, -122.6750],
        popup="<b>Marker here</b>",
        tooltip="Click Here!"
    ).add_to(map)
    
    return map._repr_html_()

@app.route("/map-marker")
def map_marker():
    # this map using stamen terrain
    # we add some marker here
    map = folium.Map(
        location=[45.52336, -122.6750],
        tiles='Stamen Terrain',
        zoom_start=12
    )

    folium.Marker(
        location=[45.52336, -122.6750],
        popup="<b>Marker here</b>",
        tooltip="Click Here!"
    ).add_to(map)

    folium.Marker(
        location=[45.55736, -122.8750],
        popup="<b>Marker 2 here</b>",
        tooltip="Click Here!",
        icon=folium.Icon(color='green')
    ).add_to(map)

    folium.Marker(
        location=[45.53236, -122.8750],
        popup="<b>Marker 3 here</b>",
        tooltip="Click Here!",
        icon=folium.Icon(color='red')
    ).add_to(map)

    return map._repr_html_()


'''

if __name__ == "__main__":
    app.run(debug=True, host=server)
