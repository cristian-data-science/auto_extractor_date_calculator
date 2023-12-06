import streamlit as st
import pandas as pd
import re
from time import sleep

def extract_rut(description):
    rut_patterns = [
        re.compile(r"Trabajador(?: Contratista Acreditado)?:\s*0*([A-Za-z]?\d{7,8}-[\dkK])"),
        re.compile(r"Trabajador: ([\w-]+)"),
        re.compile(r"Trabajador Contratista Acreditado: ([\w-]+)")
    ]
    
    for rut_pattern in rut_patterns:
        match = rut_pattern.search(description)
        if match:
            return match.group(1)
    return None

def safe_convert_to_datetime(date_str):
    try:
        return pd.to_datetime(date_str)
    except ValueError:
        return "Error de formato de fecha"

def process_file(uploaded_file):
    # Carga los datos desde el archivo
    base_sheet_df = pd.read_excel(uploaded_file, sheet_name='tiempo de acreditación')
    bitacora_sheet_df = pd.read_excel(uploaded_file, sheet_name='Bitacora 4540006488')

    # Aplica las transformaciones
    bitacora_sheet_df['RUT'] = bitacora_sheet_df['Descripción Evento'].apply(extract_rut)
    bitacora_sheet_df = bitacora_sheet_df[bitacora_sheet_df['Evento'] == 'Aprobación Pase Trabajador']
    latest_dates_df = bitacora_sheet_df.groupby('RUT')['Fecha Evento'].min().reset_index()
    results_df = pd.merge(base_sheet_df, latest_dates_df, on='RUT', how='left')
    results_df['CREACIÓN DE FERFIL ES SIGA'] = results_df['CREACIÓN DE FERFIL ES SIGA'].apply(safe_convert_to_datetime)
    results_df['ACREDITADO'] = results_df['Fecha Evento'].apply(safe_convert_to_datetime)
    results_df = results_df.groupby('RUT').agg({'CREACIÓN DE FERFIL ES SIGA': 'min', 'ACREDITADO': 'first', 'Fecha Evento': 'first'}).reset_index()
    results_df['días'] = results_df.apply(lambda row: (row['ACREDITADO'] - row['CREACIÓN DE FERFIL ES SIGA']).days if isinstance(row['ACREDITADO'], pd.Timestamp) and isinstance(row['CREACIÓN DE FERFIL ES SIGA'], pd.Timestamp) else None, axis=1)
    final_columns = ['RUT','CREACIÓN DE FERFIL ES SIGA','ACREDITADO', 'días']
    results_df = results_df[final_columns]

    return results_df

st.title('Extracción de Ruts y calculo de días de acreditación')

with st.expander("Información para el uso"):
    st.write("""
    Para la correcta carga del archivo este debe tener dos hojas en el Excel subido:
    - Una llamada "tiempo de acreditación" y tiene que contener los campos "RUT", "CREACIÓN DE FERFIL ES SIGA" y "ACREDITADO".
    - Y otra hoja llamada "Bitacora 4540006488" con al menos los campos "Evento" y "Descripción Evento".
    """)

st.header('Sube tu archivo Excel')

uploaded_file = st.file_uploader('Elige un archivo Excel', type='xlsx')

if uploaded_file is not None:
    st.write('Archivo subido con éxito!')

    # Inicia el proceso de extracción de RUTs
    with st.spinner('Extrayendo RUTs...'):
        my_bar = st.progress(0)
        for percent_complete in range(100):
            sleep(0.1)  # Simula el tiempo de procesamiento
            my_bar.progress(percent_complete + 1)
        # Finaliza la extracción de RUTs
        st.success('Extracción de RUTs completada!')

    # Procesamiento de los datos y generación de resultados
    try:
        st.info('Calculando los días de acreditación')
        results_df = process_file(uploaded_file)

        st.write('Resultados:')
        st.dataframe(results_df)

        # Botón de descarga
        st.download_button(
            label="Descargar resultados como Excel",
            data=results_df.to_csv(index=False).encode('utf-8'),
            file_name='resultados.csv',
            mime='text/csv'
        )

    except Exception as e:
        st.error(f'Error al procesar el archivo: {e}')