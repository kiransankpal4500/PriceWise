import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Import the actual FastAPI app from backend/app/main.py
import importlib.util

backend_main_path = backend_dir / "app" / "main.py"
spec = importlib.util.spec_from_file_location("backend_app_main", str(backend_main_path))
backend_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend_main)

app = backend_main.app
