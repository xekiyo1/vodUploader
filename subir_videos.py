import json
import re
from pathlib import Path
from youtube_bulk_upload.bulk_upload import YouTubeBulkUpload

# ============ EDITA ESTOS VALORES ============
CLIENT_SECRETS_FILE = "client_secret.json"
SOURCE_DIRECTORY = "Source"
DICCIONARIO_PATH = "Diccionario.json"
DESCRIPCION_TEMPLATE_PATH = "Descripcion.txt"

NOMBRE_TORNEO = "U-Smash: Anyone Can Cook!"
DATE = "25 de Julio 2026"
BRACKET_URL = "https://www.start.gg/tournament/u-smash-anyone-can-cook/details"

# Estado de privacidad: todos los videos se subirán en privado
PRIVACY_STATUS = "private"

DRY_RUN = True           # Cambia a True si solo quieres probar sin subir nada
NONINTERACTIVE = True     # True = no pedir confirmación manual por cada video
# ================================================


FILENAME_PATTERN = re.compile(
    r"^\s*\d+\s*-\s*"        # número inicial + guion (se ignora para el título)
    r"(?P<phase>[^_]+)_"    # abreviación de fase
    r"(?P<player_a>.+?)"    # jugador A
    r"_vs_"                 # separador
    r"(?P<player_b>.+)$",   # jugador B
    re.IGNORECASE,
)


def parse_filename(video_file: str) -> tuple[str, str, str]:
    """Extrae (fase_abreviada, jugador_a, jugador_b) desde el nombre del archivo."""
    stem = Path(video_file).stem
    match = FILENAME_PATTERN.match(stem)
    if not match:
        raise ValueError(
            f"No se pudo interpretar el nombre de archivo: '{stem}'. "
            f"Se esperaba el formato 'NUM - FASE_jugadorA_vs_jugadorB'."
        )
    return (
        match.group("phase").strip(),
        match.group("player_a").strip(),
        match.group("player_b").strip(),
    )


class TorneoUploader(YouTubeBulkUpload):
    """Extiende YouTubeBulkUpload con metadatos personalizados para torneos."""

    def __init__(self, *args, phase_dictionary: dict, nombre_torneo: str, date: str, 
                 bracket_url: str, description_template: str, **kwargs):
        
        self.phase_dictionary = phase_dictionary
        self.nombre_torneo = nombre_torneo
        self.date = date
        self.bracket_url = bracket_url
        self.description_template = description_template
        
        super().__init__(*args, **kwargs)

    def get_video_files(self) -> list[Path]:
        """Obtiene la lista de videos y los ORDENA por el número inicial (1, 2, 3...)."""
        files = super().get_video_files()

        def extract_number(file_path: Path) -> int:
            match = re.match(r"^\s*(\d+)", file_path.name)
            return int(match.group(1)) if match else 999999

        return sorted(files, key=extract_number)

    def resolve_phase(self, phase_abbr: str) -> str:
        if phase_abbr not in self.phase_dictionary:
            self.logger.warning(
                f"Fase '{phase_abbr}' no está en el diccionario, se usará tal cual."
            )
        return self.phase_dictionary.get(phase_abbr, phase_abbr)

    def determine_youtube_title(self, video_file: str) -> str:
        phase_abbr, player_a, player_b = parse_filename(video_file)
        phase_full = self.resolve_phase(phase_abbr)
        title = f"{self.nombre_torneo} | {player_a.capitalize()} vs {player_b.capitalize()} | {phase_full}"
        return self.truncate_to_nearest_word(title, 95)

    def determine_youtube_description(self, video_file: str, youtube_title: str) -> str:
        description = self.description_template
        description = description.replace("NOMBRE_TORNEO", self.nombre_torneo)
        description = description.replace("DATE", self.date)
        description = description.replace("BRACKET", self.bracket_url)
        return description

    def determine_made_for_kids(self, video_file: str) -> bool:
        """Declara explícitamente que NO es contenido para niños (Ley COPPA)."""
        return False
    
    def check_for_duplicate_on_youtube(self, video_file: str, youtube_title: str) -> bool:
        """
        SOBRESCRIBE la detección de duplicados.
        Siempre retorna False para permitir subir todos los videos sin verificar duplicados.
        """
        self.logger.info(f"Verificación de duplicados DESACTIVADA para: {youtube_title}")
        return False


def main():
    # Validar que todos los archivos requeridos existan
    for label, path in [
        ("client_secret.json", CLIENT_SECRETS_FILE),
        ("carpeta de videos", SOURCE_DIRECTORY),
        ("Diccionario.json", DICCIONARIO_PATH),
        ("Descripcion.txt", DESCRIPCION_TEMPLATE_PATH),
    ]:
        if not Path(path).exists():
            raise SystemExit(f"ERROR: No se encontró {label} en la ruta: {path}")

    with open(DICCIONARIO_PATH, "r", encoding="utf-8") as f:
        phase_dictionary = json.load(f)

    with open(DESCRIPCION_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        description_template = f.read()

    uploader = TorneoUploader(
        youtube_client_secrets_file=CLIENT_SECRETS_FILE,
        source_directory=SOURCE_DIRECTORY,
        phase_dictionary=phase_dictionary,
        nombre_torneo=NOMBRE_TORNEO,
        date=DATE,
        bracket_url=BRACKET_URL,
        description_template=description_template,
        dry_run=DRY_RUN,
        interactive_prompt=not NONINTERACTIVE,
        privacy_status=PRIVACY_STATUS,
        check_for_duplicate_titles=False,  # ESTA ES LA CLAVE: desactiva la verificación de duplicados
    )

    print("🚀 Iniciando proceso de subida masiva...")
    uploaded_videos = uploader.process()

    print(f"\n✅ Procesados exitosamente: {len(uploaded_videos)} videos")
    for video in uploaded_videos:
        input_file = video.get('input_filename', 'Video')
        yt_title = video.get('youtube_title', 'Título')
        print(f" 🎬 {input_file} -> {yt_title}")


if __name__ == "__main__":
    main()