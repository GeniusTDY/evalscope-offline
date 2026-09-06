import json, os
meta_dir = '/workspace/evalscope/benchmarks/_meta'
targets = ['gsm8k','competition_math','aime26','mmlu_redux','arc','bbh','ceval','cmmlu',
           'humaneval','mbpp','bigcodebench','bigcodebench_hard','hellaswag','winogrande',
           'piqa','ifeval','commonsense_qa','logi_qa','halueval']
for name in targets:
    mp = os.path.join(meta_dir, name + '.json')
    d = json.load(open(mp))
    m = d.get('meta') or {}
    sublist = m.get('subset_list')
    n_sub = len(sublist) if isinstance(sublist, list) else 0
    # accumulate evaluated samples from statistics.subset_stats where name in subset_list
    st = d.get('statistics') or {}
    total = st.get('total_samples')
    print(f'{name}: dataset_id={m.get("dataset_id")!r} subsets={n_sub} total_samples={total}')