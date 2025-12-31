# ProyectoTercerParcialAV
Proyecto para Análisis Vectorial sobre integrales dobles y triples.

# Calculadora de Integrales Dobles y Triples  
**Exactas vs Numéricas**

## Descripción del proyecto
Este proyecto consiste en una calculadora web desarrollada en Python que permite calcular integrales dobles y triples de forma:

- Exacta, utilizando cálculo simbólico con SymPy  
- *umérica, mediante métodos de integración aproximada usando SciPy o una malla tipo trapecio (grid) 

La aplicación permite comparar ambos resultados y analizar el error absoluto y relativo, lo cual es útil para comprender la diferencia entre métodos analíticos y numéricos en el cálculo integral.

El proyecto fue desarrollado como parte de la asignatura de Análisis Vectorial.

---

## Objetivos

### Objetivo general
Desarrollar una aplicación que calcule integrales dobles y triples, permitiendo comparar resultados exactos y numéricos para reforzar la comprensión del cálculo multivariable.

### Objetivos específicos
- Calcular integrales dobles y triples mediante métodos exactos.
- Implementar métodos de integración numérica.
- Comparar resultados exactos y aproximados.
- Analizar el error absoluto y relativo.
- Presentar los resultados mediante una interfaz web clara y sencilla.

---

## Alcance del proyecto
- La aplicación trabaja con funciones predefinidas para garantizar estabilidad y facilidad de uso.
- Se aceptan dominios rectangulares para integrales dobles y prismas rectangulares para integrales triples.
- El proyecto está enfocado en el análisis matemático, no en visualización avanzada.

---

## Tecnologías utilizadas

- Python 3
- Flask – Framework web
- SymPy – Cálculo simbólico
- NumPy – Operaciones numéricas
- SciPy – Integración numérica
- HTML / Css / JavaScript – Interfaz de usuario

---

## Estructura del proyecto

Proyecto Tercer Parcial/
├── app.py # Servidor Flask
├── integrales.py # Lógica de integrales exactas y numéricas
├── requerimientos.txt # Dependencias del proyecto
├── templates/
│ └── index.html # Interfaz principal
└── static/
├── css/
│ └── style.css # Estilos
└── js/
└── main.js # Interactividad básica


---

## Instalación y ejecución

### Clonar el repositorio
```bash
git clone https://github.com/USUARIO/NOMBRE_DEL_REPOSITORIO.git
cd Proyecto Tercer Parcial

En la terminal
### Instalamos las dependencias
pip install -r requerimientos.txt

### Ejecutamos
python app.py

### Abrimos en navegador
http://127.0.0.1:5000/

