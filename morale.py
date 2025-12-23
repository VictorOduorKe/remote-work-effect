import pandas as pd
import matplotlib.pyplot as plt
import os

# =============================
# 0. OUTPUT DIRECTORY
# =============================
OUTPUT_DIR = "charts_2020"
os.makedirs(OUTPUT_DIR, exist_ok=True)
# =============================
# 1. LOAD & PREP DATA
# =============================
def get_dataframe():
    df = pd.read_csv("datasets/2020_cleaned_data.csv")
    df.columns = df.columns.str.strip().str.lower()
    
    # Ensure required columns exist and are numeric where possible
    numeric_cols = ["org_encouraged", "org_prepared", "family_time", "caring_time", "commute_time", "age"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    df = df.dropna(subset=["time_ly", "org_encouraged", "org_prepared"])
    
    # FEATURE ENGINEERING
    def classify_work_mode(value):
        value = str(value).lower()
        if "less than" in value or "10%" in value or "rarely" in value:
            return "Mostly onsite"
        if "half" in value or "50%" in value:
            return "Hybrid"
        return "Mostly remote"

    df["work_mode"] = df["time_ly"].apply(classify_work_mode)

    # Use pre-cleaned Likert scores
    df["morale_score"] = (df["org_encouraged"] + df["org_prepared"]) / 2
    
    df["total_care_load"] = df["family_time"] + df["caring_time"]
    df["burnout_risk"] = df["total_care_load"] / (
        df["total_care_load"] + df["commute_time"] + 1
    )
    
    df["engagement_score"] = df["morale_score"]
    
    return df

df = get_dataframe()

# =============================
# 2. INSIGHT 1: MORALE BY WORK MODE
# =============================
morale_by_mode = df.groupby("work_mode")["morale_score"].mean()

plt.figure()
morale_by_mode.plot(kind="bar")
plt.title("Average Morale by Work Mode (2020)")
plt.xlabel("Work Mode")
plt.ylabel("Average Morale Score")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/morale_by_work_mode.png", dpi=300)
plt.close()

# =============================
# 3. INSIGHT 2: ORG SUPPORT → JOB SATISFACTION
# =============================
support_vs_morale = df.groupby("org_prepared")["morale_score"].mean()

plt.figure()
support_vs_morale.plot(marker="o")
plt.title("Organisational Preparedness vs Job Satisfaction (2020)")
plt.xlabel("Org Preparedness Score")
plt.ylabel("Average Morale Score")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/org_preparedness_vs_morale.png", dpi=300)
plt.close()

# =============================
# 4. INSIGHT 3: STRESS & BURNOUT RISK
# =============================
plt.figure()
plt.scatter(df["total_care_load"], df["age"], c=df["burnout_risk"], cmap='viridis')
plt.title("Care Load vs Age (Burnout Risk Color)")
plt.xlabel("Family + Caring Time (hours)")
plt.ylabel("Age")
plt.colorbar(label='Burnout Risk')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/care_load_vs_age.png", dpi=300)
plt.close()

# =============================
# 5. INSIGHT 4: ENGAGEMENT TRADE-OFF
# =============================
engagement_by_mode = df.groupby("work_mode")["engagement_score"].mean()

plt.figure()
engagement_by_mode.plot(kind="bar")
plt.title("Employee Engagement by Work Mode (2020)")
plt.xlabel("Work Mode")
plt.ylabel("Engagement Score")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/engagement_by_work_mode.png", dpi=300)
plt.close()

# =============================
# 6. SUMMARY TABLE
# =============================
def get_summary():
    summary = df.groupby("work_mode").agg({
        "morale_score": "mean",
        "engagement_score": "mean",
        "burnout_risk": "mean",
        "total_care_load": "mean"
    }).round(2)
    return summary
