from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # Solution/
PIPELINE = ROOT / "pipeline"
FEATURES = ROOT / "features"
BUILD = ROOT / "build"
LOG_DIR = BUILD / "logs"
REQUIREMENTS = ROOT / "requirements"
