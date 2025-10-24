import coordinates as coordinates
import folium
import pandas as pd
from folium.plugins import MarkerCluster
from folium.plugins import MousePosition
from folium.features import DivIcon

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
spacex_df=pd.read_csv(URL)

#TAREA 1
#UBICACION DE LOS LUGARES DE LANZAMIENTO
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]

#Función para mapear el valor de Clase al color
def asignar_color(clase):
    if clase == 1:
        return 'green'
    else:
        return 'red'

#Crear la nueva columna 'Color' aplicando la función a la columna 'Clase'
spacex_df['Color'] = spacex_df['class'].apply(asignar_color)

#Armado del mapa
mapa_cluster = folium.Map(
    location=[spacex_df['Lat'].mean(), spacex_df['Long'].mean()],
    zoom_start=5
)

#Crear el objeto MarkerCluster
marker_cluster = MarkerCluster()

#Añadir el MarkerCluster al mapa
mapa_cluster.add_child(marker_cluster)

#Iterar sobre el DataFrame para crear y añadir marcadores al CLÚSTER
for index, row in spacex_df.iterrows():
    # Extraer las coordenadas y el color asignado
    lat = row['Lat']
    lon = row['Long']
    color = row['Color']
    lugar_lanzamiento = row['Launch Site']
    # 4.1. Definir el icono con el color dinámico
    icono = folium.Icon(color=color, icon='rocket', prefix='fa')

    # 4.2. Crear el marcador
    marcador = folium.Marker(
        location=[lat, lon],
        # El popup mostrará si fue Éxito o Fracaso
        popup=f"Lugar: {row['Launch Site']}<br>Clase: {row['class']} ({color.upper()})",
        icon=icono
    )

    # 4.3. Añadir el marcador al CLÚSTER, NO directamente al mapa
    marcador.add_to(marker_cluster)

    folium.Marker(
            location=[lat, lon],
            popup=f"<b>{lugar_lanzamiento}</b><br>Lat: {lat:.3f}, Lon: {lon:.3f}",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(mapa_cluster)

    folium.CircleMarker(
        location=[lat, lon],
        radius=15,  # Tamaño del círculo
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=f"Círculo en {lugar_lanzamiento}"
    ).add_to(mapa_cluster)

#Añadimos la posicion del mouse
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

mapa_cluster.add_child(mouse_position)

from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

#Definir los puntos a conectar
coor_sitio = [28.56321, -80.57673]
coor_coast = [28.5637, -80.568]
coordenadas_trayecto = [coor_sitio, coor_coast]

#Calcular la distancia
distance_coastline = calculate_distance(coor_sitio[0], coor_sitio[1], coor_coast[0], coor_coast[1])
print(f"Distancia calculada: {distance_coastline:.2f} KM")

#Crear el objeto mapa (Si no lo tienes)
# mapa_cluster = folium.Map(location=[28.563, -80.569], zoom_start=15)

#Dibujar la línea (PolyLine)
lines=folium.PolyLine(locations=coordenadas_trayecto, weight=2, color='darkorange')
mapa_cluster.add_child(lines)

#Agregar el marcador de texto (DivIcon)
distance_marker = folium.Marker(
    coor_coast, # Ubicación del marcador en la costa
    icon=DivIcon(
        icon_size=(100,20), # Aumentamos el tamaño para que quepa el texto
        icon_anchor=(0,0),
        html='<div style="font-size: 12px; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),
    )
).add_to(mapa_cluster)

# 6. Guardar el mapa
mapa_cluster.show_in_browser()
print("El mapa interactivo con clústers y círculos se ha generado.")














