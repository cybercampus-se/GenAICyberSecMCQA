import pandas as pd
import re
import pyarrow.parquet as pq
import pyarrow as pa

# Function to convert choice format
def convert_choice_format(choices):
    if pd.isna(choices):  # Handle NaN values
        return []
    choice_map = {
        'B': 1,
        'A': 0,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5,
        'G': 6
    }
    return [choice_map.get(choice, "") for choice in str(choices) if choice in choice_map]
import ast
# Function to ensure each entry is a list containing one string
def wrap_in_list(entry):
    if pd.isna(entry):  # Handle NaN values
        return []
    return ast.literal_eval(entry)

# Read CSV file
csv_file = 'data/extracted_questions_answers_350_701.csv'
df = pd.read_csv(csv_file)

# Remove rows where choices is '[]'
df = df[df['Answers'] != '[]']

# Create new columns with required names and formats
df['question'] = df['Question']
df['choices'] = df['Answers'].apply(wrap_in_list)
df['answer'] = df['Correct Answer'].apply(convert_choice_format)
df['image'] = df['Image'].astype(str)
df['Exam'] = 'CCNP-350-701'

# Remove rows where choices is '[]'
df = df[df['choices'] != '[]']

# Select required columns for the parquet file
df_parquet = df[['question', 'choices', 'answer', 'image', 'Exam']]

# Save to parquet file
parquet_file_path = 'data/350-701-CCNP.parquet'
table = pa.Table.from_pandas(df_parquet)
pq.write_table(table, parquet_file_path)

print(f"Parquet file {parquet_file_path} created successfully.")