# To generate cleaned files
```bash
git clone https://github.com/VictorOduorKe/remote-work-effect.git
cd remote work-effect

# ubuntu user
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 clean_data.py

#windows user
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python clean_data.py
```
Two files with cleaned data(2020_cleaned_data.csv,2021_cleaned_data.csv) will be generated in the same directory

# These are the instructions incase you dont understand what field name represents

1. All field name have been renamed to short terms:
 ``` bash 
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
        ```
