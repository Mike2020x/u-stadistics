"""
Entidades de datos para estudiantes, cursos e inscripciones
"""
from src.binary.reader import read_u32_le


class Student:
    """Representa un estudiante en el sistema"""
    
    def __init__(self, data: bytes, offset: int):
        """
        Crea una instancia de Student leyendo desde datos binarios
        
        Args:
            data: Buffer de bytes con los datos
            offset: Posición inicial del estudiante en el buffer
        """
        self.student_id = read_u32_le(data, offset)
        self.flags = data[offset + 4]
        self.name = data[offset + 5:offset + 5 + 23].decode('latin-1').rstrip('\x00')
        self.age = read_u32_le(data, offset + 28)
    
    def is_female(self) -> bool:
        """Retorna True si el estudiante es femenino (bit 7 del flag)"""
        return (self.flags & 0x80) != 0
    
    def is_undergrad(self) -> bool:
        """Retorna True si el estudiante es de pregrado (edad < 25)"""
        return self.age < 25


class Course:
    """Representa un curso en el sistema"""
    
    def __init__(self, data: bytes, offset: int):
        """
        Crea una instancia de Course leyendo desde datos binarios
        
        Args:
            data: Buffer de bytes con los datos
            offset: Posición inicial del curso en el buffer
        """
        self.course_id = read_u32_le(data, offset)
        self.name = data[offset + 4:offset + 4 + 32].decode('latin-1').rstrip('\x00')
        self.credit_hours = read_u32_le(data, offset + 36)


class Enrollment:
    """Representa una inscripción de estudiante en un curso"""
    
    def __init__(self, data: bytes, offset: int):
        """
        Crea una instancia de Enrollment leyendo desde datos binarios
        
        Args:
            data: Buffer de bytes con los datos
            offset: Posición inicial de la inscripción en el buffer
        """
        self.student_id = read_u32_le(data, offset)
        self.course_id = read_u32_le(data, offset + 4)
        self.year = read_u32_le(data, offset + 8)
        self.semester = read_u32_le(data, offset + 12)
    
    @property
    def year_sem_key(self) -> int:
        """Clave combinada año-semestre para agrupar"""
        return self.year * 10 + self.semester
