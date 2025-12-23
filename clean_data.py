import pandas as pd
import numpy as np
import chardet
import os
import re

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

    # 2. Rename Columns
    if "2020" in input_file:
        rename_rules = {
            "response id": "response_id",
            "year were you born": "birth_year",
            "what is your gender": "gender",
            "industry? (detailed)": "industry_detailed",
            "industry": "industry",
            "occupation? (detailed)": "occupation_detailed",
            "occupation": "occupation",
            "employed by your organisation": "org_size",
            "manage people": "is_manager",
            "describe your household": "household_type",
            "long have you been in your current job": "job_tenure",
            "metro / regional": "metro_regional",
            
            # Time & Org - Last Year
            "spend remote working last year": "remote_time_last_year",
            "remote working last year, how strongly do you agree or disagree with the following statements? - my organisation encouraged": "org_encouragement_last_year",
            "remote working last year, how strongly do you agree or disagree with the following statements? - my organisation was well prepared": "org_preparedness_last_year",
            "remote working last year, how strongly do you agree or disagree with the following statements? - it was common": "remote_prevalence_last_year",
            "remote working last year, how strongly do you agree or disagree with the following statements? - it was easy to get permission": "permission_ease_last_year",
            "remote working last year, how strongly do you agree or disagree with the following statements? - i could easily collaborate": "collaboration_ease_last_year",
            "remote working last year, how strongly do you agree or disagree with the following statements? - i would recommend": "remote_recommendation_last_year",
            "preferred to work remotely last year": "preferred_remote_last_year",

            # Time & Org - Last 3 Months
            "spend remote working in the last 3 months": "remote_time_last_3m",
            "remote working in the last 3 months, how strongly do you agree or disagree with the following statements? - my organisation encouraged": "org_encouragement_last_3m",
            "remote working in the last 3 months, how strongly do you agree or disagree with the following statements? - my organisation was well prepared": "org_preparedness_last_3m",
            "remote working in the last 3 months, how strongly do you agree or disagree with the following statements? - it was common": "remote_prevalence_last_3m",
            "remote working in the last 3 months, how strongly do you agree or disagree with the following statements? - it was easy to get permission": "permission_ease_last_3m",
            "remote working in the last 3 months, how strongly do you agree or disagree with the following statements? - i could easily collaborate": "collaboration_ease_last_3m",
            "remote working in the last 3 months, how strongly do you agree or disagree with the following statements? - i would recommend": "remote_recommendation_last_3m",
            "preferred to work remotely in the last 3 months": "preferred_remote_last_3m",

            # Future
            "prefer to work remotely?": "future_preferred_remote_time",
            "employer would encourage more remote working": "future_employer_encouragement_likelihood",
            "employer would make changes to support remote working": "future_employer_support_likelihood",
            "choice about whether i work remotely": "future_location_choice_likelihood",

            # Productivity & Hours
            "productivity when you work remotely": "relative_remote_productivity",
            "employer's workplace, how many hours would you spend doing the following activities? - preparing for work and commuting": "office_commute_hours",
            "employer's workplace, how many hours would you spend doing the following activities? - working": "office_work_hours",
            "employer's workplace, how many hours would you spend doing the following activities? - personal and family time": "office_family_hours",
            "employer's workplace, how many hours would you spend doing the following activities? - caring and domestic responsibilities": "office_domestic_hours",
            "remote work, how many hours would you spend doing the following activities? - preparing for work and commuting": "remote_commute_hours",
            "remote work, how many hours would you spend doing the following activities? - working": "remote_work_hours",
            "remote work, how many hours would you spend doing the following activities? - personal and family time": "remote_family_hours",
            "remote work, how many hours would you spend doing the following activities? - caring and domestic responsibilities": "remote_domestic_hours",
        }
    else:
        # 2021 Rules
        rename_rules = {
            "year were you born": "birth_year",
            "what is your gender": "gender",
            "industry": "industry",
            "occupation": "occupation",
            "employed by your organisation": "org_size_total",
            "manage people": "is_manager",
            "describe your household": "household_type",
            "long have you been in your current job": "job_tenure_length",
            "metro / regional": "location_type",
            "metro_or_regional": "location_type",
            
            # Time spent
            "spend remote working last year": "remote_time_last_year",
            "spend remote working in the last 3 months": "remote_time_last_3_months",
            "preferred to work remotely last year": "preferred_remote_last_year",
            "preferred to work remotely in the last 3 months": "preferred_remote_last_3_months",
            "prefer to work remotely": "preferred_remote_future",
            
            # Org scores
            "encouraged people to work remotely": "org_encouragement_score",
            "well prepared for me to work remotely": "org_preparedness_score",
            "common for people in my organisation": "org_remote_culture_prevalence",
            "easy to get permission": "remote_permission_ease",
            "collaborate with colleagues": "remote_collaboration_ease",
            "recommend remote working": "remote_recommendation_score",
            "employer would encourage": "future_employer_support_likelihood",
            
            # Productivity
            "productivity when you work remotely": "relative_remote_productivity",
            
            # Hours - Workplace
            "employer's workplace, how many hours would you spend doing the following activities? - preparing for work and commuting": "office_day_commute_hours",
            "employer's workplace, how many hours would you spend doing the following activities? - working": "office_day_work_hours",
            "employer's workplace, how many hours would you spend doing the following activities? - personal and family time": "office_day_personal_hours",
            "employer's workplace, how many hours would you spend doing the following activities? - caring and domestic responsibilities": "office_day_caring_hours",
            
            # Hours - Remote
            "remote work, how many hours would you spend doing the following activities? - preparing for work and commuting": "remote_day_commute_hours",
            "remote work, how many hours would you spend doing the following activities? - working": "remote_day_work_hours",
            "remote work, how many hours would you spend doing the following activities? - personal and family time": "remote_day_personal_hours",
            "remote work, how many hours would you spend doing the following activities? - caring and domestic responsibilities": "remote_day_caring_hours",
        }

    descriptive_rules = {
        "most significant barrier": "barrier_most",
        "least significant barrier": "barrier_least",
        "biggest barriers": "barrier_most",
        "smallest barriers": "barrier_least",
        "worst aspect": "worst_remote",
        "best aspect": "best_remote",
        "have the following barriers": "barrier"
    }

    new_columns_list = []
    seen = {}
    for col in df.columns:
        col_lower = col.lower()
        matched_name = None
        
        # 1. Check specific rules first
        for key, new_name in rename_rules.items():
            if key in col_lower:
                matched_name = new_name
                break
        
        # 2. Special handling for 2020 Barriers and Aspects (Complex Regex)
        if not matched_name and "2020" in input_file:
            complex_renames_2020 = [
                (r"most significant barrier.*connectivity.*caring responsibilities", "most_barrier_infra_caring"),
                (r"least significant barrier.*connectivity.*caring responsibilities", "least_barrier_infra_caring"),
                (r"most significant barrier.*connectivity.*lack of motivation", "most_barrier_security_motivation"),
                (r"least significant barrier.*connectivity.*lack of motivation", "least_barrier_security_motivation"),
                (r"most significant barrier.*connectivity.*my workspace", "most_barrier_systems_workspace"),
                (r"least significant barrier.*connectivity.*my workspace", "least_barrier_systems_workspace"),
                (r"most significant barrier.*connectivity.*management discourages", "most_barrier_skills_living"),
                (r"least significant barrier.*connectivity.*management discourages", "least_barrier_skills_living"),
                (r"most significant barrier.*it equipment.*lack of motivation", "most_barrier_collab_motivation"),
                (r"least significant barrier.*it equipment.*lack of motivation", "least_barrier_collab_motivation"),
                
                (r"best aspect.*family.*learning opportunities", "best_aspect_worklife_learning"),
                (r"worst aspect.*family.*learning opportunities", "worst_aspect_worklife_learning"),
                (r"best aspect.*family.*mental wellbeing", "best_aspect_social_wellbeing"),
                (r"worst aspect.*family.*mental wellbeing", "worst_aspect_social_wellbeing"),
                (r"best aspect.*family.*job satisfaction", "best_aspect_expenses_satisfaction"),
                (r"worst aspect.*family.*job satisfaction", "worst_aspect_expenses_satisfaction"),
                (r"best aspect.*hours.*mental wellbeing", "best_aspect_hours_commitments"),
                (r"worst aspect.*hours.*mental wellbeing", "worst_aspect_hours_commitments"),
                (r"best aspect.*hours.*job satisfaction", "best_aspect_personal_relationships"),
                (r"worst aspect.*hours.*job satisfaction", "worst_aspect_personal_relationships"),
            ]
            
            for pattern, name in complex_renames_2020:
                if re.search(pattern, col_lower):
                    matched_name = name
                    break

        
        # Check descriptive rules if no match
        if not matched_name:
            for phrase, prefix in descriptive_rules.items():
                if phrase in col_lower:
                    parts = re.split(r'[\?\:\-]\s+', col_lower)
                    specific_part = parts[-1] if len(parts) > 1 else col_lower.replace(phrase, "")
                    clean_part = re.sub(r'\(.*?\)', '', specific_part).strip()
                    clean_part = ''.join(c if c.isalnum() else '_' for c in clean_part)
                    clean_part = re.sub(r'_+', '_', clean_part).strip('_')
                    words = clean_part.split('_')
                    if len(words) > 4: clean_part = '_'.join(words[:4])
                    if clean_part: matched_name = f"{prefix}_{clean_part}"
                    break

        # Fallback
        if not matched_name:
            clean_name = ''.join(c if c.isalnum() else '_' for c in col_lower).strip('_')
            words = clean_name.split('_')
            matched_name = '_'.join(words[:5]) if len(words) > 5 else clean_name

        # Uniqueness
        final_name = matched_name
        if final_name in seen:
            seen[final_name] += 1
            final_name = f"{final_name}_{seen[final_name]}"
        else:
            seen[final_name] = 0
        new_columns_list.append(final_name)

    df.columns = new_columns_list

    # 3. Cleaning Steps
    df.replace(['NA', 'N/A', 'nan', ' ', 'None'], np.nan, inplace=True)
    
    # Age Calculation
    year_match = re.search(r'(\d{4})', os.path.basename(input_file))
    dataset_year = int(year_match.group(1)) if year_match else 2021
    if 'birth_year' in df.columns:
        df['birth_year'] = pd.to_numeric(df['birth_year'], errors='coerce')
        df['age'] = dataset_year - df['birth_year']

    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(axis=0, how='all', inplace=True)
    df.to_csv(output_file, index=False)
    print(f"Successfully cleaned and saved to {output_file}")

if __name__ == "__main__":
    clean_file("datasets/2021_rws.csv", "datasets/2021_cleaned_data.csv")
    clean_file("datasets/2020_rws.csv", "datasets/2020_cleaned_data.csv")