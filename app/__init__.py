import sys
from pathlib import Path

# Add backend directory to sys.path so backend/app subpackages can be found
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Add backend/app to __path__
backend_app_dir = backend_dir / "app"
__path__.append(str(backend_app_dir))
