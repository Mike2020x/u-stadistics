"""
Cálculos estadísticos adicionales
"""
from typing import Dict, List

from src.models.entities import Student, Course, Enrollment


def calculate_course_statistics(
    courses: Dict[int, Course],
    enrollments: List[Enrollment],
    students: Dict[int, Student]
) -> Dict[int, Dict]:
    """
    Calcula estadísticas de edad por curso
    
    Args:
        courses: Diccionario de cursos
        enrollments: Lista de inscripciones
        students: Diccionario de estudiantes
        
    Returns:
        Diccionario {course_id: {'name', 'avg_age', 'count'}}
    """
    course_ages = {}
    
    for course_id, course in courses.items():
        # Obtener estudiantes inscritos en este curso
        enrolled_students = [
            students[e.student_id]
            for e in enrollments
            if e.course_id == course_id and e.student_id in students
        ]
        
        if enrolled_students:
            avg_age = sum(s.age for s in enrolled_students) / len(enrolled_students)
            course_ages[course_id] = {
                'name': course.name,
                'avg_age': avg_age,
                'count': len(enrolled_students)
            }
    
    return course_ages


def get_age_statistics(students: Dict[int, Student]) -> tuple:
    """
    Retorna estadísticas de edad de los estudiantes
    
    Args:
        students: Diccionario de estudiantes
        
    Returns:
        Tupla (min_age, max_age) o (None, None) si no hay estudiantes
    """
    if not students:
        return None, None
    
    ages = [s.age for s in students.values()]
    return min(ages), max(ages)
