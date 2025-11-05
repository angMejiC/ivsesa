#fase 1: Analisis Exploratorio de los Datos e importamos las librerias

import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import folium
from folium.plugins import MarkerCluster
import streamlit.components.v1 as components # Importar el componente para HTML

with st.container():
     st.title("IVSESA: Índice de Vulnerabilidad Social y Seguridad Alimentaria 📊")
    
     st.markdown("---")
     
     st.markdown("El proyecto de Comedores Comunitarios de Santiago de Cali es una estrategia clave de apoyo" \
" alimentario y fortalecimiento social, con 780 comedores que entregan " \
"unas 80.000 raciones diarias en más de 25 comunas. " \
"La mayoría son gestionados por mujeres cabeza de hogar, quienes" \
" brindan un entorno solidario y cercano. Los beneficiarios son " \
"principalmente personas mayores, niños, mujeres, migrantes y víctimas del " \
"conflicto. Además de alimentar, los comedores funcionan como espacios protectores" \
" y de cohesión social. En 2024 se realizó una caracterización sociodemográfica para" \
" mejorar la atención a poblaciones vulnerables. Con base en ello, se propone " \
"crear un índice de vulnerabilidad social que permita focalizar intervenciones " \
"y fortalecer la seguridad alimentaria en la ciudad.")

     st.title("Objetivo general")
     st.markdown("Construir un índice de vulnerabilidad social con énfasis " \
"en seguridad alimentaria, a partir del análisis " \
"y la visualización de datos provenientes " \
"de la caracterización sociodemográfica de" \
" la población beneficiaria del proyecto de " \
"Comedores Comunitarios en Santiago de Cali, con el " \
"fin de focalizar y optimizar las intervenciones" \
" relacionadas con seguridad alimentaria en la ciudad")

