# %% [markdown]
# # Notes
# 
# ### Dataset MMLU Computer Security:
# * https://huggingface.co/datasets/cais/mmlu/viewer/computer_security/test
# 
# ### Official HELM Result MMLU Computer Security
# https://crfm.stanford.edu/helm/mmlu/latest/#/leaderboard
# 
# ### Big Mistake in Prompt:
# **Added the """ after a linebreak e.g.** <br>
# Anwser: <br>
# """<br>
# **Correct way:<br>**
# Anwser:"""
# 
# ## Cisco Pass exam
# * https://learningnetwork.cisco.com/s/question/0D53i00000U2TO7CAN/what-is-the-pass-percentage-required-to-get-in-ccna-200301
# * 825 / 1000 (82 %)
# * Every (paid) exam takes 120 min and has about 120 Questions
# 
# ## HELM  implementation: 
# * Max_output tokens to restrict the possible outputs to the max number of answers possibilities
# * Temperature = 0
# * Joint strategy (all answer choices are presented at once)
# * Short Introduction: The following are multiple choice questions (with answers) about computer security.
# * (Paper: https://arxiv.org/pdf/2211.09110.pdf)
# 
# ## HELM / Paper Imprreovements:
# * Sampling --> std, mean min / max accuracy
# 
# # CCNA 201-301 - 5 Shot like HELM with Answer format: Answer: ABC or Answer: A <br>
# ### Oberservations Phi:
# * Output of Phi-Model always empty, similiar config as mmlu (temp=0, max_output_token = 2), by increasing temp the result of Phi is better but still not close to the other models<br>
# * Also have to increase the Max Output Tokens otherwise only \n as response
# * Possible approach: Increasing temp and output_tokens, regex pattern that searchs for string in responses
# ### Oberservations Llama 2:
# * LLama 2 results are much worse in comp. to single shot with Correct Answer: ['A', 'B'] and temp =0.7 and no limit to output tokens
# 
# 
# ## New 
# 
# * ~~Yi, Llama 1, Llama 2 (nicht uncensored), Mixtral, Phi-2 --> Für MMLU~~
# * Change Answer to Letter (Frage: Exam Answer sind in HELM so, doch ändern?)
# * ~~Prompt without whitespace --> extra ~~
# * Ungeshuffeld vs HELM Grafik --> HELM vs unsere
# * Shuffle (min-max) vs nicht shuffeln
# * Dokumentieren --> Prompt, Changes Correct Answer Helm implementierung
# * Folien für Präsentation --> Implementierung, Ergebnisse (MMLU ähnlich wie HELM) --> , mit mehr Tokens CCNA Paper (Questionsbank nicht veröffentlicht) --> Weg Cisco (350-701 SCOR), Vetgleich zum Paper
# * Alles Dokumentieren
# * **How many points to pass? --> Horizontale** 

# %%
from templates import *
import time
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
import pandas as pd
from langchain import PromptTemplate
import re
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import random
import warnings
import numpy as np
import yaml
import json
import os
warnings.filterwarnings('ignore')
#Set the output limit to inf
#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)


# %%
import sys
script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
# Change the current working directory to the script's directory
os.chdir(script_dir)
CONFIG_FILE = 'config_mmlu.yaml'

# %%
########################################
#Functions for the evaluation of the LLM
########################################

def load_config(config_paht):
    """Loads the LLM model configuration from the provided path.

    Args:
        config_path: The path to the LLM model configuration file.

    Returns:
        The LLM model configuration.
    """
    with open(config_paht, 'r') as f:
        
        config = yaml.safe_load(f)
    return config


def extract_answer_ol(answer):
    """Extracts the correct answers from the provided answer string.

    Args:
        answer: The answer string to extract the correct answers from.

    Returns:
        A list of correct answers (e.g., ['A', 'B']) if found, otherwise None. 
    """
    #print(repr(answer))
    answer = re.sub(r'[\s\n.,]', '', answer)
    pattern = re.compile(r'^[A-Z,]*$')
    #print(answer)
    if re.match(pattern, answer):
        if ',' in answer:
            return None
        else:
            return list(answer)
    else:
        return None
    
