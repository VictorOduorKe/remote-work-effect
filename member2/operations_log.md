# Comprehensive Engineering Operations Log: Member 2 (Productivity Analyst)

**Role:** Member 2 — Productivity Analyst  
**Objective:** Quantify the impact of remote work on employee productivity using 2020 and 2021 datasets.  
**Tech Stack:** Python 3.x, Pandas (Data Manipulation), Matplotlib/Seaborn (Visualization).  
**Work Directory:** `remote-work-effect/member2/`

---

## 1. Environment Setup & Isolation
**Rationale:** To prevent merge conflicts and ensure a clean workspace, all work was isolated in a dedicated subdirectory.
*   **Action:** Created directory `remote-work-effect/member2`.
*   **Dependency Management:** relied on standard data science libraries (`pandas`, `matplotlib`, `seaborn`) already expected in the environment.

---

## 2. Phase I: 2021 Data Analysis (Single Year Baseline)
**Script:** `explore_data.py` (Initial Probe) & `analyze_member2.py` (Core Logic)

### 2.1 Data Exploration
*   **Objective:** Identify the correct columns for "Work Mode" and "Productivity".
*   **Method:** Printed all column names and value counts for potential candidates.
*   **Findings:**
    *   **Work Mode Signal:** Column `how_much_of_your_work` contained categorical string values (e.g., "50% - About half of my time", "100% - All of my time").
    *   **Productivity Signal:** Column `relative_remote_productivity` contained sentiment-mixed string values (e.g., "I’m 50% more productive...", "My productivity is about same...").

### 2.2 Data Cleaning Pipeline (Function: `analyze_member2.py`)
**Challenge:** The raw data contained human-readable strings mixed with percentages, requiring regex extraction and normalization.

#### A. Percentage Parsing (`clean_percentage`)
*   **Logic:**
    *   Input: "50% - About half of my time" -> Output: `50` (int).
    *   Input: "Rarely or never" / "Less than 10%" -> Output: `0` or `5`.
    *   **Assumption:** Any mention of a percentage "X%" is the ground truth for that row.
*   **Implementation:** Simple string matching (`if "50%" in val: return 50`) was chosen over regex for this specific function due to the finite set of survey options.

#### B. Productivity Scoring (`clean_productivity`)
*   **Logic:**
    *   Input: "I’m 50% more productive..." -> Output: `+50` (int).
    *   Input: "I’m 20% less productive..." -> Output: `-20` (int).
    *   Input: "My productivity is about same..." -> Output: `0` (int).
*   **Implementation:**
    *   Used **Regular Expressions (Regex)**: `re.search(r'(\d+)%', val)` to extract the numeric value.
    *   **Conditional Logic:** Checked for substring "more productive" vs "less productive" to assign sign (+/-).

#### C. Null Handling
*   **Decision:** Dropped rows where *either* `prod_score` or `remote_pct` was NaN.
*   **Rationale:** We cannot analyze the relationship between work mode and productivity if one variable is missing. Imputation (guessing) would introduce bias.
*   **Impact:** Reduced dataset from ~1500 to **1,421** analyzeable rows.

### 2.3 Feature Engineering: Work Mode
*   **Logic:** Categorized the continuous `remote_pct` into three distinct buckets for clearer analysis:
    *   **Remote:** >= 80% (High remote intensity).
    *   **Hybrid:** > 20% AND < 80% (Mixed context).
    *   **On-site:** <= 20% (Low remote intensity).

### 2.4 Visualization Strategy (2021)
*   **Bar Chart (`productivity_by_mode.png`):** Chosen to show the *magnitude* of difference between groups.
*   **Histogram (`productivity_distribution.png`):** Chosen to show the *variance*. It revealed that while the average is positive, there is a "fat tail" of negative experiences, mostly in the On-site group.

---

## 3. Phase II: Comparative Analysis (2020 vs 2021)
**Script:** `comparative_analysis.py`
**Objective:** Analyze the *trend* over time. Are we getting better at remote work?

### 3.1 Schema Mapping & Normalization
**Challenge:** The 2020 dataset had different column names and slight format variations (e.g., typos like "I知" instead of "I'm").

*   **Mapping Table:**
    | Variable | 2021 Column | 2020 Column |
    | :--- | :--- | :--- |
    | **Work Pct** | `how_much_of_your_work` | `remote_time_last_3m` |
    | **Prod Score** | `relative_remote_productivity` | `relative_remote_productivity` |

*   **Logic Adaptation:**
    *   Created `clean_percentage_2020` to handle 2020-specific string formats (e.g., "Rarely or never").
    *   Reused `clean_productivity` but made it robust to the "I知" typo by focusing on the regex extraction of digits and the phrases "more/less productive".

### 3.2 Dataset Merging
*   **Technique:** Vertical Concatenation (`pd.concat`).
*   **Process:**
    1.  Processed 2020 and 2021 dataframes independently to create standardized `remote_pct` and `prod_score` columns.
    2.  Added a `year` label column ('2020', '2021') to each.
    3.  Concatenated them into `combined_df`.
*   **Final Volume:** **2,928** total rows (1,507 from 2020 + 1,421 from 2021).

### 3.3 Trend Analysis & Insights
*   **Grouping:** `combined_df.groupby(['year', 'work_mode'])['prod_score'].mean()`
*   **Key Finding:** The "Hybrid" group saw the largest YoY improvement (from +10.5% to +19.0%), suggesting "Hybrid" was the most difficult mode to master initially but offered high returns once established.

### 3.4 Visualization Strategy (Comparative)
*   **Grouped Bar Chart (`comparison_productivity_avg.png`):** Plotted `year` as the `hue` to allow direct side-by-side comparison of 2020 vs 2021 bars for each work mode.
*   **Kernel Density Estimate (KDE) Plot (`comparison_productivity_dist.png`):** Used `sns.kdeplot` to show the probability density of scores. This visually proved the entire population shifted "to the right" (more productive) in 2021 compared to 2020.

---

## 4. Error Handling & Iteration
*   **Issue:** F-String Syntax Error in `comparative_analysis.py`.
    *   *Cause:* Attempted to put a complex conditional logic with newlines inside an f-string `{...}` block.
    *   *Fix:* Refactored the logic outside the f-string into a variable `trend_text`, then passed the variable into the print statement. This improved readability and fixed the syntax error.
*   **Issue:** Path resolution.
    *   *Cause:* Running scripts from the root directory caused `FileNotFoundError` when scripts looked for `../datasets`.
    *   *Fix:* Used `os.path.dirname(os.path.abspath(__file__))` to dynamically resolve paths relative to the script, making the code portable.

---

## 5. Final Artifacts
All outputs are stored in `remote-work-effect/member2/`:
1.  `analysis_summary.txt`: 2021-specific stats.
2.  `comparative_analysis_summary.txt`: YoY trend stats.
3.  `productivity_by_mode.png`: 2021 Bar chart.
4.  `productivity_distribution.png`: 2021 Histogram.
5.  `comparison_productivity_avg.png`: Comparative Bar chart.
6.  `comparison_productivity_dist.png`: Comparative KDE plot.
7.  `presentation_source.md`: Content formatted for slide generation.