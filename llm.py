from llama_cpp import Llama
import os
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),"models","mistral-7b-openorca.Q4_K_M.gguf")


class Mistral7BOpenOrca:
    def __init__(self, model_path: str = MODEL_PATH, 
                 n_ctx: int = 4000, n_threads=None, 
                 n_gpu_layers: int = 0, verbose: bool = True):
        """
        Initialize the Mistral 7B OpenOrca model.
        
        Args:
            model_path: Path to the GGUF model file
            n_ctx: Context window size
            n_threads: Number of CPU threads to use (None for automatic)
            n_gpu_layers: Number of layers to offload to GPU (0 for CPU-only)
            verbose: Whether to print loading progress
            
        Returns:
            Generated text as a string
        """
        self.model_path = model_path
        self.n_ctx = n_ctx
        self.n_threads = n_threads
        self.n_gpu_layers = n_gpu_layers
        self.verbose = verbose
        
        # Suppress some warnings that might appear during loading
        # with warnings.catch_warnings():
        #     warnings.simplefilter("ignore")
        self.llm = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            n_gpu_layers=self.n_gpu_layers,
            verbose=self.verbose
        )
    
    def run(self, prompt: str, system_prompt="You are a helpful assistant.", 
            max_tokens: int = 1024, temperature: float = 0.7, 
            top_p: float = 0.9, echo: bool = False) -> str:
        """
        Run inference on the model with the given prompt.
        
        Args:
            prompt: User input prompt
            system_prompt: System message to guide model behavior
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (lower = more deterministic)
            top_p: Nucleus sampling probability threshold
            echo: Whether to echo back the prompt in the output
            
        Returns:
            Dictionary containing the generated text and other information
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})        
        messages.append({"role": "user", "content": prompt})
        
        output = self.llm.create_chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            echo=echo
        )        
        return output['choices'][0]['message']['content']

# Example usage
print("Loading model...")
model = Mistral7BOpenOrca()
system_prompt = """You are a helpful, respectful and honest assistant. 
Always answer as helpfully as possible, while being safe. 
Your answers should not include any harmful, unethical, racist, sexist, toxic, 
dangerous, or illegal content. Please ensure that your responses are socially 
unbiased and positive in nature."""
    
# Example prompt
user_prompt = "Explain quantum computing in simple terms."
# Run inference
print("Generating response...")
response = model.run(user_prompt, system_prompt)
print("\nResponse:")
print(response)

# class MistralOpenOrca:
#     def __init__(self,
#         gguf_path: str = "models\mistral-7b-openorca.Q4_K_M.gguf", # ,
#         model_id: str = "TheBloke/Mistral-7B-OpenOrca-GGUF",
#         device: str = "cpu"
#     ):
#         """
#         Load a GGUF-quantized Mistral-7B-OpenOrca model for inference.
        
#         Args:
#             gguf_path: Path to the .gguf file.
#             model_id: Hub repo containing the model metadata/tokenizer.
#             device: Device string, e.g. "cpu" or "cuda:0".
#             torch_dtype: Data type to load weights as (float32/16/bfloat16).
#         """
#         # Load tokenizer and model with gguf_file param
#         self.device = device
#         self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=gguf_path)
#             # model_id,
#         #     gguf_file=gguf_path,
#         #     local_files_only=False
#         # )
#         self.model = AutoModelForCausalLM.from_pretrained(pretrained_model_name_or_path=gguf_path).to(device)
#         #self.device = torch.device(device)
#         #self.model.to(self.device)
#         #self.model.eval()

#     def run(self, prompt: str, system_prompt: str = "") -> str:
#         """
#         Generate a response given a user prompt and optional system prompt.
        
#         Args:
#             prompt: The user’s input.
#             system_prompt: An optional system instruction.        
#         Returns:
#             The generated text.
#         """
#         # Construct chat-style formatting
#         full_prompt = (
#             "<|im_start|>system\n"
#             f"{system_prompt}"
#             "<|im_end|>\n"
#             "<|im_start|>user\n"
#             f"{prompt}"
#             "<|im_end|>\n"
#             "<|im_start|>assistant\n"
#         )
#         inputs = self.tokenizer(
#             full_prompt,
#             return_tensors="pt"
#         ).to(self.device)

#         # Generate tokens
#         outputs = self.model.generate(
#             **inputs,
#             max_new_tokens=512,
#             do_sample=True,
#             temperature=0.7,
#             top_p=0.9
#         )
#         # Decode and return
#         return self.tokenizer.batch_decode(
#             outputs
#         )[0]

# from transformers import AutoTokenizer, AutoModelForSequenceClassification

# # tokenizer = AutoTokenizer.from_pretrained("C:\\Users\\ArPaVa\\Documents\\VS Code\\Tesis\\Code\\Tesis\\models\\mistral-7b-openorca.Q4_K_M.gguf")
# model = AutoModelForSequenceClassification.from_pretrained(r"C:/Users/ArPaVa/Documents/VS Code/Tesis/Code/Tesis/models/mistral-7b-openorca.Q4_K_M.gguf")

# input_text = "Your input text goes here"
# encoded_input = tokenizer(input_text, return_tensors='pt')
# output = model(**encoded_input)