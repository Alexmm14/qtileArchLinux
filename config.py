import os
from collections.abc import Callable

import libqtile.resources
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Output, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import asyncio



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
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
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
    Key([mod, "shift"], "Tab", lazy.group.prev_window(), desc="Ventana anterior"),
    #Lanzador
    Key([mod], "space", lazy.spawn("rofi -show drun -theme ~/.config/rofi/launchers/type-4/style-5.rasi"), desc="Move window focus to other window"),

    #Teclas de sonido
    # TECLAS MULTIMEDIA (ASUS TUF F15)
    # Vol++
    Key([], "XF86AudioRaiseVolume", 
    lazy.spawn("bash -c 'pactl set-sink-volume @DEFAULT_SINK@ +5%; VOLUME=$(pactl get-sink-volume @DEFAULT_SINK@ | grep -Po \"[0-9]+(?=%)\" | head -n1); [ $VOLUME -gt 100 ] && pactl set-sink-volume @DEFAULT_SINK@ 100%'")),    # Vol--
    Key([], "XF86AudioLowerVolume", 
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    # Mute
    Key([], "XF86AudioMute", 
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # BRILLO (Iconos de sol en el teclado)
    Key([], "XF86MonBrightnessUp", 
        lazy.spawn("brightnessctl set +3%")),
    Key([], "XF86MonBrightnessDown", 
        lazy.spawn("brightnessctl set 3%-")),
    # Bloquear y Suspender con Alt + L
    Key([mod], "l", lazy.spawn("bash -c '/home/alexmm14/.local/bin/lock-pro && systemctl suspend'"), desc="Suspender"),
    # Captura con formato: screenshot_2026-04-18_16-05.png
    Key([], "Print", lazy.spawn("sh -c 'maim ~/Images/screenshot_$(date +%Y-%m-%d_%H-%M-%S).png'")),
    Key([windows, "shift"], "s", lazy.spawn("sh -c 'maim -s | xclip -selection clipboard -t image/png'")),
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


groups = [Group(i) for i in "12345"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        #Blanco 
        border_focus="#ffffff",        # Color de la ventana activa
        border_normal="#222222",       # Color de ventana inactiva
        border_width=2,                # Grosor del borde
        margin=2,                      # EL ESPACIO DE 1px que querías
        border_focus_stack=["#d75f5f", "#8f3d3d"], 
    ),
    layout.Max(margin=1),              # También le ponemos margen al modo pantalla completa
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

logo = os.path.join(os.path.dirname(libqtile.resources.__file__), "logo.png")
screens = [
    # Monitor Principal (HDMI-1)
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),  # <--- ASEGÚRATE DE QUE ESTA COMA ESTÉ AQUÍ
                widget.TaskList(
                    icon_size=24,                 # Un poco más grande para que se vea mejor
                    font="sans",
                    borderwidth=0,                # Quitamos bordes para un look más limpio
                    margin_y=2,
                    padding_y=2,
                    padding_x=5,
                    highlight_method='block',
                    title_width_method='uniform', # Mantiene el tamaño del botón constante
                    max_title_width=40,           # Limitamos el ancho para que casi no quepa texto
                    # El truco: una función que devuelve un string vacío en lugar del nombre
                    parse_text=lambda text: "",
                    theme_path="/usr/share/icons/Papirus",
                ),
                widget.Systray(),
                # Widget de Brillo
                widget.Backlight(
                    backlight_name='intel_backlight',
                    fmt='󰃟 {}', # Icono de sol/brillo (requiere Nerd Fonts)
                    padding=10,
                    foreground="#ffcc00", # Amarillo brillante
                ),
                
                # Widget de Volumen
                widget.Volume(
                    fmt='󰕾 {}',
                    padding=10,
                    foreground="#66ffff",
                    # Esto obliga al widget a usar 'pactl' para obtener el dato real
                    get_volume_command="pactl get-sink-volume @DEFAULT_SINK@",
                    # Esto le dice cómo verificar si está muteado
                    check_mute_command="pactl get-sink-mute @DEFAULT_SINK@",
                    check_mute_string="Mute: yes",
                    # Muestra esto cuando NO esté muteado (el volumen)
                    update_interval=0.2,
                ),
                widget.Clock(format="%d-%m-%Y %a %I:%M %p"),
            ],
            24,
        ),
    ),
    # Segundo Monitor (Laptop eDP-1)
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.WindowName(), # Aquí podrías usar TaskList también si quieres iconos
                widget.Clock(format="%I:%M %p"),
            ],
            24,
        ),
    ),
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
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
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
def autostart():
    # Esto buscará cuál de tus perfiles (duo o solo) encaja con lo que hay conectado
    os.system("autorandr --change &")
    os.system("feh --bg-fill /home/alexmm14/.secrets/wallpapers/143453-Arch_Linux.jpg")
    os.system("picom &")



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