#TODO test the regex. LLama3 seems to have longer answers sometime: https://github.com/TIGER-AI-Lab/MMLU-Pro/issues/5
def extract_answer(answer):
    # Define the regex patterns
    pattern1 = re.compile(r"answer is \(?([ABCDEFGHIJ])\)?", re.IGNORECASE)
    pattern2 = re.compile(r'.*[aA]nswer:\s*([A-J])', re.IGNORECASE)
    
    # Find matches using the first regex pattern
    match1 = pattern1.findall(answer)
    
    # Find matches using the second regex pattern
    match2 = pattern2.findall(answer)
    
    # Combine results from both patterns
    results = match1 + match2
    
    # Return unique results as a list
    return list(set(results))

    
def compare_answers(answerLLM, answer_exam):
    """Compares the extracted correct answers with the answers in answer_exam.

    Keyword arguments:
    answerLLM -- the list of answers extracted from the LLM answer
    answer_exam -- list of answers from the exam
    """
    # Convert answer_exam_list from letters to numbers
    answerLLM = [ord(answer) - 65 for answer in answerLLM]

    # Get number of correct answers in the exam
    num_of_correct_exam_answers = len(answer_exam)

    # Convert both lists to sets for efficient comparison
    answer_LLM_set = set(answerLLM)
    answer_exam_set = set(answer_exam)

    # Calculate the count of matching answers
    number_of_correct_llm_answers = len(answer_LLM_set.intersection(answer_exam_set))

    #Calculate the number of incorrect answers
    number_of_incorrect_llm_answers = len(answer_LLM_set.difference(answer_exam_set))

    # Check if the number of answers given by the LLM is greater than the number of correct answers
    too_many_answ_given = False
    if len(answer_LLM_set) > num_of_correct_exam_answers:
        too_many_answ_given = True

    # Return a dictionary with the matching count and the number of correct answers
    return number_of_correct_llm_answers, too_many_answ_given, number_of_incorrect_llm_answers

def format_choices_for_llm(choices):
    #Define the letters for the choices
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    
    # Erstellen Sie den formatierten String
    formatted_choices = '\n'.join(f'{letters[i]}. {choice}' for i, choice in enumerate(choices))
    
    return formatted_choices

def evaluation_sampling(llm_answer, exam_Answers, num_of_correct_answer):
    """Analyse the answer given by the LLM and compare it with the exam answers.

    Keyword arguments:
    llm_answer -- the answer string given by the LLM
    exam_Answers -- the list of answers from the exam
    """

    answerLLM = extract_answer(llm_answer)
    if answerLLM is not None:
        num_of_correct_llm_Answers, too_many_answ, number_of_incorrect_llm_answers = compare_answers(answerLLM, exam_Answers)
        if num_of_correct_llm_Answers == num_of_correct_answer and too_many_answ == False:
            answered_correctly = True
        else:
            answered_correctly = False 
        return num_of_correct_llm_Answers, answerLLM, too_many_answ, answered_correctly, number_of_incorrect_llm_answers
    else:
         return -1


def evaluation(llm_output_dataframe):

    # Compute the number of total questions for each model
    number_of_questions = llm_output_dataframe.groupby('Model')['QuestionIndex'].count()
    
    #Number of fully correct answers given by the LLM
    correctly_answered = llm_output_dataframe.groupby('Model')['Answered_Correctly'].sum()

    #Number of incorrect answers given by the LLM
    incorrectly_answered = number_of_questions - correctly_answered

    #Amount of correct answers in the exam
    amount_correct_exam_answers = llm_output_dataframe.groupby('Model')['NumberOfCorrectExamAnswers'].sum()

    #Amount of correct answers given by the LLM even if not fully correct
    amount_correct_llm_answers = llm_output_dataframe.groupby('Model')['NumberOfCorrectLLMAnswers'].sum()
    
    # Calculate Partial Credits
    llm_output_dataframe['Partial_Credit'] = llm_output_dataframe.apply(
        lambda row: max(0, row['NumberOfCorrectLLMAnswers'] / row['NumberOfCorrectExamAnswers'] - 
                        (row['NumberOfIncorrectLLMAnswers'] /row['NumberOfCorrectExamAnswers'])), axis=1)
    
    # Aggregate Partial Credit for each model
    partial_credit_sum = llm_output_dataframe.groupby('Model')['Partial_Credit'].sum()

    #Calculation of Accuracy and Recall and f1 score
    accuracy = correctly_answered / number_of_questions
    accuracy_partial = partial_credit_sum / number_of_questions    
    
    results_df = pd.DataFrame({
        'Number of Questions': number_of_questions,
        'Correctly Answered': correctly_answered,
        'Incorrectly Answered': incorrectly_answered,
        'Accuracy': accuracy,
        'Accuracy Partial': accuracy_partial,
        'Total Partial Credit': partial_credit_sum
    })

    results_df = results_df.reset_index()

    return results_df


