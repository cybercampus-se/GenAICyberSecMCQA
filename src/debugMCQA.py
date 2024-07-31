
from templates import *
from utils import *
import time
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
import pandas as pd
from langchain import PromptTemplate
import warnings
import json
import os
from langchain_openai import ChatOpenAI
warnings.filterwarnings('ignore')

import sys
script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
# Change the current working directory to the script's directory
os.chdir(script_dir)

CONFIG_FILE = 'config_ccnp_vision.yaml'
config = load_config(CONFIG_FILE)
# Assign values from the configuration
WORKSPACE_DIC = config['workspace_dir']
MODEL_PATH = config['model_paths']
TEMPERATURE = config['model_parameters']['temperature']
MAX_OUTPUT_TOKENS = config['model_parameters']['max_output_tokens']
MAX_SAMPLING_RATE = config['max_sampling_rate']
NUM_OF_SHUFFLES = config['num_of_shuffles']
NUMBER_OF_QUESTIONS = config['number_of_questions']
TRACK_RESULTS = config['track_results']
PRINT_RESULTS = config['print_results']
DATASET_NAME = config['dataset_name']
DATE = time.strftime(config['date_format'])
CONTROL_OUTPUT = config['control_output']

OUTPUT_PATH = config['output_path'].format(
    number_of_questions=NUMBER_OF_QUESTIONS,
    dataset_name=DATASET_NAME,
    date=DATE
)

OUTPUT_EVALUATION = config['output_evaluation'].format(
    output_path=OUTPUT_PATH,
    dataset_name=DATASET_NAME
)

OUTPUT_EVALUATION_DETAILED = config['output_evaluation_detailed'].format(
    number_of_questions=NUMBER_OF_QUESTIONS,
    dataset_name=DATASET_NAME,
    date=DATE
)

OUTPUT_EVALUATION_JSON = config['output_evaluation_json'].format(
    number_of_questions=NUMBER_OF_QUESTIONS,
    dataset_name=DATASET_NAME,
    date=DATE
)

if config['create_results_folder'] and not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

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
#questions  = pd.read_csv(QUESTIONS_BANK)
#Randomly take NUMBER_OF_QUESTIONS (default 120)
try:
    questions = questions.sample(n=NUMBER_OF_QUESTIONS,random_state=42)
except:
    print("Number of questions is greater than the number of questions in the questionbank. Max Number taken")

#questions = extract_answer_from_text_file("../data/questionbank_cisco_CCNP.txt")
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
prompt_template = PromptTemplate.from_template(PROMPT_TEMPLATE)

import requests
import json
from openai import OpenAI
import copy
# Define the URL and the data payload

