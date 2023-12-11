# Extracción de Ruts y calculo de días de acreditación

Esta es una aplicación web desarrollada en Python utilizando la biblioteca Streamlit. La aplicación permite a los usuarios subir un archivo Excel, extraer información específica y realizar cálculos en los datos.

## Funcionalidades

1. **Subida de archivos**: Los usuarios pueden subir un archivo Excel que contenga dos hojas: 'tiempo de acreditación' y 'Bitacora 4540006488'.

2. **Extracción de RUTs**: La aplicación extrae los RUTs (números de identificación utilizados en Chile) de la columna 'Descripción Evento' en la hoja 'Bitacora 4540006488'.

3. **Cálculo de días de acreditación**: La aplicación calcula el número de días entre 'CREACIÓN DE FERFIL ES SIGA' y 'ACREDITADO' para cada RUT.

4. **Visualización de resultados**: Los resultados se muestran en la interfaz de usuario y también se pueden descargar como un archivo CSV.

## Cómo usar

1. Abra la aplicación en su navegador web.
2. Suba su archivo Excel utilizando el botón de subida de archivos.
3. Espere mientras la aplicación extrae los RUTs y calcula los días de acreditación.
4. Visualice los resultados en la interfaz de usuario y descargue los resultados si lo desea.

## Requisitos

- Python 3.6 o superior
- Bibliotecas: streamlit, pandas, re, time

## Instalación

Para instalar las dependencias necesarias, ejecute el siguiente comando:

```bash
pip install streamlit pandas