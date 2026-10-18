#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Actual CLI rejection controls in private copies; no source archive needed."""
from __future__ import annotations
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types

HERE=Path(__file__).resolve().parent


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def snapshot(root):
    return {str(p.relative_to(root)):(hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_mode&0o777)
            for p in sorted(root.rglob('*')) if p.is_file()}


def execute(folder, *extra):
    return subprocess.run([sys.executable,'-I','-O','-B',str(folder/'verify.py'),*map(str,extra)],
                          cwd=folder, capture_output=True, text=True, timeout=30)


def main():
    names=('verify.py','sheaf.py','GEOMETRY.json.gz','RESULT.json')
    before={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in names}
    result={}
    with tempfile.TemporaryDirectory(prefix='centre-sheaf-controls-') as tmp:
        root=Path(tmp)
        for case in ('valid','geometry_drift','boolean_geometry','duplicate_geometry','boolean_receipt',
                     'missing_source','corrupt_extractor','exclusive_receipt'):
            folder=root/case
            folder.mkdir()
            for name in names:
                shutil.copy2(HERE/name,folder/name)
            geo=folder/'GEOMETRY.json.gz'
            expected=None
            extra=['--geometry',str(geo)]
            if case in ('geometry_drift','boolean_geometry'):
                value=json.loads(gzip.decompress(geo.read_bytes()))
                value['routes'][0][0] = True if case=='boolean_geometry' else value['routes'][0][0]^1
                geo.write_bytes(gzip.compress(json.dumps(value).encode(),mtime=0))
                expected='integer geometry' if case=='boolean_geometry' else 'derived geometry SHA256 mismatch'
            elif case=='duplicate_geometry':
                raw=gzip.decompress(geo.read_bytes()).decode()
                geo.write_bytes(gzip.compress(('{"rows":[], '+raw[1:]).encode(),mtime=0))
                expected='duplicate JSON key: rows'
            elif case=='boolean_receipt':
                p=folder/'RESULT.json'
                value=json.loads(p.read_bytes());value['schema_version']=True
                p.write_text(json.dumps(value))
                expected='receipt type mismatch: receipt.schema_version'
            elif case in ('missing_source','corrupt_extractor'):
                source=root/(case+'-source-root');source.mkdir()
                extra=['--root',str(source)]
                if case=='corrupt_extractor':
                    f=source/'research/centre-block-repair-information/independent.py'
                    f.parent.mkdir(parents=True)
                    f.write_text('# intentionally corrupt disposable source\n')
                    expected='source SHA256 mismatch: research/centre-block-repair-information/independent.py'
                else:
                    expected='missing regular source: research/centre-block-repair-information/independent.py'
            elif case=='exclusive_receipt':
                extra+=['--write-receipt',str(folder/'RESULT.json')]
                expected='File exists'
            frozen=snapshot(folder)
            proc=execute(folder,*extra)
            need(snapshot(folder)==frozen,'CLI mutated protected inputs: '+case)
            if expected is None:
                need(proc.returncode==0 and 'PASS_CENTRE_SHEAF_FIBRE' in proc.stdout,'valid CLI failed')
                result[case]='PASS'
            else:
                need(proc.returncode!=0 and expected in proc.stderr and 'PASS_CENTRE_SHEAF_FIBRE' not in proc.stdout,
                     'wrong rejection: '+case+' '+proc.stderr)
                result[case]=expected
    # Semantic loss of an otherwise independent outgoing class must be caught.
    module=types.ModuleType('disposable_semantic_engine')
    exec(compile((HERE/'sheaf.py').read_bytes(),str(HERE/'sheaf.py'),'exec'),module.__dict__)
    data=json.loads(gzip.decompress((HERE/'GEOMETRY.json.gz').read_bytes()))
    rows=[[module.Q(x) for x in row] for row in data['rows']]
    for row in rows:
        row[1]=module.Q(0)
    try:
        module.analyse(rows,[tuple(r) for r in data['routes']])
    except ValueError as exc:
        need('additional dependent coset classes' in str(exc),'wrong semantic rejection')
        result['erased_independent_column']='REJECT_ADDITIONAL_KERNEL'
    else:
        raise ValueError('erased independent column accepted')
    need(all(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==sha for name,sha in before.items()),
         'original files changed')
    print('PASS_CENTRE_SHEAF_CONTROLS '+json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
