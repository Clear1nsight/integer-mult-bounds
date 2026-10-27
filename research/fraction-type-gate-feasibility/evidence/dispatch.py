from pathlib import Path
import sys
import guard

guard.SOURCE=guard.HERE.parent/'feasibility'
guard.CLOSURE=('fraction_table.py','table_parent.py','parent_finite.py','finite.py','frozen.py','actual_audit.py','inputs/PR5848.tar','/usr/lib/python3.12/fractions.py')
guard.AGGREGATE=600
label=sys.argv[1]
script='actual_audit.py' if label=='actual-type-gate' else 'finite.py'
with (guard.HERE/'execution.lock').open('a') as lock:
    guard.fcntl.flock(lock,guard.fcntl.LOCK_EX|guard.fcntl.LOCK_NB)
    guard.run(label,script,optimized=label.endswith('-O'))
