import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[6] / "studies/f3/models"))
import qualify

qualify.OUT = Path("/tmp/sp-sprint2-pipeline/dev")

if __name__ == "__main__":
    qualify.main()
