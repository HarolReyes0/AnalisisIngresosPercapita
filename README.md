# Proyecto: Sistema de Modelado y Visualización de Datos de Salud

Este proyecto tiene como objetivo procesar, modelar y visualizar datos de afiliación y dispersión de cápitas    
en el sector salud dominicano, utilizando Dash, Pandas y Plotly.

---

## Estructura del Proyecto
```
project/
│
├── data/
│   ├── processed/       # Datos ya modelados por institución
│   └── raw/             # Datos crudos originales (ONE, CNSS)
│
├── documents/           # Manuales y archivos de documentación y analisis (PDF, DOCX)
├── notebooks/           # Espacio para análisis exploratorio (Jupyter)
│
├── src/                 # Código fuente principal
│   ├── dashboard/       # Código de la app Dash y layout
│   │   ├── layout.py
│   │   └── charts.py
│   ├── modeling/        # Procesamiento de datos
│   │   └── data_cleaning.py
│   └── main.py          # Punto de entrada del proyecto
│
├── README.md            # Documentación general del proyecto
├── requirements.txt     # Dependencias de Python
└── .gitignore           # Archivos ignorados por Git
```

---

## 🚀 ¿Cómo ejecutar el proyecto?

### 1. Clona el repositorio:
```bash
git clone https://github.com/tu_usuario/proyecto-modelado-salud.git
cd proyecto-modelado-salud
```

### 2. Crea un entorno virtual y activa:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

### 4. Ejecuta la aplicación:
```bash
python src/main.py
```

Esto abrirá el dashboard interactivo en tu navegador en el puerto `8071`.

---

## 🧠 Funcionalidades Clave
- Modelado automático de datos de instituciones como ONE y CNSS.
- Limpieza de archivos Excel y CSV con transformaciones automáticas.
- Visualización interactiva con filtros por año y régimen.
- Uso de Dash + Plotly + Bootstrap Templates para una interfaz moderna.

---

## 📊 Visualizaciones Incluidas
- Cantidad de afiliados por tipo de régimen.
- Número de cápitas pagadas por año.
- Monto dispersado por género.
- Porcentaje de dinero dispersado por tipo de cliente.

---
## Fuente de Datos
[Protección Social y Seguridad Social - ONE](https://www.one.gob.do/datos-y-estadisticas/temas/estadisticas-sociales/proteccion-social-seguridad-social/)   
[Portal de Datos - CNSS](https://cnss.gob.do/transparencia/estadisticas-institucionales/historico-indice-del-uso-tic-itcge)   
[Plataforma Integral de Población - ONE](https://pip.one.gob.do/)