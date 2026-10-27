"""One fresh full actual original/derived trace comparison; not a speed benchmark."""
from copy import deepcopy
import gzip
import importlib.util
import json
from pathlib import Path
import sys
import time
from frozen import baseline,require
from fraction_table import derive,certified_domain
from finite import types_of

with baseline() as package:
    sys.path.insert(0,str(package))
    import source
    with source.baseline() as p:
        spec=importlib.util.spec_from_file_location('actual_audit_source',p/'verify.py')
        v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
        with v.source() as (original_path,original,reference):
            word=json.loads(gzip.decompress((original_path/'inputs/WORD.json.gz').read_bytes()))
            ideal,weights=reference.ideal(word);rounded=set(ideal['counts'])
            fingerprint=reference.digest((word,weights,sorted(rounded)))
            require(certified_domain(word,weights,rounded),'actual source is in proven entry domain')
            cpu=time.process_time();started=time.perf_counter();a=reference.error_trace(word,weights,rounded);baseline_seconds=time.perf_counter()-started;baseline_cpu=time.process_time()-cpu
            fast=derive(reference)
            cpu=time.process_time();started=time.perf_counter();b=fast(word,weights,rounded);candidate_seconds=time.perf_counter()-started;candidate_cpu=time.process_time()-cpu
            require(a==b and types_of(a)==types_of(b),'all actual trace/witness values and types')
            require(reference.digest((word,weights,sorted(rounded)))==fingerprint,'all actual inputs unchanged')
            result=dict(baseline_trace_cpu_seconds=baseline_cpu,derived_trace_cpu_seconds=candidate_cpu,certified_domain=True,status='PASS_FULL_ACTUAL_FRACTION_TRACE_EQUIVALENCE',events=len(word['program']),coordinates=ideal['n'],full_output_sha256=reference.digest(a),weights_sha256=reference.digest(weights),baseline_trace_seconds=baseline_seconds,derived_trace_seconds=candidate_seconds,observed_seconds_removed=baseline_seconds-candidate_seconds,profile_whole_qualifier_seconds=38.31372155799181,all_values_types_and_inputs_preserved=True,table_statistics=fast.statistics())
            print(json.dumps(result,sort_keys=True))
