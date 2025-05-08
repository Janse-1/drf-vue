# 📚 Sistema de Gestión Académica - IE Indigena N1

Este es un sistema web para la gestión académica de la **Institución Educativa Indígena N1**, que permite la administración de sedes, estudiantes, profesores y notas. Incluye generación de boletines en PDF y carga de calificaciones por parte del docente.

#### Actualmente está en fase inicial
<p>
Solo con django y se irán agregando más cosas conforme el tiempo.
</p>


## 🚀 Tecnologías que se usarán

- **Backend**: Python + Django + Django REST Framework
- **Frontend**: Vue.js + Axios (proximamente)
- **Base de datos**: MySQL 

> Nota: las ultimas versiones de cada una de estas.

## ⚙️ Instalación y configuración

#### 📦 Cómo clonar y ejecutar el proyecto

#### 1. Clonar el repositorio


`git clone https://github.com/Janse-1/drf-vue`

`cd drf-vue`

#### 2. Crear y activar el entorno virtual
    python -m venv venv
	Linux  source venv/bin/activate 
	Windows venv\Scripts\activate

#### 3. Instalar dependencias
`pip install -r requirements.txt`

#### 4. Configurar la base de datos
Edita el archivo `settings.py` con tus credenciales de base de datos:

	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'NAME': 'institucion',
			'USER': 'root',
			'PASSWORD': '',
			'HOST': 'localhost',
			'PORT': '3306',
		}

#### 5. Ejecuta las migraciones
`python manage.py migrate`

#### 6. Levantar el servidor
`python manage.py runserver`


### 🛠 Estado del proyecto
>Proyecto en fase inicial de desarrollo (solo backend).

### ✅ Buenas prácticas

- Commits limpios y con mensajes descriptivos.
- Uso de ramas para desarrollo de nuevas funcionalidades del backend y frontend.
