from llama_cpp import Llama
import os
import gc
import time
from settings import MODELS_DIR
MODEL_PATH = os.path.join(MODELS_DIR, "mistral-7b-openorca.Q4_K_M.gguf")


class Mistral7BOpenOrca:
    def __init__(self, model_path: str = MODEL_PATH, 
                 n_ctx: int = 8000, n_threads=None, 
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
            max_tokens: int = 1000, temperature: float = 0.4, 
            top_p: float = 0.9) -> str:
        """
        Run inference on the model with the given prompt.
        
        Args:
            prompt: User input prompt
            system_prompt: System message to guide model behavior
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (lower = more deterministic)
            top_p: Nucleus sampling probability threshold
            
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
            top_p=top_p
        )        
        return output['choices'][0]['message']['content']
    
    def unload_model(self):
        if self.llm:
            self.llm.__del__()  # Calls internal cleanup
            del self.llm
            self.llm = None
            gc.collect()

def chunking_list(source_list, lines_per_chunk, overlap):
    if len(source_list) <= lines_per_chunk:
        return [source_list]
    result = []
    start = 0
    while start < len(source_list):
        end = min(start + lines_per_chunk, len(source_list))
        result.append(source_list[start:end])
        start += (lines_per_chunk - overlap)
    return result

def summarize_transcription(transcription_file_content: list, audio_context_info: str="", lines_per_chunk = 40, overlap_lines = 5):
    
    user_prompt_template = """Eres un asistente especializado en análisis de grabaciones de audio. Tu tarea es: 
Identificar los temas tratados. Por cada tema redacta un párrafo extenso explicando detalladamente lo ocurrido relacionado a ese tema. No copies la transcripción, debe ser un resumen.

Considera que trabajas con transcripciones automáticas que pueden contener errores.
El resultado tiene que ser un texto por cada tema con un resumen de lo tratado e indicando a que tiempos del audio corresponden. Ten en cuenta que un tema normalmente abarca varias líneas de la transcripción.
{audio_context_info}

Audio segment:
{text}

"""
    
    model = Mistral7BOpenOrca()    
    
    chunks = chunking_list(transcription_file_content, lines_per_chunk, overlap_lines)
    results = []
    for chunk in chunks:
        if chunk and (len(chunk) > 1 or (len(chunk) == 1 and len(chunk[0]) > 20)):
            chunk_start_time = None
            chunk_end_time = None
            chunk_text = ""
            for i, line in enumerate(chunk):              
                try:
                    # text = f"{i+1}. {line.split('):')[1].strip()}"
                    time_part = line.split('):')[0] + ")"
                    start_time = float(time_part.split('to')[0].split('From')[1].strip())
                    end_time = float(time_part.split('to')[1].split(')')[0].strip())
                    
                    if chunk_start_time is None:
                        chunk_start_time = start_time
                    chunk_end_time = end_time
                    chunk_text += f"{line}\n"
                except:
                    pass
                
            user_prompt = user_prompt_template.format(text=chunk_text, audio_context_info=audio_context_info)
            for attempt in range(3):
                summary = model.run(user_prompt)

                if summary:
                    break
                print(f"Attempt {attempt + 1} failed: Summary is empty. Retrying")

            results.append({
                'start_time': chunk_start_time,
                'end_time': chunk_end_time,
                'chunk': chunk,
                'summary': summary
            })    
            print(summary)
    model.unload_model()
    del model
    gc.collect()
    return results
