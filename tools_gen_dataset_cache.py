import json
import os
import sys
import time

WORKSPACE = os.path.dirname(os.path.abspath(__file__))
CACHE_ROOT = os.path.join(WORKSPACE, 'datasets_cache', 'modelscope')
os.environ['MODELSCOPE_CACHE'] = CACHE_ROOT

BENCHMARKS = [
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
        except Exception as e:
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