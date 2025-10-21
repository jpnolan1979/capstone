import csv, sqlite3
import prettytable
import pandas as pd
prettytable.DEFAULT = 'DEFAULT'
import sqlite3

# Diccionario con las consultas SQL
QUERIES ={
    1: {
        "description": "Masa promedio de carga útil (F9 v1.1)",
        "sql": "SELECT DISTINCT Launch_Site FROM SPACEXTBL;"
    },
    2: {
        "description": "Fecha del primer aterrizaje exitoso en plataforma terrestre",
        "sql": "SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5;"
    },
    3: {
        "description": "Boosters con éxito en drone ship y carga útil entre 4000kg y 6000kg",
        "sql": "SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Customer = 'NASA (CRS)';"
    },
    4: {
        "description": "Conteo total de resultados de misión (Éxito/Fallo)",
        "sql": "SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%';"
    },
    5: {
        "description": "Boosters con la máxima masa de carga útil",
        "sql": "SELECT MIN(Date) FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)';"
    },
    6: {
        "description": "Fallos en drone ship en 2015 (Mes, Booster, Sitio)",
        "sql": "SELECT DISTINCT Booster_Version FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ > 4000 AND PAYLOAD_MASS__KG_ < 6000;"
    },
    7: {
        "description": "Ranking de resultados de aterrizaje (2010-06-04 a 2017-03-20)",
        "sql": "SELECT Mission_Outcome, COUNT(Mission_Outcome) AS Total_Count FROM SPACEXTBL GROUP BY Mission_Outcome;"
    },
    8: {
        "description": "Ranking de resultados de aterrizaje (2010-06-04 a 2017-03-20)",
        "sql": "SELECT DISTINCT Booster_Version FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL);"
    },
    9: {
        "description": "Ranking de resultados de aterrizaje (2010-06-04 a 2017-03-20)",
        "sql": "SELECT SUBSTR(Date, 6, 2) AS Month_Name, Landing_Outcome, Booster_Version, Launch_Site FROM SPACEXTBL WHERE SUBSTR(Date, 0, 5) = '2015' AND Landing_Outcome = 'Failure (drone ship)';"
    },
    10: {
        "description": "Ranking de resultados de aterrizaje (2010-06-04 a 2017-03-20)",
        "sql": "SELECT Landing_Outcome, COUNT(Landing_Outcome) AS Count_of_Outcomes FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Count_of_Outcomes DESC;"
    },

}

# Nombre del archivo de la base de datos
DB_NAME = "my_data1db"

# ----------------------------------------------------------------------
# Funciones principales
# ----------------------------------------------------------------------

def display_menu():
    """Muestra el menú de consultas disponibles."""
    print("\n" + "=" * 40)
    print("🚀 Menú de Consultas SQL de SpaceX 🛰️")
    print("=" * 40)
    for num, data in QUERIES.items():
        print(f"[{num}] - {data['description']}")
    print("[0] - Salir")
    print("=" * 40)


def execute_query(query_sql):
    """Establece conexión, ejecuta la consulta y muestra los resultados."""
    try:
        # Conexión a la base de datos (se crea si no existe)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        df = pd.read_csv("Spacex (2).csv")
        df.to_sql("SPACEXTBL", conn, if_exists='replace', index=False, method="multi")

        # Ejecutar la consulta
        cursor.execute(query_sql)
        results = cursor.fetchall()

        # Obtener los nombres de las columnas
        column_names = [description[0] for description in cursor.description]

        # Mostrar los resultados
        print("\n" + "-" * 50)
        print("✅ Resultados de la Consulta:")
        print(column_names)
        print("-" * len(str(column_names)))
        for row in results:
            print(row)
        print("-" * 50)

    except sqlite3.Error as e:
        print(f"\n❌ Ocurrió un error al ejecutar la consulta: {e}")
    finally:
        if conn:
            conn.close()


def main():
    """Función principal del script."""
    while True:
        display_menu()

        try:
            choice = int(input("Introduce el número de la consulta a ejecutar (o 0 para salir): "))
        except ValueError:
            print("🛑 Entrada inválida. Por favor, introduce un número.")
            continue

        if choice == 0:
            print("👋 Saliendo del script. ¡Adiós!")
            break

        if choice in QUERIES:
            query_data = QUERIES[choice]
            print(f"\n⚙️ Ejecutando: {query_data['description']}...")
            execute_query(query_data['sql'])
        else:
            print("🔢 Número de consulta no válido. Inténtalo de nuevo.")


# Ejecutar el script
if __name__ == "__main__":
    main()








