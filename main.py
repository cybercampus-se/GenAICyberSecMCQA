import argparse
from templates import *
from utils import *
import time
import pandas as pd
from langchain_core.prompts import PromptTemplate
import warnings
import json
import os
import requests
import json
from openai import OpenAI
import copy
from dotenv import load_dotenv
import sys
#script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
## Change the current working directory to the script's directory
#os.chdir(script_dir)
#load api key from .env file
load_dotenv()
# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--config', help='Path to the config file')
#add model as argument
parser.add_argument('--model', help='Model to use')
args = parser.parse_args()
# Load the config
config = load_config(args.config)
# Assign values from the configuration
MODEL_PATH = config.get('model_paths')
#in case the model is passed as an argument
if args.model:
    # overwrite MODEL_PATH with a dict with 1 entry: "Claude 3.5 Sonnet (new): "anthropic:claude-3-5-sonnet-20241022
    MODEL_PATH = {args.model: "vllm:"+args.model}
TEMPERATURE = config.get('model_parameters', {}).get('temperature')

MAX_OUTPUT_TOKENS = config.get('model_parameters', {}).get('max_output_tokens')
MAX_SAMPLING_RATE = config.get('max_sampling_rate')
NUM_OF_SHUFFLES = config.get('num_of_shuffles')
NUMBER_OF_QUESTIONS = config.get('number_of_questions')
TRACK_RESULTS = config.get('track_results')
PRINT_RESULTS = config.get('print_results')
DATASET_NAME = config.get('dataset_name')
CONTROL_OUTPUT = config.get('control_output')


# Get the directory where main.py is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Then when setting up OUTPUT_PATH, make it relative to SCRIPT_DIR
OUTPUT_PATH = os.path.join(SCRIPT_DIR, config['output_path'].format(
    number_of_questions=NUMBER_OF_QUESTIONS,
    dataset_name=DATASET_NAME
))

# Do the same for other paths
OUTPUT_EVALUATION = os.path.join(SCRIPT_DIR, config['output_evaluation'].format(
    output_path=OUTPUT_PATH,
    dataset_name=DATASET_NAME
))

OUTPUT_EVALUATION_DETAILED = os.path.join(SCRIPT_DIR, config['output_evaluation_detailed'].format(
    number_of_questions=NUMBER_OF_QUESTIONS,
    dataset_name=DATASET_NAME
))

OUTPUT_EVALUATION_JSON = os.path.join(SCRIPT_DIR, config['output_evaluation_json'].format(
    number_of_questions=NUMBER_OF_QUESTIONS,
    dataset_name=DATASET_NAME
))

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH, exist_ok=True)

QUESTIONS_BANK = config['questions_bank']
PROMPT_TEMPLATE = config['prompt_template']

#Gets the variable from the templates.py file
PROMPT_TEMPLATE = globals()[PROMPT_TEMPLATE]

#Save the metadata as a JSON file, if TRACK_RESULTS is set to True
if TRACK_RESULTS:
    parameters = {
        "RUN_NAME": DATASET_NAME, 
        "DATE": time.strftime("%Y-%m-%d %H:%M:%S"),  
        "QUESTION_BANK": QUESTIONS_BANK,  
        "MAX_SAMPLING_RATE": MAX_SAMPLING_RATE,  
        "NUM_OF_SHUFFLES": NUM_OF_SHUFFLES,  
        "FEW_SHOT_TEMPLATE": PROMPT_TEMPLATE,  
        "TEMPERATURE": TEMPERATURE,  
        "MAX_TOKENS": MAX_OUTPUT_TOKENS  
    }
    with open(OUTPUT_EVALUATION_JSON, 'w') as f:
        json.dump(parameters, f)

