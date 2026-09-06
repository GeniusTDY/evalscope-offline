---
license: apache-2.0
dataset_info:
- config_name: dialogue
  features:
  - name: knowledge
    dtype: string
  - name: dialogue_history
    dtype: string
  - name: right_response
    dtype: string
  - name: hallucinated_response
    dtype: string
  splits:
  - name: data
    num_bytes: 6212598
    num_examples: 10000
  download_size: 3448632
  dataset_size: 6212598
- config_name: dialogue_samples
  features:
  - name: knowledge
    dtype: string
  - name: dialogue_history
    dtype: string
  - name: response
    dtype: string
  - name: hallucination
    dtype: string
  splits:
  - name: data
    num_bytes: 5303515
    num_examples: 10000
  download_size: 2834937
  dataset_size: 5303515
- config_name: general
  features:
  - name: ID
    dtype: string
  - name: user_query
    dtype: string
  - name: chatgpt_response
    dtype: string
  - name: hallucination
    dtype: string
  - name: hallucination_spans
    sequence: string
  splits:
  - name: data
    num_bytes: 2905898
    num_examples: 4507
  download_size: 1819331
  dataset_size: 2905898
- config_name: qa
  features:
  - name: knowledge
    dtype: string
  - name: question
    dtype: string
  - name: right_answer
    dtype: string
  - name: hallucinated_answer
    dtype: string
  splits:
  - name: data
    num_bytes: 5486422
    num_examples: 10000
  download_size: 3751109
  dataset_size: 5486422
- config_name: qa_samples
  features:
  - name: knowledge
    dtype: string
  - name: question
    dtype: string
  - name: answer
    dtype: string
  - name: hallucination
    dtype: string
  splits:
  - name: data
    num_bytes: 5112196
    num_examples: 10000
  download_size: 3427901
  dataset_size: 5112196
- config_name: summarization
  features:
  - name: document
    dtype: string
  - name: right_summary
    dtype: string
  - name: hallucinated_summary
    dtype: string
  splits:
  - name: data
    num_bytes: 46408787
    num_examples: 10000
  download_size: 27990918
  dataset_size: 46408787
- config_name: summarization_samples
  features:
  - name: document
    dtype: string
  - name: summary
    dtype: string
  - name: hallucination
    dtype: string
  splits:
  - name: data
    num_bytes: 42743472
    num_examples: 10000
  download_size: 25506458
  dataset_size: 42743472
configs:
- config_name: dialogue
  data_files:
  - split: data
    path: dialogue/data-*
- config_name: dialogue_samples
  data_files:
  - split: data
    path: dialogue_samples/data-*
- config_name: general
  data_files:
  - split: data
    path: general/data-*
- config_name: qa
  data_files:
  - split: data
    path: qa/data-*
- config_name: qa_samples
  data_files:
  - split: data
    path: qa_samples/data-*
- config_name: summarization
  data_files:
  - split: data
    path: summarization/data-*
- config_name: summarization_samples
  data_files:
  - split: data
    path: summarization_samples/data-*
---