def plot_evaluation_CCNA(evaluation_df, hline_accuracy=None, hline_partial=None, title=None):
    """
    Plots evaluation metrics from a DataFrame containing columns:
        - 'Model'
        - 'Accuracy Mean', 'Accuracy Min', 'Accuracy Max'
        - 'Accuracy Partial Mean', 'Accuracy Partial Min', 'Accuracy Partial Max'
    """

    # Define a list of colors for the models
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    # Define bar width
    bar_width = 0.5  # Increase bar width for thicker bars

    # --- Subplot 1: Accuracy ---
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    for i, model in enumerate(evaluation_df['Model']):
        bars = axs[0].bar(i + bar_width * i, evaluation_df.loc[i, 'Accuracy Mean'], bar_width, 
                   yerr=[[abs(evaluation_df.loc[i, 'Accuracy Mean'] - evaluation_df.loc[i, 'Accuracy Min'])], [abs(evaluation_df.loc[i, 'Accuracy Max'] - evaluation_df.loc[i, 'Accuracy Mean'])]],
                   label=model, color=colors[i % len(colors)], capsize=5)

    axs[0].set_ylabel('Accuracy (%)')
    axs[0].set_title('Accuracy Mean with Error Bars (Max and Min)', fontsize=12)
    axs[0].set_xticks([i + bar_width * i for i in range(len(evaluation_df['Model']))])
    axs[0].set_xticklabels(evaluation_df['Model'], rotation=45, ha='right', fontsize=10)
    axs[0].legend()
    axs[0].set_ylim([0, 1])
    axs[0].yaxis.set_major_locator(mtick.MultipleLocator(0.1))
    axs[0].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    axs[0].grid(True, linestyle='dotted', axis='y')

    # Add horizontal line to Accuracy subplot
    if hline_accuracy is not None:
        axs[0].axhline(y=hline_accuracy, color='r', linestyle='--')

    # --- Subplot 2: Partial Accuracy ---
    for i, model in enumerate(evaluation_df['Model']):
        bars = axs[1].bar(i + bar_width * i, evaluation_df.loc[i, 'Accuracy Partial Mean'], bar_width,
                   yerr=[[abs(evaluation_df.loc[i, 'Accuracy Partial Mean'] - evaluation_df.loc[i, 'Accuracy Partial Min'])], [abs(evaluation_df.loc[i, 'Accuracy Partial Max'] - evaluation_df.loc[i, 'Accuracy Partial Mean'])]],
                   label=model, color=colors[i % len(colors)], capsize=5)

    axs[1].set_ylabel('Accuracy Partial (%)')
    axs[1].set_title('Accuracy Partial Mean with Error Bars (Max and Min)', fontsize=12)
    axs[1].set_xticks([i + bar_width * i for i in range(len(evaluation_df['Model']))])
    axs[1].set_xticklabels(evaluation_df['Model'], rotation=45, ha='right', fontsize=10)
    axs[1].legend()
    axs[1].set_ylim([0, 1])
    axs[1].yaxis.set_major_locator(mtick.MultipleLocator(0.1))
    axs[1].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    axs[1].grid(True, linestyle='dotted', axis='y')

    # Add horizontal line to Partial Accuracy subplot
    if hline_partial is not None:
        axs[1].axhline(y=hline_partial, color='r', linestyle='--')

    fig.tight_layout(pad=1.2)  # Decrease padding for closer plots

    # Add title to the figure
    if title is not None:
        fig.suptitle(title, fontsize=16, y=1.05)

    plt.show()
    fig.savefig(f"{OUTPUT_PATH}llm_5_Shot_{DATASET_NAME}.png")

