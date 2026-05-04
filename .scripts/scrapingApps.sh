#!/bin/bash

# Comprobar si se pasó una ruta
if [ -z "$1" ]; then
    echo "Uso: $0 /ruta/a/los/archivos/desktop"
    exit 1
fi

echo "{"

# Buscamos en la ruta proporcionada
find "$1" -name "*.desktop" 2>/dev/null | while read -r file; do
    # Extraemos Name y StartupWMClass
    # Usamos 'head -1' para evitar múltiples traducciones del nombre en el mismo archivo
    name=$(grep "^Name=" "$file" | head -1 | cut -d'=' -f2)
    wm_class=$(grep "^StartupWMClass=" "$file" | head -1 | cut -d'=' -f2)

    if [[ -n "$name" && -n "$wm_class" ]]; then
        # Limpieza: espacios -> guiones bajos, y eliminar caracteres no alfanuméricos
        clean_name=$(echo "$name" | sed 's/ /_/g; s/[^a-zA-Z0-9_]//g')

        printf "    \"%s\": {\"wm_class\": \"%s\", \"group\": \"X\"},\n" "$clean_name" "$wm_class"
    fi
done | sort -u

echo "}"
