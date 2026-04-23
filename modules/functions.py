import asyncio
from libqtile import qtile
from libqtile.log_utils import logger

volume_timer = None

def show_volume(qtile):
    logger.info("Cambiando color de volumen a visible")
    global volume_timer
    
    visible_color = "#66ffff"
    hidden_color = "#00000000"

    vol_widget = qtile.widgets_map.get('volume_widget')
    
    if vol_widget:
        try:
            # 1. Cambiamos el color a visible
            vol_widget.foreground = visible_color
            logger.info("Cambiando color de volumen a visible")

            
            # 2. En lugar de .update(), usamos .tick() o simplemente .draw()
            # .draw() es suficiente para mostrar el cambio de color inmediato.
            vol_widget.draw()

            # 3. Manejo del timer para ocultar
            if volume_timer:
                volume_timer.cancel()

            def hide():
                try:
                    vol_widget.foreground = hidden_color
                    vol_widget.draw()
                except Exception:
                    pass

            loop = asyncio.get_running_loop()
            volume_timer = loop.call_later(3, hide)
            
        except Exception as e:
            logger.error(f"Error en show_volume: {e}")
    else:
        logger.error("No se encontró 'volume_widget'. Revisa el name en config.py")


def init_widgets_list(widget):
    widgets_list = [
        #widget.CurrentLayout(),
        widget.GroupBox(
            disable_drag=True,
        ),
        widget.Prompt(),
        widget.TaskList(
            icon_size=20,
            fmt='[{}]',
            font="sans",
            borderwidth=0,
            margin_y=3,
            padding_y=3,
            padding_x=5,
            highlight_method='block',
            title_width_method='uniform',
            max_title_width=40,
            parse_text=lambda text: "",
            theme_mode='preferred',
            theme_path='/usr/share/icons/Papirus',
        ),
        widget.Backlight(
            backlight_name='intel_backlight',
            fmt='󰃟 {}',
            foreground="#ffcc00",
        ),
        widget.TextBox(text=' | ', foreground="#555555"),
        widget.Volume(
            fmt='󰕾 {}',
            foreground="#66ffff",
            get_volume_command="pactl get-sink-volume @DEFAULT_SINK@",
            check_mute_command="pactl get-sink-mute @DEFAULT_SINK@",
            check_mute_string="Mute: yes",
        ),
        widget.TextBox(text=' | ', foreground="#555555"),
        widget.Clock(format="%d-%m-%Y %a %H:%M:%S"),
        widget.TextBox(text=' | ', foreground="#555555"),
        widget.Battery(
            format='{char} {percent:2.0%}',
            charge_char='󰂄',
            discharge_char='󰁹',
            padding=10,
        ),
    ]
    return widgets_list