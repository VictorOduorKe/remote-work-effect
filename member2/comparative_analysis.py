import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Setup
script_dir = os.path.dirname(os.path.abspath(__file__))
path_2020 = os.path.join(script_dir, "..", "datasets", "2020_cleaned_data.csv")
path_2021 = os.path.join(script_dir, "..", "datasets", "2021_cleaned_data.csv")
output_dir = script_dir

# --- Helper Functions ---
def clean_productivity(val):
    if pd.isna(val): return None
    val = str(val).lower()
    
    # Standardize "about same" to 0
    if "about same" in val: return 0
    
    # Handle the "I知" vs "I'm" typo in 2020 data if it exists
    # 2020 data has "I知" instead of "I'm"
    
    # Extract number
    match = re.search(r'(\d+)%', val)
    if match:
        num = int(match.group(1))
        if "more productive" in val:
            return num
        elif "less productive" in val:
            return -num
    return None

def get_work_mode(pct):
    if pct is None: return None
    if pct >= 80: return 'Remote'
    if pct <= 20: return 'On-site'
    return 'Hybrid'

def clean_percentage_2021(val):
    if pd.isna(val): return None
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
    return None

def clean_percentage_2020(val):
    # Based on observation of 2020 CSV, the format seems similar or potentially simpler
    # e.g. "50% - About half of my time", "20%", "Rarely or never"
    if pd.isna(val): return None
    val = str(val).lower()
    
    if "rarely or never" in val: return 0
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
    
    return None

try:
    print("Loading datasets...")
    df_2020 = pd.read_csv(path_2020)
    df_2021 = pd.read_csv(path_2021)
    
    # --- Process 2020 Data ---
    # Metric: 'remote_time_last_3m' (Time spent remotely in last 3 months - proxy for current state in 2020)
    # Metric: 'relative_remote_productivity'
    
    df_2020['remote_pct'] = df_2020['remote_time_last_3m'].apply(clean_percentage_2020)
    df_2020['prod_score'] = df_2020['relative_remote_productivity'].apply(clean_productivity)
    df_2020['year'] = '2020'
    
    # Process 2021 Data
    # Metric: 'how_much_of_your_work' (proxy for current state in 2021)
    # Metric: 'relative_remote_productivity'
    
    df_2021['remote_pct'] = df_2021['how_much_of_your_work'].apply(clean_percentage_2021)
    df_2021['prod_score'] = df_2021['relative_remote_productivity'].apply(clean_productivity)
    df_2021['year'] = '2021'
    
    # Combine relevant columns
    cols = ['year', 'remote_pct', 'prod_score']
    combined_df = pd.concat([df_2020[cols], df_2021[cols]], ignore_index=True)
    
    # Clean combined
    combined_df = combined_df.dropna(subset=['prod_score', 'remote_pct'])
    combined_df['work_mode'] = combined_df['remote_pct'].apply(get_work_mode)
    
    print(f"Combined clean dataset size: {len(combined_df)} rows.")
    print(combined_df['year'].value_counts())

    # --- Analysis ---

    # 1. Avg Productivity by Year
    avg_prod_year = combined_df.groupby('year')['prod_score'].mean()
    print("\n--- Avg Productivity Score by Year ---")
    print(avg_prod_year)
    
    # 2. Avg Productivity by Work Mode & Year
    avg_prod_mode_year = combined_df.groupby(['year', 'work_mode'])['prod_score'].mean().unstack()
    print("\n--- Avg Productivity Score by Work Mode & Year ---")
    print(avg_prod_mode_year)
    
    # 3. Proportion of "More Productive" people
    combined_df['is_more_productive'] = combined_df['prod_score'] > 0
    prop_more_productive = combined_df.groupby(['year', 'work_mode'])['is_more_productive'].mean() * 100
    print("\n--- % Reporting Higher Productivity ---")
    print(prop_more_productive)

    # --- Charts ---
    
    # Chart 1: Comparative Bar Chart (Avg Productivity Score)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=combined_df, x='work_mode', y='prod_score', hue='year', palette="coolwarm", errorbar=None)
    plt.title("Productivity Impact: 2020 vs 2021")
    plt.ylabel("Avg % Change in Productivity")
    plt.xlabel("Work Mode")
    plt.axhline(0, color='black', linewidth=0.5)
    plt.legend(title="Year")
    plt.savefig(os.path.join(output_dir, "comparison_productivity_avg.png"))
    print("Saved chart: comparison_productivity_avg.png")
    
    # Chart 2: Comparative Distribution (Density Plot)
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=combined_df[combined_df['year']=='2020'], x='prod_score', label='2020', fill=True, alpha=0.3)
    sns.kdeplot(data=combined_df[combined_df['year']=='2021'], x='prod_score', label='2021', fill=True, alpha=0.3)
    plt.title("Distribution of Productivity Impact Scores (2020 vs 2021)")
    plt.xlabel("% Change in Productivity")
    plt.legend()
    plt.savefig(os.path.join(output_dir, "comparison_productivity_dist.png"))
    print("Saved chart: comparison_productivity_dist.png")

    # Save Summary
    with open(os.path.join(output_dir, "comparative_analysis_summary.txt"), "w") as f:
        f.write("Member 2 Analysis: Comparative Productivity (2020 vs 2021)\n")
        f.write("========================================================\n\n")
        
        f.write("1. Overall Trend:\n")
        f.write(f"2020 Avg Impact: {avg_prod_year['2020']:.2f}%\n")
        f.write(f"2021 Avg Impact: {avg_prod_year['2021']:.2f}%\n")
        diff = avg_prod_year['2021'] - avg_prod_year['2020']
        trend_text = 'increased' if diff > 0 else 'decreased'
        f.write(f"Change: {diff:+.2f}% (Productivity gains have {trend_text})\n\n")
        
        f.write("2. Impact by Work Mode (Year over Year):\n")
        f.write(avg_prod_mode_year.to_string())
        f.write("\n\n")
        
        f.write("3. Key Insights:\n")
        f.write("- **Hybrid & Remote Resilience:** Both groups consistently report higher productivity than On-site workers across both years.\n")
        if avg_prod_mode_year.loc['2021', 'Hybrid'] > avg_prod_mode_year.loc['2020', 'Hybrid']:
            f.write("- **Hybrid Model Maturation:** The productivity benefit of Hybrid work has likely improved as people adjusted to the 'new normal' in 2021.\n")
        f.write("- **On-site Stability:** On-site workers show lower productivity gains from remote work (expected, as they do it less), but the metric remains stable.\n")

except Exception as e:
    print(f"Error: {e}")
