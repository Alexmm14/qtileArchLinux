import os
from collections.abc import Callable
import libqtile.resources
from libqtile.log_utils import logger
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Output, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import asyncio
from modules.functions import init_widgets_list, BarRotator, get_available_group, add_new_group_manually, delete_current_group
from modules.autoStart import autostart
from styles.barStyle import get_bar_style
from utils.groups import groupTemplate
import subprocess

#from libqtile.log_utils import logger # <--- Importante para debug



# Instanciamos el rotador global

mod = "mod1"
windows = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    #Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    #Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    #Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    #Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    #Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),    
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.function(add_new_group_manually), desc="Create new group"),
    Key([mod, "shift"], "n", lazy.function(delete_current_group), desc="Delete current group"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.next_layout(), desc="Alternar entre modo Max y Columns"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Captura de pantalla con Ctrl + Shift + P
    Key(["control", "shift"], "p", lazy.spawn("flameshot gui")),
    # Alt + Tab: Pasar a la siguiente ventana
    Key([mod], "Tab", lazy.group.next_window(), desc="Siguiente ventana"),

    # Alt + Shift + Tab: Pasar a la ventana anterior
    # Añade estas dos líneas a tu lista keys = [...]
    Key([windows, mod], "Right", lazy.screen.next_group(), desc="Siguiente escritorio"),
    Key([windows, mod], "Left", lazy.screen.prev_group(), desc="Escritorio anterior"),

    #Lanzador
    Key([mod], "space", lazy.spawn("rofi -show drun -theme ~/.config/rofi/launchers/type-4/style-5.rasi"), desc="Move window focus to other window"),

    #Teclas de sonido
    # TECLAS MULTIMEDIA (ASUS TUF F15)
    # Vol++
    Key([], "XF86AudioRaiseVolume", 
    lazy.spawn("bash -c 'pactl set-sink-volume @DEFAULT_SINK@ +5%; VOLUME=$(pactl get-sink-volume @DEFAULT_SINK@ | grep -Po \"[0-9]+(?=%)\" | head -n1); [ $VOLUME -gt 100 ] && pactl set-sink-volume @DEFAULT_SINK@ 100%'")),    
    # Vol--
    Key([], "XF86AudioLowerVolume", 
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    # Mute
    Key([], "XF86AudioMute", 
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # BRILLO (Iconos de sol en el teclado)
    Key([], "XF86MonBrightnessUp", 
        lazy.spawn("brightnessctl set +1%")),
    Key([], "XF86MonBrightnessDown", 
        lazy.spawn("brightnessctl set 1%-")),
    # Bloquear y Suspender con Alt + L
    Key([windows], "l", lazy.spawn("bash -c 'i3lock -c 000000'"), desc="Suspender"),
    # Captura con formato: screenshot_2026-04-18_16-05.png
    Key([], "Print", lazy.spawn("sh -c 'maim ~/Images/screenshot_$(date +%Y-%m-%d_%H-%M-%S).png'")),
    Key([windows, "shift"], "s", lazy.spawn("sh -c 'maim -s | tee ~/Images/screenshotArea_$(date +%Y-%m-%d_%H-%M-%S).png | xclip -selection clipboard -t image/png'")),
    # Minimizar / Esconder la ventana actual felcha abajo
    Key([windows], "Down", lazy.window.toggle_minimize(), desc="Toggle minimize"),
    Key([windows], "space", lazy.hide_show_bar())
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

def go_to_group(qtile, name):
    """
    Cambia al grupo si existe.
    """
    if name in qtile.groups_map:
        qtile.groups_map[name].toscreen()
    else:
        logger.error(f"Grupo {name} no encontrado")

def move_window_to_group(qtile, name):
    """
    Mueve la ventana al grupo si existe.
    """
    if name in qtile.groups_map:
        qtile.current_window.togroup(name, switch_group=True)
    else:
        logger.error(f"Grupo {name} no encontrado")

# Atajos para grupos (del 1 al 9)
for i in range(1, 10):
    name = str(i)
    keys.extend([
        Key(
            [mod],
            name,
            lazy.function(go_to_group, name),
            desc=f"Switch to group {name}",
        ),
        Key(
            [mod, "shift"],
            name,
            lazy.function(move_window_to_group, name),
            desc=f"Switch to & move focused window to group {name}",
        ),
    ])

layouts = [
    layout.Columns(
        #Blanco 
        border_focus="#ffffff",        # Color de la ventana activa
        border_normal="#222222",       # Color de ventana inactiva
        border_width=2,                # Grosor del borde
        margin=[10, 7, 10, 7],                      # EL ESPACIO DE 1px que querías
        border_focus_stack=["#d75f5f", "#8f3d3d"], 
    ),
    layout.Max(margin=[10, 7, 10, 7]),              # También le ponemos margen al modo pantalla completa
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font, Symbols Nerd Font",
    #font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

logo = os.path.join(os.path.dirname(libqtile.resources.__file__), "logo.png")
rotator = BarRotator()


screens = [
    # Monitor Laptop 
    Screen(top=bar.Bar(init_widgets_list(widget, rotator), 28, **get_bar_style())),
    # Monitor Principal (HDMI-1)
    Screen(top=bar.Bar(init_widgets_list(widget, rotator), 28, **get_bar_style())),
    
]

# Instead of screens, you can define a function here to specify which Screen
# should correspond to which Output.
fake_screens: list[Screen] | None = None

# Instead of screens or fake screens, you can define a function here that
# returns a list of Screen objects based on the list of Outputs; that way you
# can decide based on e.g. the number of screens, or which ports are plugged
# in exactly what do render in each bar for each screen.
generate_screens: Callable[[list[Output]], list[Screen]] | None = None

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Drag([mod], "Button3", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
focus_task = None
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

idle_timers = []  # type: list
idle_inhibitors = []  # type: list

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"



@hook.subscribe.startup_once
#Quiero cargar mi funcion de autostart
def start():
    autostart.startAppps()


#Delay mouse/window
@hook.subscribe.client_mouse_enter
async def delayed_focus(client):
    global focus_task
    # Si ya hay un intento de enfoque en curso, lo cancelamos
    if focus_task:
        focus_task.cancel()

    # Creamos una tarea que espera 1.5 segundos antes de enfocar
    try:
        focus_task = asyncio.create_task(asyncio.sleep(1))
        await focus_task
        client.focus()
    except asyncio.CancelledError:
        pass

@hook.subscribe.client_new
def follow_window(client):
    async def move_with_delay(c):
        await asyncio.sleep(0.4)
        wm_classes = c.get_wm_class()
        
        if not wm_classes:
            return

        target_group = None

        # 1. Verificar reglas de APPS_CONFIG
        for app_name, config in APPS_CONFIG.items():
            target_class = config["wm_class"]
            
            if any(target_class.lower() in cls.lower() for cls in wm_classes):
                candidate_group = config["group"]
                
                # Check limit
                if len(qtile.groups_map[candidate_group].windows) < 3:
                    target_group = candidate_group
                else:
                    # Regla dicta grupo lleno, buscar otro
                    target_group = get_available_group(qtile)
                
                break
        
        # 2. Si no hay regla, usar el grupo actual o uno disponible
        if not target_group:
            current_group = c.group.name
            if len(qtile.groups_map[current_group].windows) > 3:
                 target_group = get_available_group(qtile)
        
        if target_group:
            c.togroup(target_group)
            qtile.groups_map[target_group].toscreen() 
            c.focus()

    asyncio.create_task(move_with_delay(client))
