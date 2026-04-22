"""
Procesamiento principal de archivos binarios
"""
from typing import Dict, List
from collections import defaultdict

from src.binary.reader import read_u16_be, read_u32_le
from src.models.entities import Student, Course, Enrollment
from src.models.stats import SemesterStats
from src.processors.statistics import calculate_course_statistics


def process_binary_file(file_bytes: bytes) -> Dict:
    """
    Procesa un archivo binario de datos universitarios y retorna todas las estadísticas
    
    Args:
        file_bytes: Contenido del archivo binario
        
    Returns:
        Diccionario con toda la información procesada:
        - student_count: Total de estudiantes
        - course_count: Total de cursos
        - enrollment_count: Total de inscripciones
        - stats: Lista de SemesterStats ordenada por período
        - students_dict: Diccionario {student_id: Student}
        - courses_dict: Diccionario {course_id: {'name', 'avg_age', 'count'}}
        
    Raises:
        ValueError: Si el archivo tiene un formato inválido
    """
    offset = 0
    
    # 1. Leer Header (14 bytes)
    magic = read_u16_be(file_bytes, offset)
    if magic != 0xaaae:
        raise ValueError(
            f"Formato de archivo inválido. Magic esperado: 0xaaae, encontrado: 0x{magic:04x}"
        )
    
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
    
    # 5. Procesar estadísticas por semestre (evitar duplicados por estudiante/período)
    semester_stats = _calculate_semester_stats(enrollments, students)
    sorted_stats = sorted(semester_stats.values(), key=lambda x: x.year_sem_key)
    
    # 6. Calcular estadísticas de edad por curso
    course_ages = calculate_course_statistics(courses, enrollments, students)
    
    return {
        'student_count': student_count,
        'course_count': course_count,
        'enrollment_count': enrollment_count,
        'stats': sorted_stats,
        'students_dict': students,
        'courses_dict': course_ages
    }


def _calculate_semester_stats(enrollments: List[Enrollment], students: Dict) -> Dict[int, SemesterStats]:
    """
    Calcula las estadísticas por semestre, evitando duplicados de estudiante/período
    
    Args:
        enrollments: Lista de inscripciones
        students: Diccionario de estudiantes
        
    Returns:
        Diccionario {year_sem_key: SemesterStats}
    """
    seen = set()
    stats_dict = defaultdict(SemesterStats)
    
    for enrollment in enrollments:
        year_sem_key = enrollment.year_sem_key
        key = (enrollment.student_id, year_sem_key)
        
        # Evitar contar el mismo estudiante dos veces en el mismo período
        if key not in seen:
            seen.add(key)
            
            student = students.get(enrollment.student_id)
            if student:
                year_sem_key = enrollment.year_sem_key
                
                if year_sem_key not in stats_dict:
                    stats_dict[year_sem_key] = SemesterStats(year_sem_key)
                
                stats = stats_dict[year_sem_key]
                
                # Clasificar por género y nivel
                if student.is_undergrad():
                    if student.is_female():
                        stats.female_undergrad += 1
                    else:
                        stats.male_undergrad += 1
                else:
                    if student.is_female():
                        stats.female_grad += 1
                    else:
                        stats.male_grad += 1
    
    return stats_dict
