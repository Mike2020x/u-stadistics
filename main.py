"""
Punto de entrada principal de la aplicación
"""
import subprocess
import sys


def main():
    """Inicia la aplicación Streamlit"""
    try:
        # Ejecutar Streamlit
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "app.py"],
            cwd=".",
            check=False
        )
    except Exception as e:
        print(f"Error al ejecutar la aplicación: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
