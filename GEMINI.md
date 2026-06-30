# Directrices de Desarrollo y Arquitectura - Qtile Arch Linux

Este archivo es la guía de referencia y pauta de desarrollo para la configuración modular de Qtile en Arch Linux. Define la estructura del proyecto, las decisiones de arquitectura, las pautas de estilo y cómo interactuar con los diferentes archivos de configuración.

---

## 📖 Descripción General del Proyecto

Este repositorio contiene una configuración altamente personalizada, modularizada y moderna de **Qtile** sobre **Arch Linux**. Incluye:
- **Barra de estado inteligente e interactiva**: Cuenta con un sistema dinámico rotativo (`BarRotator`) que optimiza el espacio de visualización mostrando información de brillo, volumen, reloj y batería.
- **Asignación automática de escritorios**: Mapeo dinámico de aplicaciones mediante su clase de ventana (`WM_CLASS`).
- **Composición y Estética**: Configuración del compositor Picom con transparencias, bordes redondeados y sombras.
- **Gestos Táctiles**: Integración con `libinput-gestures`.
- **Instalación de paquetes automatizada**: Registro de dependencias oficiales (`pkglist.txt`) y de AUR (`aurlist.txt`).

---

## 📂 Estructura del Proyecto

El código está modularizado para garantizar que `config.py` se mantenga limpio y fácil de mantener:

```
/home/al3xmm14/Documentos/projects/qtileArchLinux/
├── config.py                 # Punto de entrada de Qtile y definición de atajos de teclado
├── modules/
│   ├── __init__.py
│   └── functions.py          # Lógica auxiliar de widgets y la clase BarRotator
├── styles/
│   ├── __init__.py
│   └── barStyle.py           # Estilos de la barra de estado (márgenes, bordes, opacidad, colores)
├── utils/
│   ├── __init__.py
│   └── groups.py             # Definición de escritorios virtuales (grupos) y reglas de apps
├── .scripts/
│   └── scrapingApps.sh       # Script bash para mapear nombres y WM_CLASS de archivos .desktop
├── alacritty/
│   └── alacritty.toml        # Configuración del terminal Alacritty
├── picom/
│   └── picom.conf            # Configuración del compositor Picom
├── gestures/
│   └── libinput-gestures.conf# Configuración de gestos para el touchpad
└── packageInstall/
    ├── pkglist.txt           # Paquetes oficiales para instalar vía pacman
    └── aurlist.txt           # Paquetes de repositorio AUR (yay/paru)
```

---

## 📐 Decisiones de Arquitectura y Extensibilidad

### 1. Control de Atajos de Teclado (`config.py`)
- Se define `mod = "mod1"` (tecla `Alt`) y `windows = "mod4"` (tecla `Super/Windows`).
- Las definiciones de teclas deben estar agrupadas en la lista `keys`.
- Al crear nuevas combinaciones de teclas, siempre se debe añadir el parámetro `desc` con una descripción concisa en español para documentar el comando.

### 2. Rotador Dinámico de Barra (`BarRotator`)
La lógica para optimizar el espacio de la barra está en `modules/functions.py` mediante la clase `BarRotator`.
- Se encarga de mostrar un string enriquecido con formato Pango (`<span foreground='...'>`) que rota cíclicamente entre diferentes métricas del sistema.
- Las métricas soportadas actualmente son: Brillo, Volumen, Reloj y Batería.
- Si se desea extender o modificar las métricas, edita el arreglo `metrics` dentro del método `get_display_text(self, qtile_widget)`.

### 3. Grupos y Mapeo Dinámico (`utils/groups.py`)
El mapeo de aplicaciones a escritorios virtuales se hace mediante la clase `Match` y el diccionario `APPS_CONFIG`:
- Si se requiere que una aplicación siempre se abra en un escritorio específico (ej. grupo "4" para Gemini, grupo "5" para Spotify), añade su clave e identificador en `APPS_CONFIG`.
- **Escanear Aplicaciones Automatizado**: Se proporciona el script `.scripts/scrapingApps.sh` para facilitar este proceso:
  ```bash
  # Ejecución para extraer aplicaciones instaladas localmente
  ./.scripts/scrapingApps.sh /usr/share/applications
  ```

---

## ✍️ Convenciones de Estilo y Código

Para mantener la armonía de la base de código, se definen estrictamente estas dos pautas de idioma:

### 1. Comentarios en Español
Todos los comentarios integrados en los archivos de código fuente, docstrings, explicaciones de funciones y documentación complementaria deben escribirse en **español**.
```python
# SÍ: Explicación clara en español de la función
def init_custom_widgets():
    # Inicializa y devuelve la lista de widgets de la barra
    pass
```

### 2. Código en Inglés
Todos los identificadores de programación, incluyendo nombres de clases, funciones, variables, constantes, parámetros, nombres de archivos de código y ramas deben escribirse en **inglés** de manera limpia e idiomática.
```python
# SÍ: Variables y funciones en inglés
class SystemStatusMonitor:
    def __init__(self):
        self.battery_level = 100
        
    def get_battery_status(self):
        # Retorna el porcentaje actual de la batería
        return self.battery_level
```

*Nota: Nunca mezclar idiomas en los nombres de variables (evitar "spanglish", ej. `lista_de_widgets` o `getBateria`). El estándar debe ser estrictamente código en inglés y comentarios en español.*

---

## 🛠️ Instalación y Mantenimiento del Sistema

### 1. Instalación de Paquetes (Arch Linux)
Si estás configurando este entorno en una máquina nueva, puedes instalar rápidamente las dependencias usando las listas proporcionadas en `packageInstall/`:

```bash
# Instalar paquetes oficiales con pacman
sudo pacman -S --needed - < packageInstall/pkglist.txt

# Instalar paquetes AUR usando yay
yay -S --needed - < packageInstall/aurlist.txt
```

### 2. Configuración de Componentes Auxiliares
- **Gestos de Touchpad**: `libinput-gestures` lee la configuración en `gestures/libinput-gestures.conf`. Asegúrate de copiarlo o enlazarlo simbólicamente a `~/.config/libinput-gestures.conf`.
- **Picom**: Enlazado simbólico de `picom/picom.conf` a `~/.config/picom/picom.conf` para aplicar transparencias y sombras en las ventanas de Qtile.
- **Alacritty**: Enlazado simbólico de `alacritty/alacritty.toml` a `~/.config/alacritty/alacritty.toml`.

---

## 🧪 Pruebas, Validación y Depuración

### Cómo verificar cambios antes de aplicar o reiniciar Qtile:

1. **Prueba de Sintaxis (Compilación)**:
   Siempre valida que tu configuración no tenga errores de sintaxis en Python ejecutando:
   ```bash
   python3 -m py_compile config.py
   ```

2. **Uso del Registrador de Qtile (Logging)**:
   No uses `print()` para depurar, en su lugar usa el logger oficial de Qtile para capturar salidas en `~/.local/share/qtile/qtile.log`:
   ```python
   from libqtile.log_utils import logger

   # Registro de advertencias útiles para depuración
   logger.warning("Este es un mensaje de depuración en español")
   ```

3. **Recarga Segura**:
   Una vez que compiles el archivo sin errores, recarga Qtile usando el atajo `Alt + Ctrl + R` (que ejecuta internamente `lazy.reload_config()`) para ver tus cambios de manera instantánea y segura.