# 1. Subir dataset 
archivo = st.file_uploader("Sube tu dataset CSV", type=["csv"])
if archivo is not None:
    df = pd.read_csv(archivo)
    
    # =============================================
    # NUEVO: TABLERO DE CONTROL (DASHBOARD)
    # =============================================
    st.markdown("---")
    st.header("📈 Tablero de Control - IVSESA")
    
    # Crear pestañas para organizar el dashboard
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Resumen General", 
        "🍎 Seguridad Alimentaria", 
        "💰 Situación Económica", 
        "👥 Demografía"
    ])
    
    with tab1:
        st.subheader("Resumen General del Dataset")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total de Registros", 
                value=f"{len(df):,}",
                help="Número total de hogares encuestados"
            )
        
        with col2:
            st.metric(
                label="Columnas Disponibles", 
                value=f"{len(df.columns)}",
                help="Variables disponibles en el dataset"
            )
        

        
        
        

    
    with tab2:
        st.subheader("Indicadores de Seguridad Alimentaria")
        
        # Verificar si las columnas existen antes de usarlas
        columnas_alimentacion = [
            'Consumo_proteínas', 'Consumo_frutas_verduras', 'Consumo_lácteos',
            'Variedad_alimentos', 'Saltar_comida', 'Hambre_no_comio', 'Falta_dinero'
        ]
        
        columnas_existentes = [col for col in columnas_alimentacion if col in df.columns]
        
        if columnas_existentes:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'Saltar_comida' in df.columns:
                    saltar_comida = (df['Saltar_comida'] == 'SI').sum()
                    st.metric(
                        label="Hogares que saltan comidas",
                        value=f"{saltar_comida:,}",
                        delta=f"{(saltar_comida/len(df)*100):.1f}%"
                    )
            
            with col2:
                if 'Hambre_no_comio' in df.columns:
                    hambre = (df['Hambre_no_comio'] == 'SI').sum()
                    st.metric(
                        label="Hogares con hambre por falta de comida",
                        value=f"{hambre:,}",
                        delta=f"{(hambre/len(df)*100):.1f}%"
                    )
            
            with col3:
                if 'Falta_dinero' in df.columns:
                    falta_dinero = (df['Falta_dinero'] == 'SI').sum()
                    st.metric(
                        label="Hogares con falta de dinero para alimentos",
                        value=f"{falta_dinero:,}",
                        delta=f"{(falta_dinero/len(df)*100):.1f}%"
                    )
            
            # Gráfico de distribución de consumo
            st.subheader("Distribución del Consumo Alimentario")
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            axes = axes.flatten()
            
            graficos_generados = 0
            for i, col in enumerate(columnas_existentes[:4]):
                if col in df.columns and graficos_generados < 4:
                    try:
                        conteo = df[col].value_counts()
                        axes[graficos_generados].pie(conteo.values, labels=conteo.index, autopct='%1.1f%%')
                        axes[graficos_generados].set_title(f'Distribución de {col}')
                        graficos_generados += 1
                    except:
                        continue
            
            # Ocultar ejes vacíos
            for i in range(graficos_generados, 4):
                axes[i].set_visible(False)
            
            plt.tight_layout()
            st.pyplot(fig)
        
        else:
            st.info("Las columnas de seguridad alimentaria se procesarán después de la limpieza de datos.")
    
    with tab3:
        st.subheader("Indicadores Económicos")
        
        # Verificar columnas económicas
        columnas_economicas = ['Ingresos_mensuales', 'Alcance_de_ingresos_hogar', 'Satisfacción_ingresos']
        columnas_existentes = [col for col in columnas_economicas if col in df.columns]
        
        if columnas_existentes:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'Ingresos_mensuales' in df.columns:
                    try:
                        ingreso_promedio = pd.to_numeric(df['Ingresos_mensuales'], errors='coerce').mean()
                        st.metric(
                            label="Ingreso Mensual Promedio",
                            value=f"${ingreso_promedio:,.0f}",
                            help="Promedio de ingresos mensuales por hogar"
                        )
                    except:
                        st.metric(
                            label="Ingreso Mensual Promedio",
                            value="N/D"
                        )
            
            with col2:
                if 'Alcance_de_ingresos_hogar' in df.columns:
                    try:
                        no_alcanza = (df['Alcance_de_ingresos_hogar'] == 'Nunca alcanzan para cubrir todos los gastos').sum()
                        st.metric(
                            label="Ingresos no alcanzan",
                            value=f"{no_alcanza:,}",
                            delta=f"{(no_alcanza/len(df)*100):.1f}%"
                        )
                    except:
                        st.metric(
                            label="Ingresos no alcanzan",
                            value="N/D"
                        )
            
            with col3:
                if 'Satisfacción_ingresos' in df.columns:
                    try:
                        satisfaccion_promedio = pd.to_numeric(df['Satisfacción_ingresos'], errors='coerce').mean()
                        st.metric(
                            label="Satisfacción con Ingresos (0-10)",
                            value=f"{satisfaccion_promedio:.1f}",
                            help="Escala de 0 (muy insatisfecho) a 10 (muy satisfecho)"
                        )
                    except:
                        st.metric(
                            label="Satisfacción con Ingresos",
                            value="N/D"
                        )
            
            # Distribución de alcance de ingresos
            if 'Alcance_de_ingresos_hogar' in df.columns:
                st.subheader("Distribución del Alcance de Ingresos")
                fig, ax = plt.subplots(figsize=(10, 6))
                df['Alcance_de_ingresos_hogar'].value_counts().plot(kind='bar', ax=ax, color='skyblue')
                ax.set_title('Distribución del Alcance de Ingresos en el Hogar')
                ax.set_xlabel('Alcance de Ingresos')
                ax.set_ylabel('Número de Hogares')
                plt.xticks(rotation=45)
                st.pyplot(fig)
        
        else:
            st.info("Los indicadores económicos se calcularán después del procesamiento.")
    
    with tab4:
        st.subheader("Indicadores Demográficos")
        
        # Verificar columnas demográficas
        columnas_demograficas = ['Número_personas_en_hogar', 'Menores_5_años_en_hogar', 'Mayores_de_60_años']
        columnas_existentes = [col for col in columnas_demograficas if col in df.columns]
        
        if columnas_existentes:
            col1, col2, col3 = st.columns(3)
           
            
            with col2:
                if 'Menores_5_años_en_hogar' in df.columns:
                    try:
                        con_menores = (df['Menores_5_años_en_hogar'] == 'SI').sum()
                        st.metric(
                            label="Hogares con menores de 5 años",
                            value=f"{con_menores:,}",
                            delta=f"{(con_menores/len(df)*100):.1f}%"
                        )
                    except:
                        st.metric(
                            label="Hogares con menores de 5 años",
                            value="N/D"
                        )
            
            with col3:
                if 'Mayores_de_60_años' in df.columns:
                    try:
                        con_adultos_mayores = (df['Mayores_de_60_años'] == 'SI').sum()
                        st.metric(
                            label="Hogares con adultos mayores",
                            value=f"{con_adultos_mayores:,}",
                            delta=f"{(con_adultos_mayores/len(df)*100):.1f}%"
                        )
                    except:
                        st.metric(
                            label="Hogares con adultos mayores",
                            value="N/D"
                        )
            
            # Distribución del tamaño del hogar
            if 'Número_personas_en_hogar' in df.columns:
                st.subheader("Distribución del Tamaño del Hogar")
                fig, ax = plt.subplots(figsize=(10, 6))
                df['Número_personas_en_hogar'].value_counts().sort_index().plot(kind='bar', ax=ax, color='lightgreen')
                ax.set_title('Distribución del Número de Personas por Hogar')
                ax.set_xlabel('Número de Personas')
                ax.set_ylabel('Número de Hogares')
                st.pyplot(fig)
        
        else:
            st.info("Los indicadores demográficos se procesarán en las siguientes etapas.")
    
    st.markdown("---")
    # =============================================
    # FIN DEL NUEVO TABLERO DE CONTROL
    # =============================================
   


    
        # convertir la columna ingresos_mensuales a tipo float 
    df['Ingresos_mensuales'] = (
    df['Ingresos_mensuales']
    .astype(str)
    .str.replace('[^0-9,.]', '', regex=True)
    .str.replace(',', '.', regex=False)
    .astype(float)
       ) 
    st.write("### dataset con las columnas que vamos a utlizar para el analisis")

    st.dataframe(df[['Ingresos_mensuales','Alcance_de_ingresos_hogar','Satisfacción_ingresos','Consumo_proteínas',
                    'Consumo_frutas_verduras','Variedad_alimentos','Consumo_lácteos',
                    'Saltar_comida','Hambre_no_comio','Falta_dinero','Menores_5_años_en_hogar',
                     'Mayores_de_60_años','Número_personas_en_hogar']].head(5))
    

    #fase 2: Limpieza de Datos
    #la variable consumo_proteinas es una variable compuesta por otras 4 variables, vamos aplicar
    #  puntuacion numerica para darle valor """
   
     
    # Mapeo más preciso basado en frecuencia nutricional
    mapeo_consumo = {
    'NO CONSUMI ESTE ALIMENTO': 4,
    '1 VEZ EN LA SEMANA': 3,
    'DE 2 A 3 VECES A LA SEMANA': 2,
    'TODOS LOS DÍAS': 1,
    'NO SABE NO RESPONDE': 0       # Se mantiene como Missing
    }
    

    # Calcular puntuación total de proteínas (rango: 4-16)
    df['puntuacion_proteinas'] = (
    df['carnes_rojas'].map(mapeo_consumo) +
    df['Pollo'].map(mapeo_consumo) +
    df['Pescado'].map(mapeo_consumo) +
    df['Huevo'].map(mapeo_consumo)
        )
    # Convertir a categorías significativas
    df['Consumo_proteínas'] = pd.cut(df['puntuacion_proteinas'],
                                bins=[-1, 6, 9, 12, 16],
                                labels=[1,2,3,4])
    df['Consumo_proteínas'] = df['Consumo_proteínas'].astype(int)
    
    mapeo_frutas_verduras_vulnerabilidad = {
    # 4: Mayor vulnerabilidad
    'NO CONSUMÍ FRUTAS NI VERDURAS': 4,
    # 3: Alta vulnerabilidad
    '1 VEZ EN LA SEMANA': 3,
    # 2: Moderada vulnerabilidad
    'DE 2 A 3 VECES A LA SEMANA': 2,
    # 1: Menor vulnerabilidad
    'TODOS LOS DÍAS': 1,
    # 0: Missing
    'NO SABE NO RESPONDE': 0
              }
    df['Consumo_frutas_verduras'] = df['Consumo_frutas_verduras'].map(mapeo_frutas_verduras_vulnerabilidad)

    # Mapeo de vulnerabilidad para consumo_lácteos
    df['Consumo_lácteos_v'] = df['Consumo_lácteos'].astype(str).str.strip().str.upper()
    mapeo_lacteos_vulnerabilidad = {
    # 4: Mayor vulnerabilidad
    'NO CONSUMI LÁCTEOS NI SUS DERIVADOS': 4,
    # 3: Alta vulnerabilidad
    '1 VEZ A LA SEMANA': 3,
    # 2: Moderada vulnerabilidad
    'DE 2 A 3 VECES A LA SEMANA': 2,
    # 1: Menor vulnerabilidad
    'TODOS LOS DIAS': 1,
    # 0: Missing
    'NO SABE NO RESPONDE': 0
              }   
    # Aplicamos la limpieza y luego el mapeo:
    # Reemplaza la columna original con la nueva puntuación
    df['Consumo_lácteos'] = df['Consumo_lácteos_v'].map(mapeo_lacteos_vulnerabilidad)
    # Imputar los NaNs (que son valores que no coincidieron con ninguna clave del diccionario) a 0.
    df['Consumo_lácteos'] = df['Consumo_lácteos'].fillna(0)

      
    # Mapeo de VULNERABILIDAD para Variedad_alimentos (4 = Mayor Vulnerabilidad)
    mapeo_variedad_binario = {
      'NO': 4,
      'SI': 1
             }

    # 1. Limpieza de texto (fundamental para binarias)
    df['Variedad_alimentos'] = df['Variedad_alimentos'].astype(str).str.strip().str.upper()

    # 2. Aplicar el mapeo
    df['Variedad_alimentos'] = df['Variedad_alimentos'].map(mapeo_variedad_binario)

    # 3. Tratamiento de NaNs (si el texto original era diferente a 'SI' o 'NO'): imputar a 0 (missing)
    df['Variedad_alimentos'] = df['Variedad_alimentos'].fillna(0)
    
    
    #grupo economico
    
    # Mapeo de VULNERABILIDAD para el Alcance de Ingresos (4=Peor)
    mapeo_alcance_ingresos_vulnerabilidad = {
       'Nunca alcanzan para cubrir todos los gastos': 4,
       'Algunas veces no alcanzan para cubrir todos los gastos': 3,
       'Siempre alcanzan para cubrir todos los gastos': 1
             }

    # Aplicar el mapeo (asumiendo que el texto ya fue limpiado a este formato)
    df['Alcance_de_ingresos_hogar'] = df['Alcance_de_ingresos_hogar'].map(mapeo_alcance_ingresos_vulnerabilidad)
    # Si tienes valores no mapeados (e.g., "No Sabe"), asume que son missing y llénalos con 0.
    df['Alcance_de_ingresos_hogar'] = df['Alcance_de_ingresos_hogar'].fillna(0)
    # Asegúrate de que la columna es numérica (float o int) y maneja NaNs si es necesario
    df['Satisfacción_ingresos'] = pd.to_numeric(df['Satisfacción_ingresos'], errors='coerce').fillna(0)
    # El rango es de 0 a 10, pero usaremos el min/max real de los datos por seguridad
    min_val = df['Satisfacción_ingresos'].min()
    max_val = df['Satisfacción_ingresos'].max()
    # Paso 1 y 2: Normalizar e Invertir (para que 10 se mapee cerca de 0)
    x_norm = (df['Satisfacción_ingresos'] - min_val) / (max_val - min_val)
    x_invertido = 1 - x_norm  # Inversión: Mayor satisfacción -> Menor puntuación (vulnerabilidad)
    # Paso 3: Re-escalar a [1, 4]
    df['Satisfacción_ingresos_v'] = 1 + 3 * x_invertido

    # Opcional: reemplazar la columna original con la nueva puntuación
    df['Satisfacción_ingresos'] = df['Satisfacción_ingresos_v']

    # 1. Definir el umbral de referencia del DANE (Línea de Pobreza Per Cápita Nacional 2024)
    LINEA_POBREZA_PER_CAPITA_C = 460198.0  # COP $460.198
    LINEA_EXTREMA = 0.5 * LINEA_POBREZA_PER_CAPITA_C # $230.099
    LINEA_HOLGURA = 2.0 * LINEA_POBREZA_PER_CAPITA_C # $920.396
   
    df['Ingresos_mensuales'] = pd.to_numeric(df['Ingresos_mensuales'], errors='coerce').fillna(0)
    df['Número_personas_en_hogar'] = pd.to_numeric(df['Número_personas_en_hogar'],
                                                    errors='coerce').fillna(1).clip(lower=1)
    # 3. Calcular el Ingreso Mensual Per Cápita
    df['Ingreso_per_capita'] = df['Ingresos_mensuales'] / df['Número_personas_en_hogar']
    # 4. Definir las condiciones de vulnerabilidad (de la MÁXIMA a la MÍNIMA)
    conditions = [
        # Condición 4 (Máxima Vulnerabilidad): Bajo la Línea de Pobreza Extrema
       (df['Ingreso_per_capita'] < LINEA_EXTREMA),

        # Condición 3 (Alta Vulnerabilidad): Entre Línea Extrema y Línea de Pobreza
       (df['Ingreso_per_capita'] >= LINEA_EXTREMA) & (df['Ingreso_per_capita'] < LINEA_POBREZA_PER_CAPITA_C),

        # Condición 2 (Moderada Vulnerabilidad): Entre 1x y 2x Línea de Pobreza
       (df['Ingreso_per_capita'] >= LINEA_POBREZA_PER_CAPITA_C) & (df['Ingreso_per_capita'] < LINEA_HOLGURA),
  
        # Condición 1 (Baja Vulnerabilidad): Ingreso mayor a 2x la Línea de Pobreza
       (df['Ingreso_per_capita'] >= LINEA_HOLGURA)
                  ]   
    # 5. Definir las puntuaciones
    choices = [4, 3, 2, 1]

    # 6. Aplicar la lógica condicional y crear la variable de vulnerabilidad
    df['Ingresos_mensuales_v'] = np.select(conditions, choices, default=4) # default=4 para cualquier caso no cubierto (ej. si el ingreso es 0) 

    # 7. Reemplazar la columna original para el índice final
    df['Ingresos_mensuales'] = df['Ingresos_mensuales_v']

  
    df['Satisfacción_ingresos'] = pd.to_numeric(df['Satisfacción_ingresos'], errors='coerce').fillna(0)

    # 2. Definir el rango real de la variable
    # Dado que se indica que va de 0 a 10, y que queremos mantener los outliers,
    # usaremos el min/max observado en la data, que debería ser 0 y 10.
    min_val = df['Satisfacción_ingresos'].min()
    max_val = df['Satisfacción_ingresos'].max()

    # 3. Normalizar e Invertir la escala

    if max_val == min_val:
       # Si todos los valores son iguales, asignar una puntuación neutra o baja.
       df['Satisfacción_ingresos_v'] = 1
    else:
    # 3.1. Normalizar a [0, 1] (Directa: 10/Máxima Satisfacción -> 1)
      x_norm = (df['Satisfacción_ingresos'] - min_val) / (max_val - min_val)

    # 3.2. Invertir (para que Alta Satisfacción tenga puntuación BAJA)
      x_invertido = 1 - x_norm # Alta Insatisfacción/Baja Satisfacción -> 1

    # 3.3. Re-escalar a [1, 4]
      df['Satisfacción_ingresos_v'] = 1 + 3 * x_invertido

    # 4. Reemplazar la columna original
    df['Satisfacción_ingresos'] = df['Satisfacción_ingresos_v']

    # Mapeo universal para variables binarias de riesgo (4 = Sí, 1 = No)
    mapeo_riesgo_binario = {
       'SI': 4,
       'NO': 1
       }
    columnas_binarias_carencia = ['Saltar_comida', 'Hambre_no_comio', 'Falta_dinero']

    for col in columnas_binarias_carencia:
       # 1. Limpiar y estandarizar el texto (vital para que 'SI' y 'NO' coincidan)
       df[col] = df[col].astype(str).str.strip().str.upper()

       # 2. Aplicar el mapeo de riesgo
       df[col] = df[col].map(mapeo_riesgo_binario)

       # 3. Tratar NaNs (valores no mapeados): asumimos 0 (missing/desconocido)
       df[col] = df[col].fillna(0)

    # Mapeo universal para variables binarias de riesgo demográfico (4 = Sí, 1 = No)
    mapeo_riesgo_demografico = {
      'SI': 4,
      'NO': 1
     }
    columnas_demograficas_binarias = ['Menores_5_años_en_hogar', 'Mayores_de_60_años']
    for col in columnas_demograficas_binarias:
       # 1. Limpiar y estandarizar el texto (a mayúsculas y sin espacios)
       df[col] = df[col].astype(str).str.strip().str.upper()

       # 2. Aplicar el mapeo de riesgo
       df[col] = df[col].map(mapeo_riesgo_demografico)

       # 3. Tratar NaNs (valores no mapeados): asumimos 0 (missing/desconocido)
       df[col] = df[col].fillna(0)


    df['Número_personas_en_hogar'] = pd.to_numeric(df['Número_personas_en_hogar'], 
                                                   errors='coerce').fillna(1).clip(lower=1)
    # 2. Definir las condiciones (de la más vulnerable a la menos vulnerable)
    # 2. Definir las condiciones (de la más vulnerable a la menos vulnerable)
    conditions = [
       # Máxima Vulnerabilidad (Puntuación 4): 6 o más personas
      (df['Número_personas_en_hogar'] >= 6),

       # Alta Vulnerabilidad (Puntuación 3): 4 o 5 personas (El punto crítico de referencia del DANE)
      (df['Número_personas_en_hogar'] >= 4) & (df['Número_personas_en_hogar'] <= 5),

       # Moderada Vulnerabilidad (Puntuación 2): 3 personas
      (df['Número_personas_en_hogar'] == 3),

       # Baja Vulnerabilidad (Puntuación 1): 1 o 2 personas
      (df['Número_personas_en_hogar'] <= 2)
           ]
     # 3. Definir las puntuaciones correspondientes
    choices = [4, 3, 2, 1]
    # 4. Aplicar la lógica condicional
    df['Número_personas_en_hogar_v'] = np.select(conditions, choices, default=4) # default=4 para cualquier valor inconsistente/error no cubierto
    # 5. Reemplazar la columna original
    df['Número_personas_en_hogar'] = df['Número_personas_en_hogar_v']

    # PASO 1: DEFINIR LOS PESOS PARA CADA UNA DE TUS 13 COLUMNAS
    # NOTA: La suma de todos los valores debe ser 1.0 (100%)
    pesos = {
    'Ingresos_mensuales': 0.15,               # Alto peso, objetivo
    'Hambre_no_comio': 0.15,                  # Alto peso, carencia extrema
    'Falta_dinero': 0.10,                     # Medio-alto peso
    'Alcance_de_ingresos_hogar': 0.05,        # Medio-bajo peso, percepción
    
    'Consumo_proteínas': 0.075,
    'Consumo_frutas_verduras': 0.075,
    'Consumo_lácteos': 0.075,
    'Variedad_alimentos': 0.075,
    
    'Saltar_comida': 0.05,
    
    'Número_personas_en_hogar': 0.05,
    'Menores_5_años_en_hogar': 0.03,
    'Mayores_de_60_años': 0.03,
    'Satisfacción_ingresos': 0.02,            # Bajo peso, subjetivo
    }
    #VARIABLE FINAL (ÍNDICE)
    df['Indice_Vulnerabilidad'] = 0
    COLUMNAS_ANALISIS = list(pesos.keys())
    # Calcular la suma ponderada
    for col, peso in pesos.items():
       df['Indice_Vulnerabilidad'] += df[col] * peso

    bins = [0.99, 2.00, 3.00, 3.50, 4.01]  # Los límites deben cubrir el rango [1, 4]
    labels = ['Baja', 'Moderada', 'Alta', 'Crítica']
    # 2. Aplicar la función pd.cut para categorizar el índice final
    df['Nivel_Vulnerabilidad'] = pd.cut(
       df['Indice_Vulnerabilidad'],
       bins=bins,
       labels=labels,
       right=False,  # Importante: El intervalo es [a, b), excepto el último (3.50 a 4.00]
       include_lowest=True
    )
    # 3. (Opcional) Crear una versión numérica si es necesario (1, 2, 3, 4)
    # Puedes usar los códigos de las categorías si necesitas una variable ordinal numérica:
    df['Nivel_Vulnerabilidad_num'] = df['Nivel_Vulnerabilidad'].cat.codes + 1
   
    
   

    st.write("### 📊 Distribución de Hogares por Nivel de Vulnerabilidad")
    # Es mejor usar la variable categórica para un conteo y visualización en barras
    conteo_vulnerabilidad = df['Nivel_Vulnerabilidad'].value_counts().sort_index()
    # 1. Crear la figura y los ejes de Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    # 2. Generar el gráfico de barras
    sns.barplot(
       x=conteo_vulnerabilidad.index,
    y=conteo_vulnerabilidad.values,
    ax=ax,
    palette='Reds_d' # Puedes elegir la paleta que desees, 'Reds_d' para un gradiente de riesgo
      )
    # 3. Añadir etiquetas y título
    ax.set_title('Conteo de Hogares por Nivel de Vulnerabilidad', fontsize=16)
    ax.set_xlabel('Nivel de Vulnerabilidad', fontsize=12)
    ax.set_ylabel('Número de Hogares', fontsize=12)
    ax.tick_params(axis='x', rotation=0) # Asegura que las etiquetas del eje X estén planas

    # Opcional: Añadir el conteo exacto sobre cada barra
    for i, v in enumerate(conteo_vulnerabilidad.values):
       ax.text(i, v + 50, str(v), ha='center', va='bottom', fontsize=10)

    # 4. Mostrar el gráfico en Streamlit
    st.pyplot(fig)

    # Opcional: Mostrar la tabla de conteo
    st.write("#### Conteo Numérico de la Distribución")
    st.dataframe(conteo_vulnerabilidad.reset_index().rename(columns={'index': 'Nivel', 'Nivel_Vulnerabilidad': 'Conteo'}))

    st.write("### 🔍 Análisis Bivariado: Vulnerabilidad por Factores Socio-Demográficos")
    # 1. Aseguramos el orden de la variable final de riesgo
    orden_vulnerabilidad = ['Baja', 'Moderada', 'Alta', 'Crítica']
    df['Nivel_Vulnerabilidad'] = pd.Categorical(df['Nivel_Vulnerabilidad'], categories=orden_vulnerabilidad, ordered=True)
    # 2. Variables seleccionadas para el análisis
    variables_analisis = {
       'Estrato': 'Distribución de Estrato Socioeconómico',
    'Nivel_escolaridad': 'Distribución por Nivel de Escolaridad',
    'Ocupacion_actual': 'Distribución por Ocupación Actual',
    'Estado_civil': 'Distribución por Estado Civil',
    'Sexo': 'Distribución por Sexo'
       }
    
    # Limpieza y Agrupación inicial de categorías para mejorar la visualización
    for col in variables_analisis.keys():
       # Limpieza básica
       df[col] = df[col].astype(str).str.strip().str.upper().replace('NAN', 'NO ESPECIFICADO')
    
       # Agrupación para Escolaridad (Simplificar el eje X)
       if col == 'Nivel_escolaridad':
          df[col] = df[col].replace({
            'PREESCOLAR': 'PRIMARIA INCOMPLETA',
            'NINGUNO': 'SIN ESCOLARIDAD',
            'TÉCNICO/TECNÓLOGO': 'TÉCNICO O TECNÓLOGO',
            'POSGRADO': 'SUPERIOR/POSGRADO'
              })
          
        # Agrupación para Ocupación (Reducir categorías pequeñas)
       if col == 'Ocupacion_actual':
          df[col] = df[col].replace({
            'PENSIONADO': 'INACTIVO/OTRO',
            'ESTUDIANTE': 'INACTIVO/OTRO',
            'JUBILADO': 'INACTIVO/OTRO',
            'BUSCA TRABAJO': 'DESEMPLEADO'
            })
          # Mantener solo las 6 categorías principales para la gráfica
          top_ocupaciones = df[col].value_counts().nlargest(6).index
          df.loc[~df[col].isin(top_ocupaciones), col] = 'OTRA / NO ESPECIFICADA'

    # 3. Generación de gráficos para cada variable
    for col, titulo in variables_analisis.items():
       st.write(f"#### {titulo}")   
       # Crear tabla de contingencia: Porcentaje de cada categoría DENTRO de cada nivel de vulnerabilidad
       contingency_table = pd.crosstab(df['Nivel_Vulnerabilidad'], df[col], normalize='index') * 100
       # Generar el gráfico de barras apiladas
       fig, ax = plt.subplots(figsize=(12, 6))

       # Usar un mapa de colores que ayude a diferenciar las categorías
       contingency_table.plot(
          kind='bar',
        stacked=True,
        ax=ax,
        colormap='viridis' # Excelente para diferenciar múltiples categorías
            )
       
         # Formato del gráfico
       ax.set_title(f'Distribución de {col} por Nivel de Vulnerabilidad', fontsize=16)
       ax.set_xlabel('Nivel de Vulnerabilidad', fontsize=12)
       ax.set_ylabel('Porcentaje (%)', fontsize=12)
       ax.legend(title=col, loc='upper left', bbox_to_anchor=(1.05, 1)) # Leyenda fuera del gráfico
       plt.xticks(rotation=0)
       plt.tight_layout()
    
       # Mostrar el gráfico en Streamlit
       st.pyplot(fig)
    
       # Opcional: Mostrar la tabla de porcentajes
       st.dataframe(contingency_table.style.format('{:.1f}%'))


    st.write("### 🌎 Análisis Geográfico: Distribución de la Vulnerabilidad")
    st.markdown("El mapa interactivo muestra la concentración de los hogares por Nivel de Vulnerabilidad.")
    
    # ⚠️ ASUMIMOS que la columna de coordenadas se llama 'UBICACION_PREDEFINIDA'
    columna_ubicacion = 'UBICACION_PREDEFINIDA' 

    # Verificar si la columna existe y no está vacía
    if columna_ubicacion in df.columns and df[columna_ubicacion].dropna().shape[0] > 0:
        
        # Separar las coordenadas (ASUMIENDO el formato "lat,lon")
        try:
            df[['lat', 'lon']] = df[columna_ubicacion].astype(str).str.split(',', expand=True)
            df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
            df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
        except:
            st.warning(f"No se pudo parsear la columna '{columna_ubicacion}'. Verifique el formato 'lat,lon'.")
            # Si hay un error de formato, terminamos la ejecución del mapa aquí
            pass
        
        # Eliminar filas con coordenadas no válidas (NaN) después del parseo
        df_mapa = df.dropna(subset=['lat', 'lon']).copy()

        if df_mapa.empty:
            st.error("No hay datos de ubicación válidos para generar el mapa.")
        else:
            # --- 2. DEFINIR COLORES Y NIVELES ---
            colores = {
                'Baja': 'green',
                'Moderada': 'lightgreen',
                'Alta': 'orange',
                'Crítica': 'red'
            }

            # --- 3. CREAR EL MAPA ---
            # Centrar el mapa en el promedio de las coordenadas de los datos válidos
            m = folium.Map(location=[df_mapa['lat'].mean(), df_mapa['lon'].mean()], zoom_start=11)

            # Crear un clúster para agrupar puntos
            marker_cluster = MarkerCluster().add_to(m)

            # --- 4. AÑADIR LOS PUNTOS AL MAPA ---
            for index, row in df_mapa.iterrows():
                nivel = row['Nivel_Vulnerabilidad']
                color = colores.get(nivel, 'gray') # 'gray' si no se encuentra el nivel
                
                folium.CircleMarker(
                    location=[row['lat'], row['lon']],
                    radius=3, 
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7,
                    tooltip=f"Vulnerabilidad: {nivel}",
                    popup=f"Nivel: {nivel} ({row['Indice_Vulnerabilidad']:.2f})"
                ).add_to(marker_cluster)

            # --- 5. MOSTRAR EL MAPA EN STREAMLIT ---
            # El método esencial para mostrar Folium en Streamlit
            map_html = m._repr_html_()
            components.html(map_html, height=800)

    else:
        st.warning(f"La columna de ubicación '{columna_ubicacion}' no existe o no contiene datos válidos.")