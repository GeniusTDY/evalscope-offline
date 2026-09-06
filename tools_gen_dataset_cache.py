#!/usr/bin/env python
"""Generate the offline dataset cache for the 19 bundled benchmarks.

Sets MODELSCOPE_CACHE to <workspace>/datasets_cache/modelscope so the on-disk
save_to_disk cache (read by RemoteDataLoader.load_from_disk on offline machines)
lands under the exact path layout the runtime expects.

Usage:  MODELSCOPE_CACHE=... python tools_gen_dataset_cache.py
"""
import json
import os
import sys
import time

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
CACHE_ROOT = os.path.join(WORKSPACE, 'datasets_cache', 'modelscope')
os.environ.setdefault('MODELSCOPE_CACHE', CACHE_ROOT)
# make sure evalscope uses this repo as source when loaded below
os.environ['MODELSCOPE_CACHE'] = CACHE_ROOT

# name -> adapter import module (module that @register_benchmark the name)
ADAPTER_MODULE = {
    'gsm8k': 'evalscope.benchmarks.gsm8k.gsm8k_adapter',
    'competition_math': 'evalscope.benchmarks.competition_math.competition_math_adapter',
    'aime26': 'evalscope.benchmarks.aime.aime_adapter',
    'mmlu_redux': 'evalscope.benchmarks.mmlu_redux.mmlu_redux_adapter',
    'arc': 'evalscope.benchmarks.arc.arc_adapter',
    'bbh': 'evalscope.benchmarks.bbh.bbh_adapter',
    'ceval': 'evalscope.benchmarks.ceval.ceval_adapter',
    'cmmlu': 'evalscope.benchmarks.cmmlu.cmmlu_adapter',
    'humaneval': 'evalscope.benchmarks.humaneval.humaneval_adapter',
    'mbpp': 'evalscope.benchmarks.mbpp.mbpp_adapter',
    'bigcodebench': 'evalscope.benchmarks.bigcodebench.bigcodebench_adapter',
    'bigcodebench_hard': 'evalscope.benchmarks.bigcodebench.bigcodebench_adapter',
    'hellaswag': 'evalscope.benchmarks.hellaswag.hellaswag_adapter',
    'winogrande': 'evalscope.benchmarks.winogrande.winogrande_adapter',
    'piqa': 'evalscope.benchmarks.piqa.piqa_adapter',
    'ifeval': 'evalscope.benchmarks.ifeval.ifeval_adapter',
    'commonsense_qa': 'evalscope.benchmarks.commonsense_qa.commonsense_qa_adapter',
    'logi_qa': 'evalscope.benchmarks.logi_qa.logi_qa_adapter',
    'halueval': 'evalscope.benchmarks.halu_eval.halu_eval_adapter',
}
BENCHMARKS = [
    # name, #subsets
    ('gsm8k', 1),
    ('competition_math', 5),
    ('aime26', 1),
    ('mmlu_redux', 57),
    ('arc', 2),
    ('bbh', 27),
    ('ceval', 52),
    ('cmmlu', 67),
    ('humaneval', 1),
    ('mbpp', 1),
    ('bigcodebench', 1),
    ('bigcodebench_hard', 1),
    ('hellaswag', 1),
    ('winogrande', 1),
    ('piqa', 1),
    ('ifeval', 1),
    ('commonsense_qa', 1),
    ('logi_qa', 1),
    ('halueval', 3),
]


def main():
    from evalscope.config import TaskConfig
    from evalscope.api.registry import get_benchmark

    cfg = TaskConfig(model='dummy')
    manifest = []
    for name, expect_subs in BENCHMARKS:
        t0 = time.time()
        record = {'name': name, 'expected_subsets': expect_subs, 'subsets': [], 'error': None}
        try:
            adapter = get_benchmark(name, cfg)
            ds = adapter.load_dataset()
            record['subsets'] = list(ds.keys())
            record['elapsed_s'] = round(time.time() - t0, 1)
            print(f"[OK] {name}: subsets={list(ds.keys())} ({time.time()-t0:.1f}s)", flush=True)
        except Exception as e:  # noqa: BLE001 - keep going, record failure
            record['error'] = f'{type(e).__name__}: {e}'
            record['elapsed_s'] = round(time.time() - t0, 1)
            print(f"[FAIL] {name}: {record['error']}", flush=True)
        manifest.append(record)

    out = os.path.join(WORKSPACE, 'datasets_cache', '_manifest.json')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print('\n=== SUMMARY ===')
    for r in manifest:
        status = 'OK' if not r['error'] else 'FAIL'
        print(f"{status} {r['name']}: subsets={r['subsets']} err={r['error']}")
    print('manifest ->', out)


if __name__ == '__main__':
    sys.exit(main())