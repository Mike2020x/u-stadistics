"""
Estadísticas por semestre académico
"""


class SemesterStats:
    """Agrupa estadísticas de estudiantes por semestre"""
    
    def __init__(self, year_sem_key: int):
        """
        Crea estadísticas para un período específico
        
        Args:
            year_sem_key: Clave combinada (año * 10 + semestre)
        """
        self.year_sem_key = year_sem_key
        self.male_undergrad = 0
        self.female_undergrad = 0
        self.male_grad = 0
        self.female_grad = 0
    
    @property
    def year(self) -> int:
        """Extrae el año de la clave"""
        return self.year_sem_key // 10
    
    @property
    def semester(self) -> int:
        """Extrae el semestre de la clave"""
        return self.year_sem_key % 10
    
    @property
    def total(self) -> int:
        """Calcula el total de estudiantes"""
        return self.male_undergrad + self.female_undergrad + self.male_grad + self.female_grad
    
    @property
    def total_undergrad(self) -> int:
        """Total de estudiantes de pregrado"""
        return self.male_undergrad + self.female_undergrad
    
    @property
    def total_grad(self) -> int:
        """Total de estudiantes de posgrado"""
        return self.male_grad + self.female_grad
