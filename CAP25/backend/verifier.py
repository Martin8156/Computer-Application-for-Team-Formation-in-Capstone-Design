import pandas as pd
import os
import json

CONFIG_FILE = "config.json"

with open(CONFIG_FILE) as f:
    config = json.load(f)
    STU_MAP = config["student_mapping"]
    COM_MAP = config["company_mapping"]

STU_MAP = {int(k): v for k, v in STU_MAP.items()}
COM_MAP = {int(k): v for k, v in COM_MAP.items()}

def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return f"Invalid path: {file_path}"

def check_company_required_columms(company_csv):
    errors = []
    required_columns = ['Project_ID', 'Company', 'Project_Title']
    for column in required_columns:
        if column not in company_csv.columns:
            errors.append(f"Missing required column: {column}")
    
    if 'Project_ID' in company_csv.columns:
        for i, val in enumerate(company_csv['Project_ID']):
            if val is None or val == '':
                errors.append(f"Project_ID cannot be empty at row {i}")

    if 'Company' in company_csv.columns:
        for i, val in enumerate(company_csv['Company']):
            if val is None or val == '':
                errors.append(f"Company cannot be empty at row {i}")

    if 'Project_Title' in company_csv.columns:
        for i, val in enumerate(company_csv['Project_Title']):
            if val is None or val == '':
                errors.append(f"Project_Title cannot be empty at row {i}")
    if errors:
        return ",".join(errors)

def check_student_required_columms(student_csv):
    errors = []
    required_columns = ['EID', 'Name']
    for column in required_columns:
        if column not in student_csv.columns:
            errors.append(f"Missing required column: {column}")
    if errors:
        return ",".join(errors)

def check_shape(company_df, student_df):
    errors = []
    # Drop non-skill columns from copies to avoid modifying the original DataFrames
    # company_df_copy = company_df.copy()
    # student_df_copy = student_df.copy()
    
    for col in ['Project_ID', 'Company', 'Project_Title']:
        if col in company_df.columns:
            company_df.drop(col, axis=1, inplace=True)
    for col in ['EID', 'Name']:
        if col in student_df.columns:
            student_df.drop(col, axis=1, inplace=True)
    
    if company_df.shape[1] != student_df.shape[1]:
        errors.append("The number of skills in the company and student files do not match")
    if errors:
        return ",".join(errors)

def check_skills(company_df, student_df):
    errors = []
    company_skills = list(company_df.columns)
    student_skills = list(student_df.columns)
    
    if company_skills != student_skills:
        errors.append("The skills in the company file and student file do not match")
    
    # Check company values with position details.
    # for col in company_skills:
    #     for idx, val in company_df[col].items():
    #         # Check numeric type
    #         if type(val) != int:
    #             errors.append(f"Error: Company - value {val} at row index {idx} in column '{col}' must be numeric")
    #         # Check value range
    #         elif val < 1 or val > 5:
    #             errors.append(f"Error: Company - value {val} at row index {idx} in column '{col}' must be between 1 and 5")
    
    # # Check student values with position details.
    # for col in student_skills:
    #     for idx, val in student_df[col].items():
    #         if type(val) != int:
    #             errors.append(f"Error: Student - value {val} at row index {idx} in column '{col}' must be numeric")
    #         elif val < 1 or val > 5:
    #             errors.append(f"Error: Student - value {val} at row index {idx} in column '{col}' must be between 1 and 5")
    # Check company values with position details.
    for col in company_skills:
        for idx, val in company_df[col].items():
            try:
                numeric_val = int(val)                    
                if numeric_val not in COM_MAP.keys():
                    errors.append(f"Error: Company - value {val} at row index {idx} in column '{col}' must be between 1 and 5")
            except Exception:
                errors.append(f"Error: Company - value {val} at row index {idx} in column '{col}' is not numeric")
    
    # Check student values with position details.
    for col in student_skills:
        for idx, val in student_df[col].items():
            try:
                numeric_val = int(val)
                if numeric_val not in STU_MAP.keys():
                    errors.append(f"Error: Student - value {val} at row index {idx} in column '{col}' must be between 1 and 5")
            except Exception:
                errors.append(f"Error: Student - value {val} at row index {idx} in column '{col}' is not numeric")
    
    if errors:
        return ",".join(errors)

def verifier(company_csv, student_csv):
    errors = []
    
    company_df = load_csv(company_csv)
    student_df = load_csv(student_csv)
    
    if isinstance(company_df, str):
        errors.append(company_df)
    if isinstance(student_df, str):
        errors.append(student_df)
    
    if errors:
        return ",".join(errors)
    
    errors.append(check_company_required_columms(company_df))
    errors.append(check_student_required_columms(student_df))
    errors.append(check_shape(company_df, student_df))
    errors.append(check_skills(company_df, student_df))
    
    #return ",".join(filter(None, errors)) if errors else "Success"
    errors = list(filter(None, errors))
    if errors:
        return ",".join(errors)
    else:
        return "Success"

# if __name__ == "__main__":
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     FILES_DIR = os.path.join(BASE_DIR, "example_file")
    
#     company_csv_path = os.path.join(FILES_DIR, "Company.csv")
#     student_csv_path = os.path.join(FILES_DIR, "Student.csv")
    
#     result = verifier(company_csv_path, student_csv_path)
#     print(result)