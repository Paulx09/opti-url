# 🔗 OptiURL - Cortador de Enlaces

Aplicación web desarrollada con Flask y MySQL para acortar URLs de manera sencilla y eficiente.

## 🚀 Características

- ✅ Acorta URLs largas en enlaces cortos y únicos
- ✅ Interfaz moderna con Bootstrap 5
- ✅ Base de datos MySQL para almacenamiento persistente
- ✅ Redireccionamiento automático
- ✅ Diseño responsive
- ✅ Detección de URLs duplicadas

## 📁 Estructura del Proyecto

```
opti-url/
├── src/
│   ├── static/
│   │   └── img/
│   │       ├── banner.png
│   │       ├── python.svg
│   │       └── ads.png
│   ├── templates/
│   │   ├── layout.html
│   │   ├── index.html
│   │   ├── ads.html
│   │   └── 404.html
│   └── app.py
├── requirements.txt
├── Procfile
├── database.sql
└── README.md
```

## 🛠 Tecnologías Utilizadas

- **Backend:** Flask (Python)
- **Base de datos:** MySQL
- **Frontend:** HTML5, Bootstrap 5, JavaScript
- **Deployment:** Railway
- **Generación de IDs:** shortuuid

## 🚀 Deployment en Railway

### Prerrequisitos
- Cuenta en [Railway](https://railway.app)
- Node.js instalado (para Railway CLI)

### Pasos para el deployment

1. **Instalar Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Hacer login en Railway**
   ```bash
   railway login
   ```

3. **Inicializar proyecto**
   ```bash
   railway init
   ```

4. **Agregar base de datos MySQL**
   ```bash
   railway add --database mysql
   ```

5. **Configurar variables de entorno**
   ```bash
   railway variables set SECRET_KEY="tu_clave_secreta_muy_segura_aqui"
   railway variables set DEBUG="False"
   ```

6. **Deployar la aplicación**
   ```bash
   railway up
   ```

7. **Configurar la base de datos**
   - Ve al dashboard de Railway
   - Abre la consola de MySQL
   - Ejecuta las consultas del archivo `database.sql`

### Variables de Entorno

Railway configurará automáticamente estas variables:
- `MYSQL_HOST` - Host de la base de datos
- `MYSQL_USER` - Usuario de MySQL
- `MYSQL_PASSWORD` - Contraseña de MySQL
- `MYSQL_DATABASE` - Nombre de la base de datos
- `PORT` - Puerto de la aplicación

Variables que debes configurar manualmente:
- `SECRET_KEY` - Clave secreta para Flask
- `DEBUG` - Modo debug (False para producción)

## 💻 Desarrollo Local

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Paulx09/opti-url.git
   cd opti-url
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv env
   source env/bin/activate  # Linux/Mac
   # o
   env\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos local**
   - Instalar MySQL
   - Crear base de datos `db_opti_url`
   - Ejecutar script `database.sql`

5. **Ejecutar la aplicación**
   ```bash
   python src/app.py
   ```

## 📊 Base de Datos

### Tabla LINKS
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INT | ID único (clave primaria) |
| URL | TEXT | URL original |
| SHORT_LINK | VARCHAR(10) | Código único del enlace corto |
| created_at | TIMESTAMP | Fecha de creación |

## 🎯 Uso

1. **Acortar URL:**
   - Ingresa la URL completa en el formulario
   - Haz clic en "Cortar URL"
   - Copia el enlace corto generado

2. **Usar enlace corto:**
   - Visita `tu-dominio.com/código`
   - Serás redirigido automáticamente a la URL original

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autor

**Paulo** - [Paulx09](https://github.com/Paulx09)

---

⭐ ¡No olvides dar una estrella al proyecto si te fue útil!
