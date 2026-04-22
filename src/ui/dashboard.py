"""
Componentes principales del dashboard
"""
import streamlit as st
import pandas as pd


def render_header():
    """Renderiza el encabezado de la aplicación"""
    st.set_page_config(
        page_title="Universidad Statistics",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Universidad Statistics")
    st.markdown("### Análisis de Inscripciones Estudiantiles")


def render_sidebar():
    """Renderiza la barra lateral con información"""
    with st.sidebar:
        st.header("ℹ️ Acerca de")
        st.info("""
        Esta aplicación procesa archivos binarios con datos de estudiantes universitarios.
        
        **Formato esperado:**
        - Header: 14 bytes
        - Estudiantes: 32 bytes c/u
        - Cursos: 40 bytes c/u
        - Inscripciones: 16 bytes c/u
        """)
        
        st.header("📁 Formato de Archivo")
        st.code("""
Header:
- magic: uint16_t (BE) = 0xAAAE
- student_count: uint32_t (LE)
- course_count: uint32_t (LE)
- enrollment_count: uint32_t (LE)

Student (32 bytes):
- student_id: uint32_t
- flags: uint8_t (bit 7 = género)
- name: char[23]
- age: uint32_t

Course (40 bytes):
- course_id: uint32_t
- name: char[32]
- credit_hours: uint32_t

Enrollment (16 bytes):
- student_id: uint32_t
- course_id: uint32_t
- year: uint32_t
- semester: uint32_t
        """, language="text")


def render_metrics(result: dict):
    """
    Renderiza las métricas generales
    
    Args:
        result: Diccionario con los datos procesados
    """
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Estudiantes", result['student_count'])
    with col2:
        st.metric("Total Cursos", result['course_count'])
    with col3:
        st.metric("Total Inscripciones", result['enrollment_count'])


def render_stats_table(result: dict):
    """
    Renderiza la tabla de estadísticas por período
    
    Args:
        result: Diccionario con los datos procesados
    """
    st.subheader("📈 Estadísticas por Período")
    
    if result['stats']:
        # Crear dataframe para mostrar
        data = []
        for stat in result['stats']:
            data.append({
                'Año': stat.year,
                'Semestre': stat.semester,
                'Masculino Pregrado': stat.male_undergrad,
                'Femenino Pregrado': stat.female_undergrad,
                'Masculino Posgrado': stat.male_grad,
                'Femenino Posgrado': stat.female_grad,
                'Total': stat.total
            })
        
        df = pd.DataFrame(data)
        
        # Mostrar tabla
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        return df
    
    return None


def render_age_filter(students_dict: dict) -> list:
    """
    Renderiza filtro de rango de edad y retorna estudiantes filtrados
    
    Args:
        students_dict: Diccionario de estudiantes
        
    Returns:
        Lista de estudiantes filtrados
    """
    st.divider()
    st.subheader("👥 Estudiantes por Rango de Edad")
    
    ages = [s.age for s in students_dict.values()]
    
    if not ages:
        st.warning("No hay estudiantes disponibles.")
        return []
    
    min_age, max_age = min(ages), max(ages)
    
    # Slider para rango de edad
    age_range = st.slider(
        "Seleccionar rango de edad",
        min_value=int(min_age),
        max_value=int(max_age),
        value=(int(min_age), int(max_age)),
        key="age_filter"
    )
    
    # Filtrar estudiantes
    filtered_students = [
        {'ID': s.student_id, 'Nombre': s.name, 'Edad': s.age}
        for s in students_dict.values()
        if age_range[0] <= s.age <= age_range[1]
    ]
    
    if filtered_students:
        df_ages = pd.DataFrame(filtered_students)
        st.dataframe(
            df_ages,
            column_config={
                'ID': st.column_config.NumberColumn("ID Estudiante"),
                'Nombre': st.column_config.TextColumn("Nombre"),
                'Edad': st.column_config.NumberColumn("Edad"),
            },
            hide_index=True,
            width='stretch'
        )
        st.caption(f"Total: {len(filtered_students)} estudiantes en el rango de edad {age_range[0]}-{age_range[1]}")
    else:
        st.warning("No hay estudiantes en este rango de edad.")
    
    return filtered_students


def render_courses_section(courses_dict: dict):
    """
    Renderiza la sección de cursos con edad promedio
    
    Args:
        courses_dict: Diccionario con información de cursos
    """
    st.divider()
    st.subheader("📚 Cursos con Edad Promedio")
    
    if courses_dict:
        # Crear dataframe de cursos
        course_data = []
        for cid, info in courses_dict.items():
            course_data.append({
                'Curso': info['name'],
                'Edad Promedio': round(info['avg_age'], 1),
                'Estudiantes Inscritos': info['count']
            })
        
        # Ordenar por edad promedio
        df_courses = pd.DataFrame(course_data).sort_values('Edad Promedio', ascending=False)
        
        # Mostrar tabla
        st.dataframe(
            df_courses,
            column_config={
                'Curso': st.column_config.TextColumn("Nombre del Curso"),
                'Edad Promedio': st.column_config.NumberColumn("Edad Promedio", format="%.1f"),
                'Estudiantes Inscritos': st.column_config.NumberColumn("Cantidad"),
            },
            hide_index=True,
            width='stretch'
        )
        
        return df_courses
    else:
        st.warning("No hay información de cursos disponibles.")
        return None


def render_empty_state():
    """Renderiza el estado vacío cuando no hay archivo cargado"""
    st.info("👆 Carga un archivo binario para comenzar el análisis")
    
    # Mostrar ejemplo de uso
    st.subheader("📋 Ejemplo de Uso")
    st.markdown("""
    1. Haz clic en **"Cargar archivo de datos binarios"**
    2. Selecciona un archivo `.bin`, `.dat` o `.raw`
    3. Espera a que se procesen los datos
    4. Explora las estadísticas y gráficos
    
    > **Nota:** El archivo debe tener el formato binario específico descrito en el panel lateral.
    """)