#Print all the parameters if CONTROL_OUTPUT is set to True
if CONTROL_OUTPUT:
    print("Parameters:")
    print("RUN_NAME:", DATASET_NAME)
    print("DATE:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print("QUESTION_BANK:", QUESTIONS_BANK)
    print("MAX_SAMPLING_RATE:", MAX_SAMPLING_RATE)
    print("NUM_OF_SHUFFLES:", NUM_OF_SHUFFLES)
    print("FEW_SHOT_TEMPLATE:", PROMPT_TEMPLATE)
    print("TEMPERATURE:", TEMPERATURE)
    print("MAX_TOKENS:", MAX_OUTPUT_TOKENS)
    print("OUTPUT_PATH:", OUTPUT_PATH)
    print("OUTPUT_EVALUATION:", OUTPUT_EVALUATION)
    print("OUTPUT_EVALUATION_DETAILED:", OUTPUT_EVALUATION_DETAILED)
    print("OUTPUT_EVALUATION_JSON:", OUTPUT_EVALUATION_JSON)
    
    for model, path in MODEL_PATH.items():
        print(f"Model: {model}, Path: {path}")
    

###########################################
#Main programm for the evaluation of the LLM
###########################################

#Create a dataframe with the size of NUM_OF_SHUFFLES which contains the dataframe llm_exam_result
shuffled_evalutation_df = pd.DataFrame(columns=[ 'Number of Questions','Correctly Answered','Incorrectly Answered','Accuracy','Accuracy Partial'])

#Read the questions from the questionsbank
questions  = pd.read_parquet(QUESTIONS_BANK)
try:
   questions = questions.sample(n=NUMBER_OF_QUESTIONS,random_state=42)
except:
   print("Number of questions is greater than the number of questions in the questionbank. Max Number taken")

#Iterate over each model definied in the MODEL_PATH dictionary
for model, model_path in MODEL_PATH.items():
    print("Loading Model ...")
    if "ollama" in model_path:
        model_name = model_path.split("ollama:")[1]
        #for the Ollama OpenAI interface
        client = OpenAI(
            base_url = 'http://localhost:11434/v1',
        )
    elif "vllm" in model_path:
        model_name = model_path.split("vllm:")[1]
        client = OpenAI(
            base_url="http://localhost:8086/v1",
            api_key="test")
    elif "openai" in model_path:
        model_name = model_path.split("openai:")[1]
        client = OpenAI()
    elif "nim" in model_path:
        model_name = model_path.split("nim:")[1]
        nim_api_key = os.getenv("NIM_API_KEY")
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=nim_api_key)
    elif "anthropic" in model_path:
        model_name = model_path.split("anthropic:")[1]
        import anthropic
        client = anthropic.Anthropic()
        print("Model loaded")
    elif "nom" in model_path:
        model_name = model_path.split("nom:")[1]
        print("Model loaded")
    else:
        #throw an exception if the model is not found
        raise Exception("Model not found")

    for shuffled_iteration in range(NUM_OF_SHUFFLES):
        llm_exam_result = pd.DataFrame(columns = ["Model", "QuestionIndex", "SamplingIndex", "NumberOfChoices", "NumberOfCorrectLLMAnswers", "NumberOfIncorrectLLMAnswers", "NumberOfCorrectExamAnswers", "Ratio", "LLM_Answer", "Exam_Answers", "Answered_Correctly",  "Too_Many_answers"]) 
        #Iterate over each question in the question dataframe
        #Start the timer
        start_time = time.time()
        for index_question, row in questions.iterrows():
            question = row['question']
            choices = row['choices']
            answers = row['answer']
            num_of_correct_answer = len(answers)
            num_of_choices = len(choices)

            choices = format_choices_for_llm(choices)
            if shuffled_iteration > 0:
                choices, answers = shuffle_choices_and_update_answer(row['choices'], row['answer'],seed=shuffled_iteration)
                choices = format_choices_for_llm(choices)
            valid_question_answer = False
            for index_sampling in range(MAX_SAMPLING_RATE):
                #Iterate over the maximum sampling rate. Do not use for Temperature = 0
                if type(PROMPT_TEMPLATE) is list:
                    #in case of the few shot conversation chat template
                    messages = copy.deepcopy(PROMPT_TEMPLATE)
                    for dialog in messages:
                        if "{Exam_Question}" in dialog["content"] and "{Exam_Choices}" in dialog["content"]:
                            dialog["content"] = dialog["content"].format(Exam_Question=row['question'], Exam_Choices=choices)
                else:    
                    messages = [{"role": "user", "content": PromptTemplate.from_template(PROMPT_TEMPLATE).format(Exam_Question=row['question'],Exam_Choices=choices)}]           

                if "vllm"  in model_path or "openai"  in model_path or "ollama" in model_path or "nim" in model_path:
                    try:
                        image_base64= row["image"]
                        if image_base64 != 'nan':
                            text = [
                            {"type": "text", "text": messages[-1]["content"]},
                                    {"type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{image_base64}",
                                    }}
                            ]
                            messages[-1]["content"] = text
                    except:
                        pass

                    response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=TEMPERATURE,
                    max_tokens=MAX_OUTPUT_TOKENS,
                    )
                    llm_answer = response.choices[0].message.content
                elif "nom" in model_path:
                    try:
                        image_base64= row["image"]
                        # with open("dog.jpeg", "rb") as f:
                        #     image_b64 = base64.b64encode(f.read()).decode()
                        if image_base64 != 'nan':
                            text = [
                            {"type": "text", "text": messages[-1]["content"]},
                                    {"type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{image_base64}",
                                    }}
                            ]
                            messages[-1]["content"] = text
                    except:
                        pass
                    ####
                    invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
                    stream = False

                    nim_api_key = os.getenv("NIM_API_KEY")
                    headers = {
                    "Authorization": f"Bearer {nim_api_key}",
                    "Accept": "text/event-stream" if stream else "application/json"
                    }

                    payload = {
                    "model": model_name,
                    "messages": messages,
                    "max_tokens": MAX_OUTPUT_TOKENS,
                    "temperature": TEMPERATURE,
                    "top_p": 0.70,
                    "stream": stream
                    }
                    response = requests.post(invoke_url, headers=headers, json=payload)
                    llm_answer = response.choices[0].message.content

                elif "anthropic" in model_path:
                    try:
                        image_base64= row["image"]
                        if image_base64 != 'nan':
                            text = [
                            {"type": "text", "text": messages[-2]["content"]},
                           
                                    {"type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/png",
                                        "data": image_base64,
                                    }}
                            ]
                            messages[-2]["content"] = text
                    except:
                        pass
                    llm_answer = client.messages.create(
                            max_tokens=MAX_OUTPUT_TOKENS,
                            model=model_name,
                            messages=messages,                          
                        ).content[0].text
                else:
                    raise Exception("Model not found")
                # Check if the answer is in the expected format
                print("LLM output: ",llm_answer)
                if extract_answer(llm_answer) is not None:
                    # Extract the correct answers from the LLM answer and analyse the answer
                    num_of_correct_llm_answer, answerLLm, too_many_answers, answered_correctly, number_of_incorrect_llm_answers = evaluation_sampling(llm_answer, answers, num_of_correct_answer)
                    #Save the current sampling index -- How of the question has been asked until the answer was in the correct format
                    sample_Index = index_sampling
                    valid_question_answer = True
                    print("Extracted answer: ",answerLLm)
                    break
            
            #Depending on the result of the answer, add the result to the dataframe
            if not valid_question_answer:
                new_row = pd.DataFrame({"Model": [model], "QuestionIndex": [index_question], "SamplingIndex": [-1], "NumberOfChoices": num_of_choices, "NumberOfCorrectLLMAnswers": [0], "NumberOfIncorrectLLMAnswers": num_of_choices, "NumberOfCorrectExamAnswers": [num_of_correct_answer], "Ratio": [-1], "LLM_Answer": [llm_answer], "Exam_Answers": [answers]})
                llm_exam_result = pd.concat([llm_exam_result, new_row], ignore_index=True)
            else:
                new_row = pd.DataFrame({"Model": [model], "QuestionIndex": [index_question], "SamplingIndex": [sample_Index],  "NumberOfChoices": num_of_choices, "NumberOfIncorrectLLMAnswers": number_of_incorrect_llm_answers , "NumberOfCorrectLLMAnswers": [num_of_correct_llm_answer], "NumberOfCorrectExamAnswers": [num_of_correct_answer], "Ratio": [num_of_correct_llm_answer/num_of_correct_answer], "LLM_Answer": [llm_answer], "Exam_Answers": [answers], "Answered_Correctly" : [answered_correctly], "Too_Many_answers": [too_many_answers]})
                llm_exam_result = pd.concat([llm_exam_result, new_row], ignore_index=True)
                valid_question_answer = False

        answered_correctly = False

        if PRINT_RESULTS:
            print(llm_exam_result)

        if TRACK_RESULTS:
            # When saving the file
            safe_model_name = model.replace("/", "_")
            save_filename = f"{NUMBER_OF_QUESTIONS}_questions_{DATASET_NAME}_{safe_model_name}_shuffled_{shuffled_iteration}.pkl"
            save_path = os.path.join(OUTPUT_PATH, save_filename)
            # Create directory if it doesn't exist
            os.makedirs(OUTPUT_PATH, exist_ok=True)
            print("saving to: ",save_path)
            # Save the file
            llm_exam_result.to_pickle(save_path)

       
        evaluation_df = evaluation(llm_exam_result)
        #Concat the evaluation dataframe to the complete dataframe
        shuffled_evalutation_df = pd.concat([shuffled_evalutation_df, evaluation_df], ignore_index=True)

        if PRINT_RESULTS:
            print(shuffled_evalutation_df)

        end_time = time.time()
        elapsed_time = end_time - start_time


        if PRINT_RESULTS:
            print("Time taken:", elapsed_time, "seconds")


model_statistics = calculate_model_statistics(shuffled_evalutation_df)

if PRINT_RESULTS:
    print(model_statistics)

if TRACK_RESULTS:
    shuffled_evalutation_df.to_pickle(OUTPUT_EVALUATION_DETAILED)
    model_statistics.to_pickle(OUTPUT_EVALUATION)