def calculate_model_statistics(df):
    """
    Calculates statistics for each model in the DataFrame.
    
    Args:
    df (DataFrame): Input DataFrame containing evaluation metrics for different models.
    
    Returns:
    DataFrame: New DataFrame containing calculated statistics for each model.
    """
    model_stats = []
    for model, group_df in df.groupby('Model'):
        model_stat = {
            'Model': model,
            'Accuracy Mean': group_df['Accuracy'].mean(),
            'Accuracy Max': group_df['Accuracy'].max(),
            'Accuracy Min': group_df['Accuracy'].min(),
            'Accuracy STD': group_df['Accuracy'].std(),
            'Accuracy Partial Mean': group_df['Accuracy Partial'].mean(),
            'Accuracy Partial Max': group_df['Accuracy Partial'].max(),
            'Accuracy Partial Min': group_df['Accuracy Partial'].min(),
            'Accuracy Partial STD': group_df['Accuracy Partial'].std()
        }
        model_stats.append(model_stat)
    
    return pd.DataFrame(model_stats)


def shuffle_choices_and_update_answer(choices, answer):
    # Erstellen Sie eine Liste von Indizes und mischen Sie sie
    indices = list(range(len(choices)))
    random.shuffle(indices)
    shuffled_choices = [choices[i] for i in indices]
    updated_answer = [indices.index(a) for a in answer]  
    
    return shuffled_choices, updated_answer

def plot_evaluation_MMLU(llm_result_df, helm_result, df1_name, df2_name, title=None, probability=0.25):
    """
    Plots evaluation metrics from two DataFrames containing columns:
        - 'Model'
        - 'Accuracy'
    """

    # Define colors for the models
    color_llm_result = 'b'
    color_helm_result = 'orange'

    # Define bar width and gap
    bar_width = 0.2  # Decrease bar width for side-by-side bars with a gap
    gap = 0.05  # Define gap between bars

    #Merge the two DataFrames, so that the results can be compared (Official HELM Results vs LLM Results)
    llm_result_df = pd.merge(llm_result_df, helm_result, on='Model', suffixes=('_LLM', '_HELM'))
    llm_result_df = llm_result_df.rename(columns={'Accuracy': 'Accuracy_HELM', 'Accuracy Mean': 'Accuracy_Mean_LLM'})

    print(llm_result_df)

    # Just one plot
    fig, ax = plt.subplots(figsize=(14, 6))

    for i, model in enumerate(llm_result_df['Model']):
        bars_llm = ax.bar(i - bar_width - gap / 2, llm_result_df.loc[i, 'Accuracy_Mean_LLM'], bar_width, color=color_llm_result)
        bars_helm = ax.bar(i + gap / 2, llm_result_df.loc[i, 'Accuracy_HELM'], bar_width, color=color_helm_result)

    ax.set_ylabel('Accuracy (%)')
    ax.set_title('Accuracy Mean LLM vs. HELM', fontsize=12)
    ax.set_xticks([i for i in range(len(llm_result_df['Model']))])
    ax.set_xticklabels(llm_result_df['Model'], rotation=45, ha='right', fontsize=10)
    ax.legend([bars_llm, bars_helm], [df1_name, df2_name])
    ax.set_ylim([0, 1])
    ax.yaxis.set_major_locator(mtick.MultipleLocator(0.1))
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.grid(True, linestyle='dotted', axis='y')

    # Add horizontal line to Accuracy subplot
    ax.axhline(y=probability, color='r', linestyle='--')

    # Add title to the figure
    if title is not None:
        fig.suptitle(title, fontsize=16, y=1.05)

    plt.show()

# %%
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
HELM_RESULT = pd.read_pickle(config['helm_result'])
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

# %%
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
    

# %%
from langchain_openai import ChatOpenAI
###########################################
#Main programm for the evaluation of the LLM
###########################################

