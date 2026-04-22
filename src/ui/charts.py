"""
Componentes de visualización (gráficos)
"""
import streamlit as st
import pandas as pd


def render_visualizations(df: pd.DataFrame):
    """
    Renderiza pestañas con diferentes visualizaciones
    
    Args:
        df: DataFrame con estadísticas por período
    """
    st.subheader("📉 Visualización")
    
    tab1, tab2, tab3 = st.tabs(["Barras", "Torta", "Evolución"])
    
    with tab1:
        render_bar_chart(df)
    
    with tab2:
        render_pie_chart(df)
    
    with tab3:
        render_evolution_chart(df)


def render_bar_chart(df: pd.DataFrame):
    """
    Renderiza gráfico de barras con categorías de estudiantes por año
    
    Args:
        df: DataFrame con estadísticas
    """
    st.bar_chart(df.set_index('Año')[
        ['Masculino Pregrado', 'Femenino Pregrado', 
         'Masculino Posgrado', 'Femenino Posgrado']
    ])


def render_pie_chart(df: pd.DataFrame):
    """
    Renderiza gráfico de torta del último período
    
    Args:
        df: DataFrame con estadísticas
    """
    if len(df) > 0:
        # Último período
        last = df.iloc[-1]
        chart_data = {
            'Categoría': ['Masc. Pregrado', 'Fem. Pregrado', 'Masc. Posgrado', 'Fem. Posgrado'],
            'Cantidad': [
                last['Masculino Pregrado'],
                last['Femenino Pregrado'],
                last['Masculino Posgrado'],
                last['Femenino Posgrado']
            ]
        }
        st.bar_chart(pd.DataFrame(chart_data).set_index('Categoría'))


def render_evolution_chart(df: pd.DataFrame):
    """
    Renderiza gráfico de línea con evolución total de estudiantes
    
    Args:
        df: DataFrame con estadísticas
    """
    st.line_chart(df.set_index('Año')['Total'])


def render_course_ages_chart(df_courses: pd.DataFrame):
    """
    Renderiza gráfico de barras con edad promedio por curso
    
    Args:
        df_courses: DataFrame con información de cursos
    """
    st.bar_chart(df_courses.set_index('Curso')['Edad Promedio'])
