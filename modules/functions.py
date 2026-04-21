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