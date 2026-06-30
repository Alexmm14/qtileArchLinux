import os
import subprocess
import asyncio
from datetime import datetime
import re
from libqtile.log_utils import logger
from libqtile.config import Key
from libqtile.lazy import lazy

class BarRotator:
    def __init__(self):
        # Mantenemos el estado de la rotación por pantalla
        self.screen_states = {}

    def get_display_text(self, qtile_widget):
        if not qtile_widget or not hasattr(qtile_widget, 'bar'):
            return "Cargando..."
            
        screen_idx = qtile_widget.bar.screen.index
        if screen_idx not in self.screen_states:
            self.screen_states[screen_idx] = 0
        
        current_shift = self.screen_states[screen_idx]
        
        # 1. Obtenemos los valores actuales de cada métrica (con sus colores usando formato Pango)
        # Usamos <span foreground='...'> para mantener tus colores originales en un solo string
        metrics = [
            f"<span foreground='#ffcc00'>{self.get_brightness()}</span>",  # 1
            f"<span foreground='#66ffff'>{self.get_volume()}</span>",      # 2
            f"<span foreground='#ffffff'>{self.get_clock()}</span>",       # 3
            f"<span foreground='#ffffff'>{self.get_battery()}</span>"       # 4
        ]
        
        # 2. Aplicamos la rotación de la lista usando el "shift" actual
        # Si current_shift es 1, moverá el último elemento al principio, etc.
        rotated_metrics = metrics[-current_shift:] + metrics[:-current_shift]
        
        # 3. Unimos los elementos usando tu separador clásico con su color gris (#555555)
        separator = " <span foreground='#555555'>|</span> "
        full_text = separator.join(rotated_metrics)
        
        # 4. Incrementamos el shift para la siguiente vuelta (0 -> 1 -> 2 -> 3 -> 0...)
        self.screen_states[screen_idx] = (current_shift + 1) % len(metrics)
        
        return full_text

    # --- Tus funciones de extracción quedan exactamente igual, solo quitamos los iconos del retorno 
    # --- para manejarlos limpiamente o los dejamos dentro como prefieras:
    def get_brightness(self):
        try:
            actual = int(open("/sys/class/backlight/intel_backlight/brightness").read())
            max_b = int(open("/sys/class/backlight/intel_backlight/max_brightness").read())
            percent = int((actual / max_b) * 100)
            return f"󰃟 {percent}%"
        except:
            return "󰃟 --%"

    def get_volume(self):
        try:
            res = subprocess.check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"]).decode("utf-8")
            mute = subprocess.check_output(["pactl", "get-sink-mute", "@DEFAULT_SINK@"]).decode("utf-8")
            if "yes" in mute:
                return "󰝟 Muted"
            import re
            vol = re.search(r"(\d+)%", res).group(1)
            return f"󰕾 {vol}%"
        except:
            return "󰕾 --%"

    def get_clock(self):
        return datetime.now().strftime("%d-%m-%Y %a %H:%M:%S")

    def get_battery(self):
        try:
            capacity = open("/sys/class/power_supply/BAT0/capacity").read().strip()
            status = open("/sys/class/power_supply/BAT0/status").read().strip()
            
            if status == "Charging":
                char = "⚡" # Cargando
            elif status in ["Not charging", "Unknown"]:
                char = "🔌" # Conectado a la corriente, batería en bypass por TLP
            else:
                char = "🔋" # Usando batería (Discharging)
                
            return f"{char} {capacity}%"
        except:
            return "🔋󰁹 --%"