#Iterate over each model definied in the MODEL_PATH dictionary
for model, model_path in MODEL_PATH.items():
     #Load the model wiht LLamaCpp
    print("Load Model ...")
    if "ollama" in model_path:
        model_name = model_path.split("ollama:")[1]
        #with this the ollama api can be accessed and also the raw model
        url = 'http://localhost:11434/api/generate'
        # Set the headers for the request
        headers = {
            'Content-Type': 'application/json'
        }
        #for the Ollama OpenAI interface
        client = OpenAI(
            base_url = 'http://localhost:11434/v1',
            api_key='ollama', # required, but unused
        )
    elif "vllm" in model_path:
        model_name = model_path.split("vllm:")[1]
        client = OpenAI(
            base_url="http://localhost:8086/v1",
            api_key="test",
        )
    else:    
        llm = LlamaCpp(
            model_path= model_path,
            n_gpu_layers=-1,
            n_batch=512,
            n_ctx=1100,
            temperature=TEMPERATURE,
            max_tokens = MAX_OUTPUT_TOKENS,
            #callback_manager=callback_manager,
            verbose=False,  # Verbose is required to pass to the callback manager
        )
        chain = prompt_template | llm
    print("Model loaded")

    for shuffled_iteration in range(NUM_OF_SHUFFLES):
        llm_exam_result = pd.DataFrame(columns = ["Model", "QuestionIndex", "SamplingIndex", "NumberOfChoices", "NumberOfCorrectLLMAnswers", "NumberOfIncorrectLLMAnswers", "NumberOfCorrectExamAnswers", "Ratio", "LLM_Answer", "Exam_Answers", "Answered_Correctly",  "Too_Many_answers"]) 
        #Iterate over each question in the question dataframe
        #Start the timer
        start_time = time.time()
        for index_question, row in questions.iterrows():
            # to test vision model
            if row["image"] == 'nan':
                continue  
            question = row['question']
            choices = row['choices']
            answers = row['answer']
            num_of_correct_answer = len(answers)
            num_of_choices = len(choices)

            choices = format_choices_for_llm(choices)
            #TODO why so?
            #num_of_choices = choices.count('\n') + 1
            #Only if shuffle is enabled, shuffle the choices
            if shuffled_iteration > 0:
                choices, answers = shuffle_choices_and_update_answer(row['choices'], row['answer'])
                #TODO does the amount of answers change?
                #num_of_correct_answer = len(answers)
                choices = format_choices_for_llm(choices)
            #Empty the char_probabilities dictionary for each question
            char_probabilities = {}
            valid_question_answer = False
            #TODO Iterate over the maximum sampling rate. Does this make sense with Temperature 0???
            for index_sampling in range(MAX_SAMPLING_RATE):
                if "ollama_raw" in model_path:
                    # use the raw olalma interface. the default (internal) template is not used.
                    payload = {
                        "model": model_name,
                        "prompt": prompt_template.format(Exam_Question=row['question'],Exam_Choices=choices),
                        "raw": True,
                        "stream": False,
                        "options": {
                            "temperature": TEMPERATURE,
                            "seed": 42
                        },
                    }
                    # Make the POST request
                    response = requests.post(url, headers=headers, data=json.dumps(payload))
                    llm_answer = response.json()["response"]
                elif "ollama" in model_path:
                    #this is used of the OLLAMA openai API format
                    dialogs = copy.deepcopy(PROMPT_TEMPLATE)
                    for dialog in dialogs:
                        if "{Exam_Question}" in dialog["content"] and "{Exam_Choices}" in dialog["content"]:
                            dialog["content"] = dialog["content"].format(Exam_Question=row['question'], Exam_Choices=choices)
                    response = client.chat.completions.create(
                    model=model_name,
                    messages=dialogs,
                    temperature=TEMPERATURE,
                    max_tokens=MAX_OUTPUT_TOKENS,
                    )
                    llm_answer = response.choices[0].message.content
                    print(dialogs[-1])
                elif "vllm" in model_path:
                    image_base64= row["image"]
                    response = client.chat.completions.create(
                    model="microsoft/Phi-3-vision-128k-instruct",
                    messages=[
                        {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_template.format(Exam_Question=row['question'],Exam_Choices=choices)},
                            {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}",
                            }, 
                            },
                        ],
                        }
                    ],
                    max_tokens=300,
                    )
                    llm_answer = response.choices[0].message.content
                else:
                    llm_answer = chain.invoke({"Exam_Question" : row['question'], "Exam_Choices" : choices})  
                # Check if the answer is in the expected format
                print("LLM output: ",llm_answer)
                if extract_answer(llm_answer) is not None:
                    # Extract the correct answers from the LLM answer and analyse the answer
                    num_of_correct_llm_answer, answerLLm, too_many_answers, answered_correctly, number_of_incorrect_llm_answers = evaluation_sampling(llm_answer, answers, num_of_correct_answer)
                    #Save the current sampling index -- How of the question has been asked until the answer was in the correct format
                    sample_Index = index_sampling
                    valid_question_answer = True
                    break
            
            #Depending on the result of the answer, add the result to the dataframe
            #TODO: if no valid answer is found(extract_answer(llm_answer)==None), the function breaks. Or the answer from last iteration is taken!!! valid_question_answer not set to false again. NumberOfIncorrectLLMAnswers is reused from last run in this case. Should be num_of_choices.
            if not valid_question_answer:
                new_row = pd.DataFrame({"Model": [model], "QuestionIndex": [index_question], "SamplingIndex": [-1], "NumberOfChoices": num_of_choices, "NumberOfCorrectLLMAnswers": [0], "NumberOfIncorrectLLMAnswers": num_of_choices, "NumberOfCorrectExamAnswers": [num_of_correct_answer], "Ratio": [-1], "LLM_Answer": [llm_answer], "Exam_Answers": [answers]})
                llm_exam_result = pd.concat([llm_exam_result, new_row], ignore_index=True)
            else:
                new_row = pd.DataFrame({"Model": [model], "QuestionIndex": [index_question], "SamplingIndex": [sample_Index],  "NumberOfChoices": num_of_choices, "NumberOfIncorrectLLMAnswers": number_of_incorrect_llm_answers , "NumberOfCorrectLLMAnswers": [num_of_correct_llm_answer], "NumberOfCorrectExamAnswers": [num_of_correct_answer], "Ratio": [num_of_correct_llm_answer/num_of_correct_answer], "LLM_Answer": [answerLLm], "Exam_Answers": [answers], "Answered_Correctly" : [answered_correctly], "Too_Many_answers": [too_many_answers]})
                llm_exam_result = pd.concat([llm_exam_result, new_row], ignore_index=True)
                #
                valid_question_answer = False

        answered_correctly = False

        if PRINT_RESULTS:
            print(llm_exam_result)

        if TRACK_RESULTS:
            llm_exam_result.to_pickle(f"{OUTPUT_PATH}{NUMBER_OF_QUESTIONS}_questions_{DATASET_NAME}_{model}_shuffled_{shuffled_iteration}.pkl")
       
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

#stop script

import os

###########################################################
#Evaluation of the results and calculation of the statistics
###########################################################
for model, model_path in MODEL_PATH.items():
    print(f"Model: {model}")
    for shuffled_iteration in range(NUM_OF_SHUFFLES):
        # Get the correct output path based on the updated date
        pickle_path = os.path.join(OUTPUT_PATH, f"{NUMBER_OF_QUESTIONS}_questions_{DATASET_NAME}_{model}_shuffled_{shuffled_iteration}.pkl")
        llm_exam_result = pd.read_pickle(pickle_path)
        evaluation_df = evaluation(llm_exam_result)
        #Concat the evaluation dataframe to the complete dataframe
        shuffled_evalutation_df = pd.concat([shuffled_evalutation_df, evaluation_df], ignore_index=True)
model_statistics = calculate_model_statistics(shuffled_evalutation_df)
print(model_statistics)
#shuffled_evalutation_df.to_pickle(OUTPUT_EVALUATION_DETAILED)
#model_statistics.to_pickle(OUTPUT_EVALUATION)
if "mmlu" in DATASET_NAME:
    HELM_RESULT = pd.read_csv(config['helm_result'])
    plot_evaluation_MMLU(model_statistics, HELM_RESULT, "Own Approach", "HELM", title="Own Approach vs. HELM Official",save_path=f"{OUTPUT_PATH}llm_5_Shot_{DATASET_NAME}.png")
else:
    plot_evaluation_CCNA(model_statistics, hline_accuracy=0.8, hline_partial=0.8, title=DATASET_NAME,save_path=f"{OUTPUT_PATH}llm_5_Shot_{DATASET_NAME}.png")
