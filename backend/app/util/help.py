import os
import uuid
from app.config import OUT_DIR

def out_name(full_path: str) -> str:
    """Extracts just the filename from a full path."""
    return os.path.basename(full_path)

def out_path(input_path: str, ext: str) -> str:
    """Generates a unique full path for the output file in the 'out' directory."""
    # Create a unique ID so files don't overwrite each other
    uid = uuid.uuid4().hex[:8]
    # Get the original filename without extension
    base = os.path.splitext(os.path.basename(input_path))[0]
    # Combine everything into the output directory
    return os.path.join(OUT_DIR, f"{base}_{uid}{ext}")