def init_widgets_list(widget, rotator):
    widgets_list = [
        widget.GroupBox(
            highlight_method="border",         
            borderwidth=2,                     
            this_current_screen_border="#FF5555", 
            this_screen_border="#FF5555",         
            other_current_screen_border="#A3BE8C", 
            other_screen_border="#A3BE8C",
            active="#ffffff",                     
            inactive="#4c566a",                   
        ),
        widget.Prompt(),
        widget.TaskList(
            icon_size=20,
            fmt='[{}]',
            font="sans",
            margin_y=3,
            padding_y=3,
            padding_x=5,
            highlight_method='border',
            border="#FFFFFF",
            borderwidth=0.5,
            rounded=True,
            title_width_method='uniform',
            max_title_width=40,
            parse_text=lambda text: "",
            theme_mode='preferred',
            theme_path='/usr/share/icons/Papirus',
        ),
        widget.Notify(
            foreground="#ffffff",
            background="#00000000",
            font="JetBrainsMono Nerd Font",
            fontsize=12,             
            padding=0,               
            margin_y=0,              
            line_height=1,           
            parse_text=lambda text: text.replace('\n', ' ').replace('\r', ''),
            scroll=True,
            scroll_step=3,
            scroll_interval=0.05,
            scroll_delay=2,
            width=200, 
            fmt='󰂚 {}', 
            action=True,
            default_timeout=5,
            name="notification_widget",
        ),
        widget.TextBox(text=' | ', foreground="#555555"),
        
        # Aquí solucionamos el problema del Lambda interno
        widget.GenPollText(
            func=lambda: "Iniciando...",
            update_interval=6,  
            name="volume_widget", 
            # IMPORTANTE: Activamos el marcado Pango para que respete los colores individuales <span foreground=...>
            markup=True, 
        ),
    ]
    
    # TRUCO: Inyectamos la referencia del widget exacto DESPUÉS de crear la lista
    # El índice [5] corresponde al ThreadPoolText dentro de la lista
    widgets_list[5].func = lambda w=widgets_list[5]: rotator.get_display_text(w)
    
    return widgets_list

def add_new_group_manually(qtile):
    """
    Crea manualmente un nuevo grupo con etiqueta de círculo, hasta un máximo de 9.
    """
    if len(qtile.groups) >= 9:
        logger.warning("Máximo de 9 grupos alcanzado.")
        return

    new_name = str(len(qtile.groups) + 1)
    qtile.add_group(new_name, label="●")
    logger.warning(f"Grupo {new_name} creado.")

def delete_current_group(qtile):
    """
    Elimina el grupo actual, reordena los grupos restantes numéricamente
    y protege el grupo '1'.
    """
    current_group = qtile.current_group
    if current_group.name == "1":
        logger.warning("No se puede eliminar el grupo principal.")
        return
    if len(qtile.groups) <= 1:
        logger.warning("No se puede eliminar el último grupo.")
        return
    
    # 1. Cambiar al grupo '1' antes de eliminar el actual
    qtile.groups_map["1"].toscreen()
    
    # 2. Eliminar el grupo
    qtile.delete_group(current_group.name)
    
    # 3. Reordenar los grupos restantes
    # Convertimos a enteros para ordenar correctamente
    groups = sorted([g for g in qtile.groups if g.name.isdigit()], key=lambda g: int(g.name))
    
    new_groups_map = {}
    for i, group in enumerate(groups, start=1):
        new_name = str(i)
        if group.name != new_name:
            # Renombrar grupo
            group.name = new_name
        new_groups_map[new_name] = group
    
    qtile.groups_map = new_groups_map
            
    logger.warning("Grupo eliminado y grupos reordenados.")

def get_available_group(qtile, max_windows=3):
    """
    Busca un grupo con menos de N ventanas. Si todos están llenos, intenta crear uno nuevo hasta el límite de 9.
    """
    for group in qtile.groups:
        if len(group.windows) < max_windows:
            return group.name
    
    # Si todos están llenos, intentar crear uno nuevo si no hemos llegado a 9
    if len(qtile.groups) < 9:
        new_name = str(len(qtile.groups) + 1)
        qtile.add_group(new_name, label="●")
        return new_name
    
    # Si llegamos al límite, devolvemos el último grupo disponible
    return qtile.groups[-1].name