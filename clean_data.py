import pandas as pd
import numpy as np
import chardet
import os

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(100000))  # Sample first 100KB
    return result['encoding']

def clean_file(input_file, output_file):
    print(f"Processing {input_file}...")
    
    # 1. Detect and Load with correct encoding
    encoding = detect_encoding(input_file)
    print(f"Detected encoding: {encoding}")
    
    try:
        df = pd.read_csv(input_file, encoding=encoding)
    except Exception as e:
        print(f"Failed to load with {encoding}, trying ISO-8859-1. Error: {e}")
        df = pd.read_csv(input_file, encoding='ISO-8859-1')

    # 2. Rename Columns using snake_case rules
    rename_rules = {
        "response id": "id",
        "worst aspect": "worst_aspect",
        "best aspect": "best_aspect",
        "work-life balance": "work_life_balance",
        "number of hours worked": "hours_worked",
        "year were you born": "birth_year",
        "gender": "gender",
        "industry? (detailed)": "ind_detail",
        "industry": "industry",
        "occupation? (detailed)": "occ_detail",
        "occupation": "occupation",
        "manage people": "manages_people",
        "household": "household",
        "employed by your organisation": "org_size",
        "long have you been in your current job": "tenure",
        "metro / regional": "location",
        "metro_or_regional": "location",
        "last quarter of last year": "time_q4_2020",
        "preferred to work remotely during the last quarter": "pref_time_q4_2020",
        "spent working remotely this year": "time_rem_2021",
        "preferred to work remotely so far this year": "pref_time_2021",
        "spend remote working last year": "time_ly",
        "preferred to work remotely last year": "pref_time_ly",
        "remote working in the last 3 months": "time_3m",
        "preferred to work remotely in the last 3 months": "pref_time_3m",
        "encouraged people to work remotely": "org_encouraged",
        "well prepared for me to work remotely": "org_prepared",
        "common for people in my organisation": "org_common",
        "collaborate with colleagues": "collaboration",
        "easy to get permission": "permission",
        "prefer to work remotely": "pref_time_future",
        "encourage more remote working": "org_encourage_future",
        "changes to support remote working": "org_support_future",
        "choice about whether i work remotely": "choice_future",
        "prepare better for remote working": "org_prepared_future",
        "recommend remote working": "recommend",
        "productivity when you work remotely": "productivity",
        "preparing for work and commuting": "commute_time",
        "how many hours would you spend doing the following activities? - working": "work_time",
        "personal and family time": "family_time",
        "caring and domestic responsibilities": "caring_time",
        "other activities": "other_time",
        "most significant barrier": "major_barrier",
        "least significant barrier": "minor_barrier",
        "feel better": "feel_better",
        "more active": "more_active",
        "discretion to offer or deny": "mgmt_discretion",
        "retain employees": "mgmt_retain",
        "recruit employees": "mgmt_recruit",
        "team works well together": "team_collab",
        "easy to manage employees remotely": "mgmt_ease_remote",
        "manage poor performers remotely": "mgmt_poor_performers",
        "manage employees remotely": "mgmt_prepared_remote",
        "more focused on results": "mgmt_focus_results",
        "contact my employees": "mgmt_contact",
        "biggest barriers": "barriers_major",
        "smallest barriers": "barriers_minor",
        "policy_updated_covid": "policy_updated",
        "has_your_employer_changed_or_updated_their_policy": "policy_updated",
        "hybrid_day_usage": "hybrid_usage",
        "worked_part_of_your_day_remotely": "hybrid_usage",
        "policy_required_office": "policy_office_required",
        "policy_office_required": "policy_office_required",
        "policy_suits_me": "policy_suits_me",
        "policy_choice_amount": "policy_choice_amount",
        "policy_choice_days": "policy_choice_days",
        "policy_mgr_discretion": "policy_mgr_discretion",
        "policy_sentiment": "policy_sentiment",
        "promotion_impact": "promotion_impact",
        "breaks_usage": "breaks_usage",
        "impact_on_employer": "impact_on_employer",
        "org_support_who": "org_support_who",
        "pay_cut_interest": "pay_cut_interest",
        "pay_cut_max": "pay_cut_max",
        "barrier_improved_": "barrier_imp_"
    }

    # Rename columns and ensure uniqueness
    new_columns_list = []
    seen = {}
    for col in df.columns:
        col_lower = col.lower()
        matched_name = None
        for key, new_name in rename_rules.items():
            if key.lower() in col_lower:
                matched_name = new_name
                break
        
        if not matched_name:
            # Fallback: simple cleanup of existing header
            clean_name = col_lower.replace('\n', ' ').replace('\r', '').strip()
            # Remove parentheses and their content for brevity
            import re
            clean_name = re.sub(r'\(.*?\)', '', clean_name).strip()
            
            clean_name = ''.join(c if c.isalnum() else '_' for c in clean_name)
            words = [w for w in clean_name.split('_') if w]
            
            # If still long, pick first few words
            if len(words) > 4:
                matched_name = '_'.join(words[:4])
            else:
                matched_name = '_'.join(words)

        # Ensure unique name
        final_name = matched_name
        if final_name in seen:
            seen[final_name] += 1
            final_name = f"{final_name}_{seen[final_name]}"
        else:
            seen[final_name] = 0
        new_columns_list.append(final_name)

    df.columns = new_columns_list

    # 3. Standardize Missing Values
    df.replace(['NA', 'N/A', 'nan', ' '], np.nan, inplace=True)

    # 4. Data Sanitization (Remove non-printable ASCII)
    # Iterate over columns by their index to avoid issues if names were somehow duplicate
    for i in range(len(df.columns)):
        if df.iloc[:, i].dtype == 'object':
            df.iloc[:, i] = df.iloc[:, i].apply(lambda x: str(x).encode('ascii', 'ignore').decode('ascii') if pd.notnull(x) else x)

    # 5. Drop entirely empty rows/cols
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(axis=0, how='all', inplace=True)

    # 6. Save
    df.to_csv(output_file, index=False)
    print(f"Successfully cleaned and saved to {output_file}. Shape: {df.shape}")

if __name__ == "__main__":
    tasks = [
        ("2020_rws.csv", "2020_cleaned_data.csv"),
        ("2021_rws.csv", "2021_cleaned_data.csv")
    ]
    
    for input_f, output_f in tasks:
        if os.path.exists(input_f):
            clean_file(input_f, output_f)
        else:
            print(f"Warning: {input_f} not found.")
