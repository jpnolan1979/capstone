# pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns

#from js import fetch
#import io

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
#resp = await fetch(URL)
#dataset_part_2_csv = io.BytesIO((await resp.arrayBuffer()).to_py())
df=pd.read_csv(URL)
#print(df.head(5))


sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()

#Tarea 1
sns.catplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Launch Site",fontsize=20)
plt.show()

#Tarea 2
sns.catplot(y="LaunchSite", x="PayloadMass", hue="Class", data=df, aspect = 5)
plt.xlabel("Payload Mass",fontsize=20)
plt.ylabel("Launch Site",fontsize=20)
plt.show()

#Tarea 3
tasa_exito_por_orbita = df.groupby('Orbit')['Class'].mean().reset_index()
print(tasa_exito_por_orbita)
# Paso 2: Crear el gráfico de barras
plt.figure(figsize=(12, 6)) # Ajusta el tamaño de la figura
sns.barplot(
    x='Orbit',           # Variable categórica en el eje X
    y='Class',    # Variable numérica (tasa de éxito) en el eje Y
    data=tasa_exito_por_orbita,
    palette='viridis'     # Un esquema de colores agradable
)

# Añadir títulos y etiquetas para claridad
plt.title('Tasa de Éxito por Tipo de Órbita', fontsize=16)
plt.xlabel('Tipo de Órbita', fontsize=12)
plt.ylabel('Tasa de Éxito (Media de Clase)', fontsize=12)

# Rotar las etiquetas del eje X si es necesario para evitar superposición
plt.xticks(rotation=45, ha='right')

# Muestra el gráfico
plt.tight_layout()
plt.show()

#Tarea 4
# Configuración del tamaño de la figura para mejor visualización
plt.figure(figsize=(12, 6))

# Dibujar el gráfico de dispersión
sns.scatterplot(
    x='FlightNumber',  # Número del vuelo en el eje X (variable continua/secuencial)
    y='Orbit',        # Tipo de órbita en el eje Y (variable categórica)
    hue='Class',       # Color (tono) determinado por el éxito (1) o fracaso (0)
    data=df,           # El DataFrame de origen
    s=100              # Tamaño de los puntos (opcional, para hacerlos más visibles)
)

# Añadir títulos y etiquetas
plt.title('Relación entre Número de Vuelo, Órbita y Éxito', fontsize=16)
plt.xlabel('Número de Vuelo', fontsize=12)
plt.ylabel('Tipo de Órbita', fontsize=12)

# Mostrar la leyenda y el gráfico
plt.legend(title='Éxito (Clase)', labels=['Fracaso (0)', 'Éxito (1)'])
plt.grid(True, linestyle='--', alpha=0.6) # Agregar una cuadrícula para facilitar la lectura
plt.tight_layout()
plt.show()

#Tarea 5
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración del tamaño de la figura para mejor visualización
plt.figure(figsize=(12, 6))

# Dibujar el gráfico de dispersión
sns.scatterplot(
    x='PayloadMass',  # Masa de la carga útil en el eje X (variable continua)
    y='Orbit',        # Tipo de órbita en el eje Y (variable categórica)
    hue='Class',       # Color (tono) determinado por el éxito (1) o fracaso (0)
    data=df,           # El DataFrame de origen
    s=100,             # Tamaño de los puntos
    palette='viridis'  # Paleta de colores para 'Clase'
)

# Añadir títulos y etiquetas
plt.title('Relación entre Masa de la Carga Útil, Órbita y Éxito', fontsize=16)
plt.xlabel('Masa de la Carga Útil (kg)', fontsize=12)
plt.ylabel('Tipo de Órbita', fontsize=12)

# Mostrar la leyenda y el gráfico
plt.legend(title='Éxito (Clase)', labels=['Fracaso (0)', 'Éxito (1)'])
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

#Tarea 6
#Transformamos la columna de fechas a años
year=[]
def Extract_year():
    for i in df["Date"]:
        year.append(i.split("-")[0])
    return year
Extract_year()
df['Date'] = year

#Calcular la Tasa de Éxito (mean de 'Clase') agrupado por Año ('Date')
tasa_exito_anual = df.groupby('Date')['Class'].mean().reset_index()
#Renombrar la columna
tasa_exito_anual.rename(columns={'Class': 'Tasa_de_Éxito'}, inplace=True)

#Crear el gráfico de líneas
plt.figure(figsize=(10, 6))
sns.lineplot(
    x='Date',                  # Año en el eje X
    y='Tasa_de_Éxito',         # Tasa de éxito en el eje Y
    data=tasa_exito_anual,
    marker='o',                # Añadir puntos para ver los datos de cada año
    linewidth=3                # Grosor de la línea
)

# Añadir títulos y etiquetas
plt.title('Tendencia Anual de la Tasa de Éxito de Lanzamiento', fontsize=16)
plt.xlabel('Año', fontsize=12)
plt.ylabel('Tasa de Éxito Promedio', fontsize=12)

# Mostrar los años claramente en el eje X
plt.xticks(rotation=45, ha='right', ticks=tasa_exito_anual['Date'].unique())
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()


#Nuevo DataFrame
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()

#Tarea 7
# Lista de columnas categóricas a codificar
columnas_categoricas = ['Orbit', 'LaunchSite', 'LandingPad', 'Serial']

features_one_hot = pd.get_dummies(
    data=features,  # El DataFrame de entrada que contiene todas las features
    columns=columnas_categoricas  # Las columnas que deben ser codificadas
)

# Mostrar las primeras filas del DataFrame resultante
print(features_one_hot.head())

# Verificar las dimensiones del nuevo DataFrame
print(f"\nForma del DataFrame original: {features.shape}")
print(f"Forma del DataFrame one-hot: {features_one_hot.shape}")

#Tarea 8
features_one_hot = features_one_hot.astype('float64')

#Verificar el tipo de dato para confirmar la conversión
print("Tipos de datos del DataFrame features_one_hot después de la conversión:")
print(features_one_hot.dtypes)

# Exportar a CSV
features_one_hot.to_csv('dataset_part_3.csv', index=False)
print("\nDataFrame exportado a 'dataset_part_3.csv'")
