import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Cargar los datos (Asegúrate de que esta ruta sea correcta)
# pd.read_csv está buscando un archivo llamado 'spacex_launch_dash.csv' en la misma ubicación que tu script de Python.

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"

try:
    spacex_df = pd.read_csv(URL)
except FileNotFoundError:
    # Usa un DataFrame de ejemplo si no tienes el archivo a mano
    data = {'Flight Number': range(1, 10),
            'Launch Site': ['CCAFS LC-40', 'CCAFS LC-40', 'KSC LC-39A', 'KSC LC-39A', 'VAFB SLC-4E', 'VAFB SLC-4E', 'CCAFS SLC-40', 'CCAFS SLC-40', 'KSC LC-39A'],
            'class': [0, 1, 1, 0, 1, 1, 0, 1, 0],
            'Payload Mass (kg)': [1000, 5000, 12000, 3000, 15000, 4500, 18000, 7000, 9000]}
    spacex_df = pd.DataFrame(data)

# Máximo y Mínimo de Masa de Carga útil
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Opciones para el desplegable
opciones_sitios = [{'label': 'Todos los Sitios', 'value': 'ALL'}] + \
                   [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Análisis de Éxito de Lanzamientos SpaceX',
            style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 40}),

    # TAREA 1: Componente Desplegable (Dropdown)
    dcc.Dropdown(
        id='site-dropdown',
        options=opciones_sitios,
        value='ALL',  # Valor inicial
        placeholder="Seleccionar un Sitio de Lanzamiento",
        searchable=True
    ),
    html.Br(),

    # Espacio para el gráfico circular (Pie Chart)
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Rango de Masa de Carga Útil (kg):"),

    # TAREA 3: Componente Control Deslizante (RangeSlider)
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: f'{i}' for i in range(0, 10001, 2000)},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # Espacio para el gráfico de dispersión (Scatter Plot)
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# TAREA 2: Callback para renderizar el gráfico circular
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Mostrar el éxito total de todos los sitios
        fig = px.pie(
            spacex_df,
            names='class',
            title='Tasa de Éxito Total (Todos los Sitios)',
            hole=.3
        )
        fig.update_traces(labels=['Fracaso', 'Éxito'], marker=dict(colors=['red', 'green']))
        return fig
    else:
        # Filtrar por sitio y calcular el éxito
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Agrupar y contar las clases
        success_counts = filtered_df['class'].value_counts().reset_index()
        success_counts.columns = ['class', 'count']

        fig = px.pie(
            success_counts,
            names='class',
            values='count',
            title=f'Éxito de Lanzamiento en el Sitio: {selected_site}',
            hole=.3
        )
        fig.update_traces(labels=['Fracaso', 'Éxito'], marker=dict(colors=['red', 'green']))
        return fig


# TAREA 4: Callback para renderizar el gráfico de dispersión
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range

    # 1. Filtrar por rango de masa de carga útil
    df_filtrado_masa = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
        ]

    # 2. Filtrar por sitio de lanzamiento
    if selected_site == 'ALL':
        df_final = df_filtrado_masa
        titulo = f'Éxito de Carga Útil vs. Órbita (Todos los Sitios)'
    else:
        df_final = df_filtrado_masa[df_filtrado_masa['Launch Site'] == selected_site]
        titulo = f'Éxito de Carga Útil vs. Órbita en {selected_site}'

    # 3. Crear el gráfico de dispersión
    fig = px.scatter(
        df_final,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',  # Colorear por categoría de cohete
        title=titulo,
        labels={'class': 'Resultado (0=Fracaso, 1=Éxito)'},
        hover_data=['Launch Site']  # Datos adicionales al pasar el ratón
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)