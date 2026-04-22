"""
Universidad Statistics - Interfaz Web
Analiza datos de estudiantes, cursos e inscripciones desde archivos binarios
"""
import streamlit as st
import struct
from collections import defaultdict
from typing import List, Dict

# ============================================================
# HELPERS - Lectura de datos binarios ( endianness )
# ============================================================

def read_u16_be(data: bytes, offset: int) -> int:
    """Lee un uint16_t en Big Endian"""
    return struct.unpack('>H', data[offset:offset+2])[0]

def read_u32_le(data: bytes, offset: int) -> int:
    """Lee un uint32_t en Little Endian"""
    return struct.unpack('<I', data[offset:offset+4])[0]

# ============================================================
# ESTRUCTURAS DE DATOS
# ============================================================

class Student:
    def __init__(self, data: bytes, offset: int):
        self.student_id = read_u32_le(data, offset)
        self.flags = data[offset + 4]
        self.name = data[offset + 5:offset + 5 + 23].decode('latin-1').rstrip('\x00')
        self.age = read_u32_le(data, offset + 28)

class Course:
    def __init__(self, data: bytes, offset: int):
        self.course_id = read_u32_le(data, offset)
        self.name = data[offset + 4:offset + 4 + 32].decode('latin-1').rstrip('\x00')
        self.credit_hours = read_u32_le(data, offset + 36)

class Enrollment:
    def __init__(self, data: bytes, offset: int):
        self.student_id = read_u32_le(data, offset)
        self.course_id = read_u32_le(data, offset + 4)
        self.year = read_u32_le(data, offset + 8)
        self.semester = read_u32_le(data, offset + 12)

class SemesterStats:
    def __init__(self, year_sem_key: int):
        self.year_sem_key = year_sem_key
        self.male_undergrad = 0
        self.female_undergrad = 0
        self.male_grad = 0
        self.female_grad = 0
    
    @property
    def year(self) -> int:
        return self.year_sem_key // 10
    
    @property
    def semester(self) -> int:
        return self.year_sem_key % 10
    
    @property
    def total(self) -> int:
        return self.male_undergrad + self.female_undergrad + self.male_grad + self.female_grad

# ============================================================
# PROCESAMIENTO PRINCIPAL
# ============================================================

def process_binary_file(file_bytes: bytes) -> Dict:
    """Procesa el archivo binario y devuelve estadísticas"""
    
    offset = 0
    
    # 1. Leer Header (14 bytes)
    magic = read_u16_be(file_bytes, offset)
    if magic != 0xaaae:
        raise ValueError(f"Formato de archivo inválido. Magic esperado: 0xaaae, encontrado: 0x{magic:04x}")
    
    student_count = read_u32_le(file_bytes, offset + 2)
    course_count = read_u32_le(file_bytes, offset + 6)
    enrollment_count = read_u32_le(file_bytes, offset + 10)
    offset += 14
    
    # 2. Cargar Estudiantes
    students = {}
    for _ in range(student_count):
        student = Student(file_bytes, offset)
        students[student.student_id] = student
        offset += 32
    
    # 3. Cargar Cursos
    courses = {}
    for _ in range(course_count):
        course = Course(file_bytes, offset)
        courses[course.course_id] = course
        offset += 40
    
    # 4. Cargar Enrollments
    enrollments = []
    for _ in range(enrollment_count):
        enrollment = Enrollment(file_bytes, offset)
        enrollments.append(enrollment)
        offset += 16
    
    # 5. Procesar estadísticas (evitar duplicados por estudiante/periodo)
    seen = set()
    stats_dict = defaultdict(SemesterStats)
    
    for enrollment in enrollments:
        year_sem_key = enrollment.year * 10 + enrollment.semester
        key = (enrollment.student_id, year_sem_key)
        
        if key not in seen:
            seen.add(key)
            
            student = students.get(enrollment.student_id)
            if student:
                is_female = (student.flags & 0x80) != 0
                is_undergrad = student.age < 25
                
                if year_sem_key not in stats_dict:
                    stats_dict[year_sem_key] = SemesterStats(year_sem_key)
                
                stats = stats_dict[year_sem_key]
                if is_undergrad:
                    if is_female:
                        stats.female_undergrad += 1
                    else:
                        stats.male_undergrad += 1
                else:
                    if is_female:
                        stats.female_grad += 1
                    else:
                        stats.male_grad += 1
    
    # Ordenar resultados
    sorted_stats = sorted(stats_dict.values(), key=lambda x: x.year_sem_key)
    
    # 6. Calcular estadísticas de edad por curso
    course_ages = {}
    for course_id, course in courses.items():
        enrolled_students = [students[e.student_id] for e in enrollments if e.course_id == course_id and e.student_id in students]
        if enrolled_students:
            avg_age = sum(s.age for s in enrolled_students) / len(enrolled_students)
            course_ages[course_id] = {
                'name': course.name,
                'avg_age': avg_age,
                'count': len(enrolled_students)
            }

    return {
        'student_count': student_count,
        'course_count': course_count,
        'enrollment_count': enrollment_count,
        'stats': sorted_stats,
        'students_dict': students,
        'courses_dict': course_ages
    }

