import streamlit as st
import pandas as pd
import sqlite3
import io

st.title("Convertidor CSV a SQLite (.db)")
st.write("Convierte tus archivos CSV a bases de datos SQLite")

# Upload del archivo CSV
uploaded_file = st.file_uploader("Sube tu archivo CSV", type="csv")

# Nombre de la tabla/base de datos
db_name = st.text_input("Nombre de la tabla:", "mi_tabla")

if uploaded_file is not None and db_name:
    if st.button("Convertir a .db"):
        try:
            # Validar extensión del archivo
            if not uploaded_file.name.endswith('.csv'):
                st.error("❌ Error: El archivo debe tener extensión .csv")
                st.stop()

            # Leer CSV
            df = pd.read_csv(uploaded_file)

            # Validar que el DataFrame no esté vacío
            if df.empty:
                st.error("❌ Error: El archivo CSV está vacío o no contiene datos")
                st.stop()

            # Validar que tenga columnas
            if len(df.columns) == 0:
                st.error("❌ Error: El archivo no tiene columnas válidas")
                st.stop()

            # Validar que el nombre de la tabla sea válido
            if not db_name or db_name.strip() == "":
                st.error("❌ Error: Debes especificar un nombre válido para la tabla")
                st.stop()

            # Crear base de datos SQLite
            conn = sqlite3.connect(f'{db_name}.db')
            df.to_sql(db_name, conn, if_exists='replace', index=False)
            conn.close()

            # Mostrar información
            st.success(f"✓ Base de datos creada con {len(df)} registros")
            st.info(f"✓ Columnas: {len(df.columns)}")

            # Mostrar primeras filas
            st.write("Primeras filas:")
            st.dataframe(df.head())

            # Botón de descarga del archivo .db
            with open(f'{db_name}.db', 'rb') as f:
                st.download_button(
                    label="⬇️ Descargar base de datos (.db)",
                    data=f,
                    file_name=f'{db_name}.db',
                    mime='application/x-sqlite3'
                )

        except pd.errors.EmptyDataError:
            st.error("❌ Error: El archivo está vacío o no contiene datos válidos")

        except pd.errors.ParserError:
            st.error("❌ Error: El archivo no tiene un formato CSV válido. Verifica que esté correctamente estructurado")

        except UnicodeDecodeError:
            st.error("❌ Error: No se puede leer el archivo. Verifica la codificación del archivo")
            st.info("💡 Intenta guardar el archivo como CSV UTF-8 desde Excel")

        except ValueError as ve:
            st.error(f"❌ Error de valor: {str(ve)}")

        except sqlite3.Error as sql_error:
            st.error(f"❌ Error de base de datos SQLite: {str(sql_error)}")

        except Exception as e:
            st.error(f"❌ Error inesperado: {str(e)}")
            st.info("💡 Verifica que el archivo sea un CSV válido con datos")
