import os, subprocess

class autostart:
    def __init__(self):
        pass     
    def startAppps():
        home = os.path.expanduser('~')

        # =========================================================================
        # 1. ORQUESTACIÓN DE ENTORNO (DBus y Gnome Keyring)
        # =========================================================================

        # Actualiza el entorno de DBus
        try:
            subprocess.Popen("dbus-update-activation-environment --all", shell=True)
        except Exception:
            pass

        # Inicia el llavero y captura sus variables de entorno
        try:
            # Usamos check_output para esperar a que nos devuelva las variables impresas
            output = subprocess.check_output(
                "gnome-keyring-daemon --start --components=secrets,pkcs11,ssh", 
                shell=True, 
                text=True
            )
            # Parseamos las líneas tipo VARIABLE=VALOR y las metemos al entorno de Python
            for line in output.splitlines():
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        except Exception:
            pass

        # =========================================================================
        # 2. COMANDOS NORMALES Y CONFIGURACIÓN DEL SISTEMA
        # =========================================================================
        apps = [
            ["libinput-gestures-setup", "start"],
            ["autorandr", "--change"],
            ['xss-lock', '--', 'transfer-sleep-lock', '--', 'i3lock', '-c', '000000'],
            ['pkill', '-f', 'wallpaper.sh'],
        ]

        for app in apps:
            try:
                subprocess.Popen(app)
            except Exception:
                pass

        # =========================================================================
        # 3. INTERFAZ VISUAL (X11 / COMPOSITOR / WALLPAPER)
        # =========================================================================

        # Picom
        try:
            subprocess.Popen(f"picom --config {home}/.config/picom/picom.conf", shell=True)
        except Exception:
            pass

        # Tu script de wallpaper
        try:
            subprocess.Popen(f"bash {home}/.secrets/scripts/wallpaper.sh", shell=True)
        except Exception:
            pass

        try:
            subprocess.Popen("brightnessctl set 15%", shell=True)
        except Exception:
            pass
