from prompt_templates import *

MODEL_PATH = {"Mixtral-8x-7b": "mixtral-8x7b-instruct-v0.1.Q4_K_M",
               "Llama2-70b": "llama2_70b_chat_uncensored.Q5_K_M",
               "Dolphin-2.5": "dolphin-2.5-mixtral-8x7b.Q5_K_M",
               "Yi-34b": "yi-34b-200k.Q5_K_M",
               "Phi-2": "phi-2.Q5_K_M"}

#Set prompt template

PROMPT_TEMPLATE = FEW_SHOT_TEMPLATE

#Set output file name

OUTPUT_PICKEL = "../data/llm_output_dataframe.pkl"

#Set max sampling rate

MAX_SAMPLING_RATE = 10