# ============================================================
# INTERFAZ STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Universidad Statistics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Universidad Statistics")
st.markdown("### Análisis de Inscripciones Estudiantiles")

# Sidebar para información
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

# Carga de archivo
uploaded_file = st.file_uploader(
    "📤 Cargar archivo de datos binarios",
    type=['bin', 'dat', 'raw'],
    help="Selecciona un archivo binario con el formato especificado"
)

if uploaded_file is not None:
    try:
        file_bytes = uploaded_file.read()
        
        with st.spinner('Procesando archivo...'):
            result = process_binary_file(file_bytes)
        
        # Mostrar estadísticas generales
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Estudiantes", result['student_count'])
        with col2:
            st.metric("Total Cursos", result['course_count'])
        with col3:
            st.metric("Total Inscripciones", result['enrollment_count'])
        
        st.divider()
        
        # Tabla de resultados
        st.subheader("📈 Estadísticas por Período")
        
        if result['stats']:
            # Crear dataframe para mostrar
            import pandas as pd
            
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
            
            # Gráficos
            st.subheader("📉 Visualización")
            
            tab1, tab2, tab3 = st.tabs(["Barras", "Torta", "Evolución"])
            
            with tab1:
                st.bar_chart(df.set_index('Año')[['Masculino Pregrado', 'Femenino Pregrado', 
                                                    'Masculino Posgrado', 'Femenino Posgrado']])
            
            with tab2:
                if len(df) > 0:
                    # Último período
                    last = df.iloc[-1]
                    chart_data = {
                        'Categoría': ['Masc. Pregrado', 'Fem. Pregrado', 'Masc. Posgrado', 'Fem. Posgrado'],
                        'Cantidad': [last['Masculino Pregrado'], last['Femenino Pregrado'], 
                                    last['Masculino Posgrado'], last['Femenino Posgrado']]
                    }
                    st.bar_chart(pd.DataFrame(chart_data).set_index('Categoría'))
            
            with tab3:
                st.line_chart(df.set_index('Año')['Total'])
        
        # -------------------------------------------------------------
        # FILTRO: Estudiantes por Rango de Edad
        # -------------------------------------------------------------
        st.divider()
        st.subheader("👥 Estudiantes por Rango de Edad")
        
        students_dict = result.get('students_dict', {})
        ages = [s.age for s in students_dict.values()]
        
        if ages:
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
        
        # -------------------------------------------------------------
        # FILTRO: Cursos con Edad Promedio
        # -------------------------------------------------------------
        st.divider()
        st.subheader("📚 Cursos con Edad Promedio")
        
        courses_dict = result.get('courses_dict', {})
        
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
            
            # Gráfico de barras
            st.bar_chart(df_courses.set_index('Curso')['Edad Promedio'])
        else:
            st.warning("No hay información de cursos disponibles.")
            
    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {str(e)}")
        st.exception(e)
else:
    # Mensaje inicial
    st.info("👆 Carga un archivo binario para comenzar el análisis")
    
    # Mostrar ejemplo de uso
    st.subheader("� Ejemplo de Uso")
    st.markdown("""
    1. Haz clic en **"Cargar archivo de datos binarios"**
    2. Selecciona un archivo `.bin`, `.dat` o `.raw`
    3. Espera a que se procesen los datos
    4. Explora las estadísticas y gráficos
    
    > **Nota:** El archivo debe tener el formato binario específico descrito en el panel lateral.
    """)