valid_question_answer = False  
#Create a dataframe with the size of NUM_OF_SHUFFLES which contains the dataframe llm_exam_result
shuffled_evalutation_df = pd.DataFrame(columns=[ 'Number of Questions','Correctly Answered','Incorrectly Answered','Accuracy','Accuracy Partial'])

#Read the questions from the questionsbank
questions  = pd.read_parquet(QUESTIONS_BANK)

#Randomly take NUMBER_OF_QUESTIONS (default 120)
try:
    questions = questions.sample(n=NUMBER_OF_QUESTIONS)
except:
    print("Number of questions is greater than the number of questions in the questionbank. Max Number taken")

#questions = extract_answer_from_text_file("../data/questionbank_cisco_CCNP.txt")
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
prompt_template = PromptTemplate.from_template(PROMPT_TEMPLATE)

#Iterate over each model definied in the MODEL_PATH dictionary
for model, model_path in MODEL_PATH.items():
     #Load the model wiht LLamaCpp
    print("Load Model ...")
    if "ollama" in model_path:
        model_name = model_path.split("ollama:")[1]
        llm = ChatOpenAI(
            model=model_name,
            temperature=TEMPERATURE,
            max_tokens=MAX_OUTPUT_TOKENS,
            timeout=None,
            max_retries=2,
            api_key="ollama",
            base_url='http://localhost:11434/v1',
            # organization="...",
            # other params...
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

    print("Model loaded")
    chain = prompt_template | llm
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
            #TODO why so difficult?
            num_of_choices = choices.count('\n') + 1
            #Only if shuffle is enabled, shuffle the choices
            if shuffled_iteration > 0:
                choices, answers = shuffle_choices_and_update_answer(row['choices'], row['answer'])
                #TODO does the amount of answers change?
                #num_of_correct_answer = len(answers)
                choices = format_choices_for_llm(choices)
            #Empty the char_probabilities dictionary for each question
            char_probabilities = {}
            #TODO forgot to reset valid_question_answer to False
            valid_question_answer = False
            #Iterate over the maximum sampling rate
            for index_sampling in range(MAX_SAMPLING_RATE):
                # Invoke the chain with the question and choices              
                llm_answer = chain.invoke({"Exam_Question" : row['question'], "Exam_Choices" : choices})  
                #get the prompt
                print(prompt_template.format(Exam_Question=row['question'],Exam_Choices=choices))
                #for the openAI format, the content needs to be extracted
                if "ollama" in model_path:
                    llm_answer = llm_answer.content
                # Check if the answer is in the expected format
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


# %%
import os

###########################################################
#Evaluation of the results and calculation of the statistics
###########################################################
for model, model_path in MODEL_PATH.items():
    print(f"Model: {model}")
    for shuffled_iteration in range(NUM_OF_SHUFFLES):
        # Get the correct output path based on the updated date
        for folder in os.listdir("../results"):
            base_folder = os.path.basename(OUTPUT_PATH[:-1])
            if os.path.isdir(os.path.join("../results", folder)) and folder.startswith(base_folder[:-20]):
                OUTPUT_PATH_CORRECT_DATE = os.path.join("../results", folder)
                break
        pickle_path = os.path.join(OUTPUT_PATH_CORRECT_DATE, f"{NUMBER_OF_QUESTIONS}_questions_{DATASET_NAME}_{model}_shuffled_{shuffled_iteration}.pkl")
        llm_exam_result = pd.read_pickle(pickle_path)
        evaluation_df = evaluation(llm_exam_result)
        #Concat the evaluation dataframe to the complete dataframe
        shuffled_evalutation_df = pd.concat([shuffled_evalutation_df, evaluation_df], ignore_index=True)
model_statistics = calculate_model_statistics(shuffled_evalutation_df)
print(model_statistics)
#shuffled_evalutation_df.to_pickle(OUTPUT_EVALUATION_DETAILED)
#model_statistics.to_pickle(OUTPUT_EVALUATION)
if "mmlu" in DATASET_NAME:
    plot_evaluation_MMLU(model_statistics, HELM_RESULT, "Own Approach", "HELM", title="Own Approach vs. HELM Official")
else:
    plot_evaluation_CCNA(model_statistics, hline_accuracy=0.8, hline_partial=0.8, title=DATASET_NAME)


