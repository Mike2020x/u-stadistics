"""
Universidad Statistics - Interfaz Web
Analiza datos de estudiantes, cursos e inscripciones desde archivos binarios
"""
import streamlit as st

from src.processors.processor import process_binary_file
from src.ui.dashboard import (
    render_header,
    render_sidebar,
    render_metrics,
    render_stats_table,
    render_age_filter,
    render_courses_section,
    render_empty_state
)
from src.ui.charts import render_visualizations, render_course_ages_chart


def main():
    """Función principal de la aplicación"""
    # Configurar página y sidebar
    render_header()
    render_sidebar()
    
    # Carga de archivo
    uploaded_file = st.file_uploader(
        "📤 Cargar archivo de datos binarios",
        type=['bin', 'dat', 'raw'],
        help="Selecciona un archivo binario con el formato especificado"
    )
    
    if uploaded_file is not None:
        try:
            # Procesar archivo
            file_bytes = uploaded_file.read()
            
            with st.spinner('Procesando archivo...'):
                result = process_binary_file(file_bytes)
            
            # Mostrar métricas
            render_metrics(result)
            st.divider()
            
            # Tabla de estadísticas
            df = render_stats_table(result)
            
            if df is not None:
                # Visualizaciones
                render_visualizations(df)
            
            # Filtro de edad
            render_age_filter(result.get('students_dict', {}))
            
            # Sección de cursos
            df_courses = render_courses_section(result.get('courses_dict', {}))
            
            if df_courses is not None:
                # Gráfico de cursos
                render_course_ages_chart(df_courses)
                
        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {str(e)}")
            st.exception(e)
    else:
        # Mensaje inicial
        render_empty_state()


if __name__ == "__main__":
    main()
