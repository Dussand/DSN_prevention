import streamlit as st
import pandas as pd



st.title('Prevencion de DSN')
st.divider()

archivo = st.file_uploader('Subir el EECC del banco', type = ['xlsx', 'xls'])

if archivo is not None:
    df = pd.read_excel(archivo, skiprows= 7)
    df['Descripción operación'] = df['Descripción operación'].str.strip()
    df['Nº operación'] = df['Nº operación'].astype(str).str.strip()

        # ---- Nueva columna con el código extraído ----
    # Usar expresiones regulares para extraer códigos que empiezan con 250
    df['PSP_TIN'] = df['Descripción operación'].str.extract(r'(250\d{9})', expand=False)

    # ---- Nueva columna con formato JSON ----
    # Crear una columna con el formato JSON requerido
    df['PSPTIN_JSON'] = df['PSP_TIN'].apply(lambda x: f"'{x}'," if pd.notnull(x) else None)

    # ---- Identificar y eliminar filas duplicadas con extorno ----
    # Identificar duplicados según el "Número de operación"
    duplicados = df[df.duplicated(subset=['Nº operación'], keep=False)]

    # Filtrar los duplicados que contienen "Extorno" en "Descripción operación"
    condicion_extorno = duplicados['Descripción operación'].str.contains('Extorno', case=False, na=False)

    # Obtener los números de operación de las filas que tienen "Extorno"
    numeros_con_extorno = duplicados[condicion_extorno]['Nº operación'].unique()

    # Filtrar todas las filas que tienen esos números de operación (con o sin "Extorno")
    filas_a_eliminar = duplicados[duplicados['Nº operación'].isin(numeros_con_extorno)]

    st.dataframe(filas_a_eliminar)

    # Eliminar estas filas del DataFrame original
    df_filtrado = df[~df['Nº operación'].isin(numeros_con_extorno)]

    # ---- Eliminar las filas duplicadas en la columna 'PSPTIN' ----
    df_filtrado = df_filtrado.drop_duplicates(subset=['PSP_TIN'])

    # ---- Eliminar las filas donde PSP_TIN no empieza con 250 o no tiene 12 dígitos ----
    df_filtrado = df_filtrado[df_filtrado['PSP_TIN'].str.match(r'^250\d{9}$', na=False)]

    # st.write('EECC del banco')
    # st.dataframe(df_filtrado)

    # st.write()


    # # Guardar el archivo modificado
    # # archivo_salida = 'BBDD11022000.xlsx'
    # archivo_salida = st.text_input('Escribe el nombre del archivo:')
    # salida = st.button(f'Descarga el archivo')
    # if salida:
    #     df_filtrado.to_excel(archivo_salida, index=False)

    #     st.write(f"\nArchivo procesado y guardado como: {archivo_salida}")

        # Especificar los nombres de los archivos previamente subidos a Colab

file_2_name = st.file_uploader('Subir archivo de metabaes', type = ['xlsx', 'xls'] )
#file_2_name = "2_1_procesopago__detalle_2025-02-12T01_07_44.546161693Z.xlsx"  # Archivo de metabase

if file_2_name is not None:
    # Leer los archivos Excel
    data_2 = pd.read_excel(file_2_name)
    data_2['psp_tin'] = data_2['psp_tin'].astype(str)
    # Mostrar columnas de los archivos para confirmar que las columnas 8 y 27 están disponibles
    # st.write("Columnas del archivo 1:")
    # st.write(df_filtrado.columns)

    # st.write("Columnas del archivo 2:")
    # st.write(data_2.columns)

    # Especificar las columnas de búsqueda (columna 8 del archivo 1 y columna 27 del archivo 2)
    criteria_column_index_1 = 7  # Índice de la columna 8 en archivo 1 (basado en 0)
    criteria_column_index_2 = 26  # Índice de la columna 27 en archivo 2 (basado en 0)

    if criteria_column_index_1 >= len(df_filtrado.columns):
        raise ValueError(f"La columna con índice {criteria_column_index_1} no se encuentra en el archivo 1.")
    if criteria_column_index_2 >= len(data_2.columns):
        raise ValueError(f"La columna con índice {criteria_column_index_2} no se encuentra en el archivo 2.")

    criteria_column_1 = df_filtrado.columns[criteria_column_index_1]
    criteria_column_2 = data_2.columns[criteria_column_index_2]

    # Identificar datos presentes en el archivo 1 pero no en el archivo 2
    data_not_in_2 = df_filtrado[~df_filtrado[criteria_column_1].isin(data_2[criteria_column_2])]

    # Mostrar la tabla resultante en el mismo Colab con formato
    st.write("DSNs econtrados:")
    # display(data_not_in_2)

    st.dataframe(data_not_in_2)

    # # Exportar resultados a un archivo Excel
    # output_file = "DSN encontrados1200.xlsx"
    # data_not_in_2.to_excel(output_file, index=False)

    # st.write(f"Los DSN se encuentran en el archivo: {output_file}")
