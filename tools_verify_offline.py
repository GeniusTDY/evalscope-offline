import os
import sys
import time
import importlib

WORKSPACE = '/workspace'
CACHE_ROOT = os.path.join(WORKSPACE, 'datasets_cache', 'modelscope')
os.environ['MODELSCOPE_CACHE'] = CACHE_ROOT
os.environ['EVALSCOPE_CACHE'] = os.path.join(WORKSPACE, 'datasets_cache', 'evalscope')
sys.path.insert(0, WORKSPACE)

import evalscope.api.dataset.hub as hub_mod


def _boom(name):
    def _f(*a, **k):
        raise RuntimeError(f'OFFLINE VIOLATION: attempted network fetch via {name}')
    return _f


hub_mod.load_dataset_from_hub = _boom('load_dataset_from_hub')
hub_mod.DatasetHub.load = _boom('DatasetHub.load')
hub_mod.DatasetHub.download_file = _boom('DatasetHub.download_file')
hub_mod.DatasetHub.download_snapshot = _boom('DatasetHub.download_snapshot')
sys.modules['evalscope.api.dataset.hub'] = hub_mod
importlib.import_module('evalscope.api.dataset.loader')

BENCHMARKS = [
    'gsm8k', 'competition_math', 'aime26', 'mmlu_redux', 'arc', 'bbh', 'ceval',
    'cmmlu', 'humaneval', 'mbpp', 'bigcodebench', 'bigcodebench_hard', 'hellaswag',
    'winogrande', 'piqa', 'ifeval', 'commonsense_qa', 'logi_qa', 'halueval',
]

from evalscope.config import TaskConfig
from evalscope.api.registry import get_benchmark

results = []
for name in BENCHMARKS:
    cfg = TaskConfig(model='dummy')
    t0 = time.time()
    try:
        adapter = get_benchmark(name, cfg)
        ds = adapter.load_dataset()
        subs = list(ds.keys())
        total = sum(len(ds[s]) for s in subs)
        results.append((name, 'OK', subs, total, round(time.time() - t0, 2)))
        print(f"[OK] {name}: subsets={subs} rows={total} ({time.time()-t0:.2f}s)", flush=True)
    except Exception as e:
        results.append((name, 'FAIL', str(e), None, round(time.time() - t0, 2)))
        print(f"[FAIL] {name}: {type(e).__name__}: {e}", flush=True)

print('\n=== OFFLINE SUMMARY ===')
ok = 0
for name, status, detail, total, t in results:
    if status == 'OK':
        ok += 1
    print(f"{status:4} {name}: {detail} {(total or '')} {t}s")
print(f'\nPassed {ok}/{len(BENCHMARKS)} fully offline.')
sys.exit(0 if ok == len(BENCHMARKS) else 1)