from dataclasses import dataclass


@dataclass
class SwiftInferArgs:
    model_id_or_path: str
    model_type: str
    infer_backend: str = 'vllm'
    max_new_tokens: int = 2048
    temperature: float = 0.1
    max_batch_size: int = 16

class SwiftInfer:

    def __init__(self, args: SwiftInferArgs):

        if args.infer_backend == 'pt':
            self.engine: InferEngine = PtEngine(args.model_id_or_path, max_batch_size=args.max_batch_size)
        elif args.infer_backend == 'vllm':
            from swift.llm import VllmEngine
            self.engine: InferEngine = VllmEngine(args.model_id_or_path, max_model_len=8192)
        elif args.infer_backend == 'lmdeploy':
            from swift.llm import LmdeployEngine
            self.engine: InferEngine = LmdeployEngine(args.model_id_or_path)
        else:
            raise ValueError(f'Unsupported infer_backend: {args.infer_backend}')


        self.request_config = RequestConfig(
            max_tokens=args.max_new_tokens,
            temperature=args.temperature,
            stream=False
        )

    def predict(self, system: str, query: str, history: list):

        # messages: [{"role": "system", "content": "<SYSTEM_PROMPT>"},



        messages = []
        if system.strip():
            messages.append({'role': 'system', 'content': system})


        for qa_pair in history:

            user_answer, model_response = qa_pair
            messages.append({'role': 'user', 'content': user_answer})
            messages.append({'role': 'assistant', 'content': model_response})


        messages.append({'role': 'user', 'content': query})

        infer_request = InferRequest(messages=messages)


        response = self.engine.infer([infer_request], self.request_config)


        result_text = response[0].choices[0].message.content.strip()

        return result_text
