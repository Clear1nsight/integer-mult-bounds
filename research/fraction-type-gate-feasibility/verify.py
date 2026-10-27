"""Fresh finite feasibility only, not complete qualification or performance."""
import json
from pathlib import Path
from frozen import require
from finite import main

if __name__=='__main__':
    actual=main()
    expected=json.loads((Path(__file__).resolve().parent/'RESULT.json').read_text())
    require(actual==expected,'complete finite and all54 controls match')
    print('PASS_FRACTION_ENTRY_GATE_FINITE_ONLY')
