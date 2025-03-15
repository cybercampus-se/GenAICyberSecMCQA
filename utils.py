import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import random
import yaml

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


def extract_answer(answer):
    """Extracts the correct answers from the provided answer string.

    Args:
        answer: The answer string to extract the correct answers from.

    Returns:
        A list of correct answers. 
    """

    # Cleaning the input by removing the reasoning part.
    answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()

    # Cleaning the input by removing some non-relevant characters
    answer_proc = re.sub(r'[\s\n.,]', '', answer)

    # TODO fix AND. There are issues with answers containing 'and'
    # TODO R1s infinite loops.

    # Define regex patterns for different cases
    pattern_single_letters = re.compile(r'^[A-J]+$')
    #pattern1 = re.compile(r"answer is \(?([A-J]+)\)?", re.IGNORECASE)
    pattern1 = re.compile(r"answer is \[?\**([A-J]+)\]?", re.IGNORECASE)
    pattern2 = re.compile(r'.*[aA]nswer:\s*\**([A-J]+)', re.IGNORECASE)
    
    if re.match(pattern_single_letters, answer_proc):
        return list(answer_proc)
    else:
        # Find matches using the first regex pattern
        #drop , from answer

        match1 = pattern1.findall(answer)
        
        # Find matches using the second regex pattern
        match2 = pattern2.findall(answer)
        
        # Combine results from both patterns
        results = match1 + match2
        
        # Flatten the list and remove duplicates
        combined_results = []
        for result in results:
            combined_results.extend(list(result))
        
        return list(set(combined_results))
    
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


def shuffle_choices_and_update_answer(choices, answer, seed):
    # Erstellen Sie eine Liste von Indizes und mischen Sie sie
    indices = list(range(len(choices)))
    random.Random(seed).shuffle(indices)
    shuffled_choices = [choices[i] for i in indices]
    updated_answer = [indices.index(a) for a in answer]  
    
    return shuffled_choices, updated_answer

if __name__ == "__main__":
    print(extract_answer("The answer is ABCDE."))
    print(extract_answer("The best answer is C, E."))
    print(extract_answer("The best answer is [DE]. The access and distribution layers must be on the same device"))
    print(shuffle_choices_and_update_answer(["0","1","2","3","5"],[1],1))
    print(shuffle_choices_and_update_answer(["0","1","2","3","5"],[1],2))
    print(shuffle_choices_and_update_answer(["0","1","2","3","5"],[1],3))
    print(shuffle_choices_and_update_answer(["0","1","2","3","5"],[1],4))