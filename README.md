# Subida Masiva de VODs de Torneos a YouTube



Script en Python que automatiza la subida masiva de partidas (VODs) de torneos a YouTube utilizando la librería `youtube-bulk-upload`. El programa interpreta el nombre de cada archivo local, traduce la abreviación de la fase del bracket, ordena las partidas cronológicamente y genera automáticamente los títulos y descripciones personalizados.



---



## Características Principales



* **Ordenamiento Cronológico:** Lee el prefijo numérico de cada video (`1 - ...`, `2 - ...`, `10 - ...`) para asegurar que se suban exactamente en el orden en que se jugaron.

* **Formateo Automático de Títulos:** Convierte nombres de archivo como `1 - WF_JugadorA_vs_JugadorB.mp4` en títulos limpios como `Nombre Torneo | Jugadora vs Jugadorb | Winners Finals` (truncando de forma segura a un máximo de 95 caracteres).

* **Plantillas de Descripción Dinámicas:** Reemplaza marcadores clave (`NOMBRE_TORNEO`, `DATE`, `BRACKET`) dentro de un archivo base (`Descripcion.txt`).

* **Modo Simulación (`DRY_RUN`):** Permite previsualizar todos los títulos y validar los archivos antes de gastar cuota de la API de YouTube o subir videos reales.


---



## 📁 Estructura del Proyecto



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

```



---



## Requisitos e Instalación



1. **Clona o descarga este repositorio** y entra en la carpeta del proyecto.

2. **Crea y activa un entorno virtual** (recomendado):

   ```bash

   python -m venv venv

   # En Linux/macOS:

   source venv/bin/activate

   # En Windows:

   venv\Scripts\activate

   ```

3. **Instala la dependencia principal:**

   ```bash

   pip install youtube-bulk-upload

   ```

4. **Configura las credenciales de YouTube:**

   * Ve a [Google Cloud Console](https://console.cloud.google.com/), habilita la **YouTube Data API v3** y crea credenciales de tipo **ID de cliente de OAuth 2.0** (Aplicación de escritorio).

   * Descarga el archivo JSON, renómbralo a `client_secret.json` y colócalo en la raíz del proyecto.

---



## 🛠️ Configuración antes de ejecutar


### 1. Formato obligatorio de los videos (`Source/`)

Todos los videos dentro de la carpeta `Source/` deben seguir estrictamente el patrón:

```text

NUM - FASE_JugadorA_vs_JugadorB.ext

```

* **`NUM`**: Número entero que define el orden de subida (se omite en el título final).

* **`FASE`**: Abreviación de la ronda (sin guiones bajos `_`).

* **`JugadorA` / `JugadorB`**: Nombres o tags de los jugadores separados por `_vs_`.



*Ejemplo válido:* `14 - LSF_Kola_vs_Sparg0.mp4`


### 2. Diccionario de Fases (`Diccionario.json`)

Define cómo se traducirán las abreviaciones al título final. Ejemplo:

```json

{

  "R1": "Pools - Ronda 1",

  "WQ": "Winners Quarters",

  "WSF": "Winners Semifinals",

  "WF": "Winners Finals",

  "LR1": "Losers Round 1",

  "LQ": "Losers Quarters",

  "LSF": "Losers Semifinals",

  "LF": "Losers Finals",

  "GF": "Grand Finals",

  "GFR": "Grand Finals Reset"

}

```

*(Si una abreviación no existe en el JSON, el script mostrará una advertencia y usará la abreviación tal como está escrita).*

### 3. Plantilla de Descripción (`Descripcion.txt`)

Escribe el texto que llevará cada video. El script reemplazará automáticamente las palabras clave `NOMBRE_TORNEO`, `DATE` y `BRACKET`. Ejemplo:

```text

Torneo: NOMBRE_TORNEO

Fecha: DATE

Bracket completo y resultados: BRACKET


¡Sigue nuestras redes para enterarte de los próximos eventos!

```



### 4. Variables del Script (`subir_videos.py`)

Edita el bloque superior del archivo Python antes de cada torneo:

```python

NOMBRE_TORNEO = "U-Smash: Anyone Can Cook!"

DATE = "25 de Julio 2026"

BRACKET_URL = "https://www.start.gg/tournament/u-smash-anyone-can-cook/details"



PRIVACY_STATUS = "private" # Opciones: "private", "unlisted", "public"

DRY_RUN = True             # True = modo prueba (no sube nada) | False = subida real

NONINTERACTIVE = True      # True = sube todo de corrido sin pedir confirmación por video

```



---



##  Uso

1. Coloca los videos renombrados dentro de la carpeta `Source/`.

2. Asegúrate de tener `DRY_RUN = True` en `subir_videos.py` y ejecuta el script para verificar que todos los nombres sean reconocidos:

   ```bash

   python subir_videos.py

   ```

3. Revisa en la consola que los títulos generados sean correctos.

4. Cambia `DRY_RUN = False` en `subir_videos.py` y vuelve a ejecutar el comando:

   ```bash

   python subir_videos.py

   ```

   *(La primera vez que lo ejecutes se abrirá una ventana en tu navegador para iniciar sesión con la cuenta de Google/YouTube donde se subirán los videos).*

---
