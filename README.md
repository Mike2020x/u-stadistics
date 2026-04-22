# 📊 Universidad Statistics

Interfaz web para analizar datos de estudiantes universitarios desde archivos binarios.

## 🚀 Despliegue Gratuito en Streamlit Cloud

### Prerrequisitos
- Cuenta de GitHub (gratuita)

### Pasos para Desplegar

#### 1. Preparar el repositorio en GitHub

1. **Crea un nuevo repositorio en GitHub:**
   - Ve a [github.com/new](https://github.com/new)
   - Nombre: `universidad-statistics`
   - Visibilidad: Public
   - No inicialices con README

2. **Sube los archivos al repositorio:**
   ```bash
   # En la carpeta del proyecto
   git init
   git add app.py requirements.txt
   git commit -m "Initial commit - Universidad Statistics"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/universidad-statistics.git
   git push -u origin main
   ```

#### 2. Desplegar en Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Inicia sesión con tu cuenta de GitHub
3. Click en **"New app"**
4. Configura:
   - Repository: `TU_USUARIO/universidad-statistics`
   - Branch: `main`
   - Main file path: `app.py`
5. Click en **"Deploy!"**

¡Listo! En ~2 minutos tendrás tu aplicación en línea gratuitamente.

**URL típica:** `https://TU_USUARIO-universidad-statistics.streamlit.app`

---

## 💻 Uso Local

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/universidad-statistics.git
cd universidad-statistics

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar

```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

---

## 📁 Formato del Archivo Binario

El programa espera un archivo binario con el siguiente formato:

```
+---------------------------+
|         HEADER (14 bytes) |
+---------------------------+
|     STUDENTS (N * 32 bytes)|
+---------------------------+
|      COURSES (M * 40 bytes)|
+---------------------------+
| ENROLLMENTS (K * 16 bytes)|
+---------------------------+
```

### Header (14 bytes)
| Campo            | Tipo     | Endianness | Posición |
| ---------------- | -------- | ---------- | -------- |
| magic            | uint16_t | Big        | 0-1      |
| student_count    | uint32_t | Little     | 2-5      |
| course_count     | uint32_t | Little     | 6-9      |
| enrollment_count | uint32_t | Little     | 10-13    |

### Student (32 bytes)
| Campo      | Tipo     | Posición |
| ---------- | -------- | -------- |
| student_id | uint32_t | 0-3      |
| flags      | uint8_t  | 4        |
| name       | char[23] | 5-27     |
| age        | uint32_t | 28-31    |

### Course (40 bytes)
| Campo        | Tipo     | Posición |
| ------------ | -------- | -------- |
| course_id    | uint32_t | 0-3      |
| name         | char[32] | 4-35     |
| credit_hours | uint32_t | 36-39    |

### Enrollment (16 bytes)
| Campo      | Tipo     | Posición |
| ---------- | -------- | -------- |
| student_id | uint32_t | 0-3      |
| course_id  | uint32_t | 4-7      |
| year       | uint32_t | 8-11     |
| semester   | uint32_t | 12-15    |

---

## 📊 Funcionalidades

- ✅ Carga de archivos binarios (drag & drop)
- ✅ Validación de formato
- ✅ Estadísticas por período (año/semestre)
- ✅ Clasificación por género y tipo de estudiante
- ✅ Tablas interactivas
- ✅ Gráficos de barras, torta y evolución
- ✅ Diseño responsive

---

## 🛠️ Tecnologías

- **Python 3.8+**
- **Streamlit** - Framework web
- **Pandas** - Manipulación de datos

---

## 📝 Notas

- El archivo debe tener magic number `0xAAAE` para ser válido
- Estudiantes con edad < 25 se clasifican como pregrado
- Bit 7 de `flags` indica género (1 = Femenino, 0 = Masculino)
- Las estadísticas evitan duplicados: un estudiante solo se cuenta una vez por período
