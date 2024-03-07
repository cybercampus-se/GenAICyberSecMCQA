'''
1. install from within docker pytorch23.10
python -m venv .venv 
source .venv/bin/activate  
pip install langchain
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python  
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python[server]

2.download model
# pip install huggingface-hub
# huggingface-cli download TheBloke/llama2_70b_chat_uncensored-GGUF llama2_70b_chat_uncensored.Q5_K_M.gguf --local-dir . --local-dir-use-symlinks False

# TheBloke/Yi-34B-200K-GGUF yi-34b-200k.Q5_K_M.gguf
# TheBloke/dolphin-2.5-mixtral-8x7b-GGUF dolphin-2.5-mixtral-8x7b.Q5_K_M.gguf 
# TheBloke/phi-2-GGUF phi-2.Q5_K_M.gguf
# TheBloke/llama2_70b_chat_uncensored-GGUF llama2_70b_chat_uncensored.q5_K_M.gguf


3.run server:
python3 -m llama_cpp.server --model mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf --n_gpu_layers 128
'''

import time

# get the start time
st = time.time()

from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

n_gpu_layers = 128  # Change this value based on your model and your GPU VRAM pool.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.


#supported models
model_dict = {
    "llama2_70b": "./llama2_70b_chat_uncensored.Q5_K_M.gguf",
    "mixtral": "./mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf",
             }
llm_model =model_dict["mixtral"]



llm = LlamaCpp(
    model_path=llm_model,
    temperature=0.7,
    max_tokens=512,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    top_p=0.95,
    top_k=40,
    callback_manager=callback_manager, 
    verbose=True, # Verbose is required to pass to the callback manager
)

prompt = "Tell me about AI"
prompt_template=f'''[INST] <<SYS>>
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
<</SYS>>
{prompt}[/INST]

'''

print(llm(prompt_template))
# get the end time
et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
