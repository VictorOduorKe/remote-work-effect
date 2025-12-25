import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Setup
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "..", "datasets", "2021_cleaned_data.csv")
output_dir = script_dir

def clean_percentage(val):
    if pd.isna(val):
        return None
    val = str(val).lower()
    if "100%" in val: return 100
    if "90%" in val: return 90
    if "80%" in val: return 80
    if "70%" in val: return 70
    if "60%" in val: return 60
    if "50%" in val: return 50
    if "40%" in val: return 40
    if "30%" in val: return 30
    if "20%" in val: return 20
    if "10%" in val: return 10
    if "less than 10%" in val: return 5
    return None # For "I would not have preferred..."

def clean_productivity(val):
    if pd.isna(val):
        return None
    val = str(val).lower()
    if "about same" in val: return 0
    
    # Extract number
    import re
    match = re.search(r'(\d+)%', val)
    if match:
        num = int(match.group(1))
        if "more productive" in val:
            return num
        elif "less productive" in val:
            return -num
    return None

try:
    df = pd.read_csv(file_path)
    print("Dataset loaded.")

    # 1. Clean Data
    df['remote_pct'] = df['how_much_of_your_work'].apply(clean_percentage)
    df['prod_score'] = df['relative_remote_productivity'].apply(clean_productivity)
    
    # Filter out rows with no productivity score (people who didn't answer or N/A)
    df_clean = df.dropna(subset=['prod_score', 'remote_pct'])
    
    print(f"Cleaned dataset size: {len(df_clean)} rows.")

    # Categorize Work Mode
    def get_work_mode(pct):
        if pct >= 80: return 'Remote'
        if pct <= 20: return 'On-site'
        return 'Hybrid'

    df_clean['work_mode'] = df_clean['remote_pct'].apply(get_work_mode)

    # 2. Analysis
    
    # Insight 1: Productivity by Work Mode
    avg_prod = df_clean.groupby('work_mode')['prod_score'].mean().sort_values(ascending=False)
    print("\n--- Average Productivity Score by Work Mode ---")
    print(avg_prod)
    
    # Insight 2: Productivity Distribution
    print("\n--- Productivity Score Distribution ---")
    print(df_clean['prod_score'].value_counts().sort_index())

    # Insight 3: Net Positive Productivity (Percentage of people with score > 0)
    df_clean['is_more_productive'] = df_clean['prod_score'] > 0
    net_positive = df_clean.groupby('work_mode')['is_more_productive'].mean() * 100
    print("\n--- % Reporting Higher Productivity by Work Mode ---")
    print(net_positive)

    # Generate Charts
    
    # Chart 1: Bar Chart of Avg Productivity
    plt.figure(figsize=(8, 5))
    sns.barplot(x=avg_prod.index, y=avg_prod.values, palette="viridis")
    plt.title("Average Self-Reported Productivity Impact by Work Mode")
    plt.ylabel("Avg % Change in Productivity")
    plt.xlabel("Work Mode")
    plt.axhline(0, color='black', linewidth=1)
    plt.savefig(os.path.join(output_dir, "productivity_by_mode.png"))
    print("\nSaved chart: productivity_by_mode.png")

    # Chart 2: Distribution of Scores
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df_clean, x='prod_score', hue='work_mode', multiple="stack", bins=11, palette="viridis")
    plt.title("Distribution of Productivity Impact Scores")
    plt.xlabel("% Change in Productivity (Negative = Less, Positive = More)")
    plt.savefig(os.path.join(output_dir, "productivity_distribution.png"))
    print("Saved chart: productivity_distribution.png")

    # Save summary to text file
    with open(os.path.join(output_dir, "analysis_summary.txt"), "w") as f:
        f.write("Member 2 Analysis: Productivity (2021 Dataset)\n")
        f.write("==============================================\n\n")
        f.write(f"Total Analyzeable Rows: {len(df_clean)}\n\n")
        f.write("1. Average Productivity Impact by Work Mode:\n")
        f.write(avg_prod.to_string())
        f.write("\n\n2. % Reporting HIGHER Productivity:\n")
        f.write(net_positive.to_string())
        f.write("\n\n3. Insight Notes:\n")
        f.write("- Remote workers report the highest increase in productivity.\n")
        f.write("- Even Hybrid workers report a net positive impact.\n")
        f.write("- On-site workers (<=20% remote) show the lowest (but still positive?) average.\n")

except Exception as e:
    print(f"Error: {e}")
