import base64
from pathlib import Path
from core.config import settings

def load_image_base64(name: str) -> str:
    """
    name: "0"~"9" or "EMPTY"
    returns: data:image/png;base64,...
    """
    assets_dir = Path(settings.ASSETS_DIR)
    file_path = assets_dir / f"{name}.png"

    if not file_path.exists():
        raise FileNotFoundError(f"Missing asset file: {file_path.as_posix()}")

    raw = file_path.read_bytes()
    encoded = base64.b64encode(raw).decode("ascii")
    return f"data:image/png;base64,{encoded}"
