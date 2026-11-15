# Subida Masiva de VODs de Torneos a YouTube

Script en Python que automatiza la subida masiva de partidas (VODs) de torneos a YouTube utilizando la librería `youtube-bulk-upload`. El programa interpreta el nombre de cada archivo local, traduce la abreviación de la fase del bracket, ordena las partidas cronológicamente y genera automáticamente los títulos y descripciones personalizados.

---

## Características Principales
* **Ordenamiento Cronológico:** Lee el prefijo numérico de cada video (`1 - ...`, `2 - ...`, `10 - ...`) para asegurar que se suban exactamente en el orden en que se jugaron.
* **Formateo Automático de Títulos:** Convierte nombres de archivo como `1 - WF_JugadorA_vs_JugadorB.mp4` en títulos limpios como `Nombre Torneo | Jugadora vs Jugadorb | Winners Finals` (truncando de forma segura a un máximo de 95 caracteres).
* **Plantillas de Descripción Dinámicas:** Reemplaza marcadores clave (`NOMBRE_TORNEO`, `DATE`, `BRACKET`) dentro de un archivo base (`Descripcion.txt`).
* **Modo Simulación (`DRY_RUN`):** Permite previsualizar todos los títulos y validar los archivos antes de gastar cuota de la API de YouTube o subir videos reales.
---

## Estructura del Proyecto

Para que el script funcione correctamente, tu carpeta debe tener la siguiente estructura:

```text
├── subir_videos.py       # Script principal de ejecución
├── client_secret.json    # Credenciales OAuth 2.0 de Google Cloud Console
├── Diccionario.json      # Mapeo de abreviaciones de fase a nombres completos
├── Descripcion.txt       # Plantilla de texto para la descripción de los videos
└── Source/               # Carpeta donde debes colocar los archivos de video
    ├── 1 - R1_Player1_vs_Player2.mp4
    ├── 2 - WF_Player3_vs_Player4.mp4
    └── ...
