import sys

import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd


def date_time(table_cells):
    """
    This function returns the data and time from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]


def booster_version(table_cells):
    """
    This function returns the booster version from the HTML  table cell
    Input: the  element of a table data cell extracts extra row
    """
    out = ''.join([booster_version for i, booster_version in enumerate(table_cells.strings) if i % 2 == 0][0:-1])
    return out


def landing_status(table_cells):
    """
    This function returns the landing status from the HTML table cell
    Input: the  element of a table data cell extracts extra row
    """
    out = [i for i in table_cells.strings][0]
    return out


def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass.find("kg")
        new_mass = mass[0:mass.find("kg") + 2]
    else:
        new_mass = 0
    return new_mass


def extract_column_from_header(row):
    """
    This function returns the landing status from the HTML table cell
    Input: the  element of a table data cell extracts extra row
    """
    if (row.br):
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()

    colunm_name = ' '.join(row.contents)

    # Filter the digit and empty names
    if not (colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name

static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(static_url, headers=headers)
print(f"Código de estado HTTP: {response.status_code}")

# Suponiendo que 'response' es el objeto que obtuviste con requests.get()
html_content = response.text

# Crea el objeto 'soup' para analizar el HTML
soup = BeautifulSoup(html_content, 'html.parser')

print("¡Objeto BeautifulSoup creado con éxito!")

# 1. Usar .find('title') para localizar la etiqueta <title>
title_tag = soup.find('title')

# 2. Verificar si la etiqueta se encontró (por si acaso) y obtener el texto
if title_tag:
    # Usar .get_text() para obtener el contenido de la etiqueta
    page_title = title_tag.get_text()

    # 3. Imprimir el resultado
    print("El título de la página es:")
    print(page_title)
else:
    print("No se pudo encontrar la etiqueta <title> en el documento.")

# 1. Encontrar todas las etiquetas <table> en la página
all_tables = soup.find_all('table')

print(f"Se encontraron {len(all_tables)} tabla(s) en la página.")

# Let's print the third table and check its content
first_launch_table = all_tables[2]
print(first_launch_table)
cleaned_column_names = []

header_cells = first_launch_table.find_all('th')
column_names = [th.get_text().strip() for th in header_cells]
cleaned_column_names = [name for name in column_names if name]

# 5. Imprimir el resultado para verificar
print(f"La tabla de interés se encuentra en el índice: 2")
print("\nNombres de las columnas (Encabezados de la Tabla Seleccionada):")
if cleaned_column_names:
    print(cleaned_column_names)
else:
    print("No se encontraron encabezados de columna (<th>) en esta tabla específica.")

print(cleaned_column_names)

launch_dict= dict.fromkeys(cleaned_column_names)

# Remove an irrelvant column
del launch_dict['Date andtime (UTC)']

# Let's initial the launch_dict with each value to be an empty list
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
# Added some new columns
launch_dict['Version Booster']=[]
launch_dict['Booster landing']=[]
launch_dict['Date']=[]
launch_dict['Time']=[]

extracted_row = 0
# Extract each table
for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
    # get table row
    for rows in table.find_all("tr"):
        # check to see if first table heading is as number corresponding to launch a number
        if rows.th:
            if rows.th.string:
                flight_number = rows.th.string.strip()
                flag = flight_number.isdigit()
        else:
            flag = False
        # get table element
        row = rows.find_all('td')
        # if it is number save cells in a dictonary
        if flag:
            extracted_row += 1
            # Flight Number value
            # TODO: Append the flight_number into launch_dict with key `Flight No.`
            # print(flight_number)
            datatimelist = date_time(row[0])

            # Date value
            # TODO: Append the date into launch_dict with key `Date`
            date = datatimelist[0].strip(',')
            # print(date)

            # Time value
            # TODO: Append the time into launch_dict with key `Time`
            time = datatimelist[1]
            # print(time)

            # Booster version
            # TODO: Append the bv into launch_dict with key `Version Booster`
            bv = booster_version(row[1])
            if not (bv):
                bv = row[1].a.string
            print(bv)

            # Launch Site
            # TODO: Append the bv into launch_dict with key `Launch Site`
            launch_site = row[2].a.string
            # print(launch_site)

            # Payload
            # TODO: Append the payload into launch_dict with key `Payload`
            payload = row[3].a.string
            # print(payload)

            # Payload Mass
            # TODO: Append the payload_mass into launch_dict with key `Payload mass`
            payload_mass = get_mass(row[4])
            # print(payload)

            # Orbit
            # TODO: Append the orbit into launch_dict with key `Orbit`
            orbit = row[5].a.string
            # print(orbit)

            # Customer
            # TODO: Append the customer into launch_dict with key `Customer`
            customer = row[6].a
            # print(customer)

            # Launch outcome
            # TODO: Append the launch_outcome into launch_dict with key `Launch outcome`
            launch_outcome = list(row[7].strings)[0]
            # print(launch_outcome)

            # Booster landing
            # TODO: Append the launch_outcome into launch_dict with key `Booster landing`
            booster_landing = landing_status(row[8])
            # print(booster_landing)

# 1. Localizar todas las filas de la tabla (etiquetas <tr>)
# Asumimos que first_lunch_table es la variable que contiene all_tables[2]
table_rows = first_launch_table.find_all('tr')

# Lista para almacenar el resultado final de los datos del lanzamiento
launch_data = []

# Iterar sobre cada fila (<tr>) de la tabla
for row in table_rows:
    # Crear un diccionario temporal para almacenar los datos de la fila actual
    row_data = {}

    # 2. Encontrar todas las celdas de datos (etiquetas <td> y <th>) en la fila
    # Incluimos 'th' porque la primera celda (el número de vuelo) a menudo es un encabezado <th>
    cells = row.find_all(['td', 'th'])

    # 3. Asignar los datos extraídos a las claves del diccionario

    # El primer elemento (cells[0]) suele ser el número de vuelo
    if len(cells) > 0 and 'Flight No.' in launch_dict:
        row_data['Flight No.'] = cells[0].get_text(strip=True)

    # Las celdas restantes (a partir de cells[1]) contienen la información
    if len(cells) > 1:

        # El HTML de estas tablas a menudo requiere un análisis más detallado para
        # extraer correctamente el sitio, la carga, etc. Aquí hay un enfoque simplificado:

        # 3.1. Extracción de las primeras 7 columnas directas:
        # Nota: La estructura HTML puede variar, ajusta los índices si es necesario.

        # Columna 2: Launch site (Índice 1 de la lista 'cells')
        if len(cells) > 1 and 'Launch site' in launch_dict:
            row_data['Launch site'] = cells[1].get_text(strip=True)

        # Columna 3: Payload (Índice 2)
        if len(cells) > 2 and 'Payload' in launch_dict:
            row_data['Payload'] = cells[2].get_text(strip=True)

        # Columna 4: Payload mass (Índice 3)
        if len(cells) > 3 and 'Payload mass' in launch_dict:
            row_data['Payload mass'] = cells[3].get_text(strip=True)

        # Columna 5: Orbit (Índice 4)
        if len(cells) > 4 and 'Orbit' in launch_dict:
            row_data['Orbit'] = cells[4].get_text(strip=True)

        # Columna 6: Customer (Índice 5)
        if len(cells) > 5 and 'Customer' in launch_dict:
            row_data['Customer'] = cells[5].get_text(strip=True)

        # Columna 7: Launch outcome (Índice 6)
        if len(cells) > 6 and 'Launch outcome' in launch_dict:
            row_data['Launch outcome'] = cells[6].get_text(strip=True)

        # La tabla original tiene información compleja en la columna 1 (Fecha/Hora/Versión/Aterrizaje).
        # Para las claves añadidas ('Version Booster', 'Booster landing', 'Date', 'Time'),
        # estas requieren un análisis avanzado de etiquetas <a> y la limpieza del texto de cells[1].

        # --- Lógica Avanzada para las columnas 'Date', 'Time', 'Version Booster', 'Booster landing' ---

        # Para extraer 'Date' y 'Time' (que estaban en la columna 'Date and time (UTC)' original)
        # Buscar la primera etiqueta <td> dentro de la fila, que contiene el tiempo/fecha
        date_time_cell = cells[1]  # Usamos cells[1] para el ejemplo, pero puede variar

        # Si la celda contiene una etiqueta <span class="nowrap"> o similar, extráela
        date_tag = date_time_cell.find('span', class_='nowrap')
        if date_tag:
            date_time_text = date_tag.get_text(strip=True).split(' ')
            if len(date_time_text) >= 2:
                row_data['Date'] = date_time_text[0]
                row_data['Time'] = date_time_text[1]

        # El resto de la información (Booster, Landing) a menudo está contenida en enlaces (<a>)
        # o imágenes (<img>) dentro de una de las celdas, lo que requiere código específico
        # que va más allá de solo extraer el texto.

        # Si la extracción simple funciona para todas las columnas clave, puedes usar un bucle simple:
        # for i, key in enumerate(list(launch_dict.keys())[:7]): # Solo las primeras 7
        #     if len(cells) > i + 1:
        #         launch_dict[key].append(cells[i+1].get_text(strip=True))

        # --- FIN de Lógica Avanzada ---

    # **IMPORTANTE:** En lugar de append a listas vacías (que es complejo con el HTML variable),
    # es mejor llenar el diccionario temporal 'row_data' y luego añadirlo a una lista grande.
    if row_data:
        launch_data.append(row_data)

# 4. (Opcional) Convertir la lista de diccionarios en un DataFrame para inspeccionar
# Asegúrate de importar pandas: import pandas as pd
df = pd.DataFrame(launch_data)
print(df.head())

df.to_csv('spacex_web_scraped.csv', index=False)
print("CSV creado con exito")