# Data Cleaning and Column Mapping Documentation

This document outlines the column renaming and data cleaning logic applied to the Remote Work Survey datasets.

## Dataset: 2020_rws.csv

### Table: Demographics & Employment
| Original Column (Keywords) | New Column Name |
| :--- | :--- |
| Response ID | `response_id` |
| Year were you born | `birth_year` |
| What is your gender | `gender` |
| Industry (Detailed) | `industry_detailed` |
| Industry | `industry` |
| Occupation (Detailed) | `occupation_detailed` |
| Occupation | `occupation` |
| Employed by your organisation | `org_size` |
| Manage people | `is_manager` |
| Describe your household | `household_type` |
| Long have you been in your current job | `job_tenure` |
| Metro / Regional | `metro_regional` |

### Table: Remote Work History & Preferences
| Original Column (Keywords) | New Column Name |
| :--- | :--- |
| Spend remote working last year | `remote_time_last_year` |
| Preferred to work remotely last year | `preferred_remote_last_year` |
| Spend remote working in the last 3 months | `remote_time_last_3m` |
| Preferred to work remotely in the last 3 months | `preferred_remote_last_3m` |
| Prefer to work remotely (Future) | `future_preferred_remote_time` |
| Choice about whether I work remotely | `future_location_choice_likelihood` |

### Table: Organizational Support (Last Year)
| Original Column (Keywords) | New Column Name |
| :--- | :--- |
| My organisation encouraged (Last Year) | `org_encouragement_last_year` |
| My organisation was well prepared (Last Year) | `org_preparedness_last_year` |
| It was common (Last Year) | `remote_prevalence_last_year` |
| Easy to get permission (Last Year) | `permission_ease_last_year` |
| I could easily collaborate (Last Year) | `collaboration_ease_last_year` |
| I would recommend (Last Year) | `remote_recommendation_last_year` |

### Table: Organizational Support (Last 3 Months)
| Original Column (Keywords) | New Column Name |
| :--- | :--- |
| My organisation encouraged (Last 3 Months) | `org_encouragement_last_3m` |
| My organisation was well prepared (Last 3 Months) | `org_preparedness_last_3m` |
| It was common (Last 3 Months) | `remote_prevalence_last_3m` |
| Easy to get permission (Last 3 Months) | `permission_ease_last_3m` |
| I could easily collaborate (Last 3 Months) | `collaboration_ease_last_3m` |
| I would recommend (Last 3 Months) | `remote_recommendation_last_3m` |

### Table: Future Expectations
| Original Column (Keywords) | New Column Name |
| :--- | :--- |
| Employer would encourage more remote working | `future_employer_encouragement_likelihood` |
| Employer would make changes to support remote working | `future_employer_support_likelihood` |

### Table: Productivity & Hours
| Original Column (Keywords) | New Column Name |
| :--- | :--- |
| Productivity when you work remotely | `relative_remote_productivity` |
| Workplace: Preparing for work and commuting | `office_commute_hours` |
| Workplace: Working | `office_work_hours` |
| Workplace: Personal and family time | `office_family_hours` |
| Workplace: Caring and domestic responsibilities | `office_domestic_hours` |
| Remote: Preparing for work and commuting | `remote_commute_hours` |
| Remote: Working | `remote_work_hours` |
| Remote: Personal and family time | `remote_family_hours` |
| Remote: Caring and domestic responsibilities | `remote_domestic_hours` |

### Table: Barriers & Aspects (Regex Mapped)
| Original Column Pattern | New Column Name |
| :--- | :--- |
| Most significant barrier... Connectivity... Caring | `most_barrier_infra_caring` |
| Least significant barrier... Connectivity... Caring | `least_barrier_infra_caring` |
| Most significant barrier... Connectivity... Motivation | `most_barrier_security_motivation` |
| Least significant barrier... Connectivity... Motivation | `least_barrier_security_motivation` |
| Most significant barrier... Connectivity... Workspace | `most_barrier_systems_workspace` |
| Least significant barrier... Connectivity... Workspace | `least_barrier_systems_workspace` |
| Most significant barrier... Connectivity... Management | `most_barrier_skills_living` |
| Least significant barrier... Connectivity... Management | `least_barrier_skills_living` |
| Most significant barrier... IT equipment... Motivation | `most_barrier_collab_motivation` |
| Least significant barrier... IT equipment... Motivation | `least_barrier_collab_motivation` |
| Best aspect... Family... Learning | `best_aspect_worklife_learning` |
| Worst aspect... Family... Learning | `worst_aspect_worklife_learning` |
| Best aspect... Family... Mental wellbeing | `best_aspect_social_wellbeing` |
| Worst aspect... Family... Mental wellbeing | `worst_aspect_social_wellbeing` |
| Best aspect... Family... Job satisfaction | `best_aspect_expenses_satisfaction` |
| Worst aspect... Family... Job satisfaction | `worst_aspect_expenses_satisfaction` |
| Best aspect... Hours... Mental wellbeing | `best_aspect_hours_commitments` |
| Worst aspect... Hours... Mental wellbeing | `worst_aspect_hours_commitments` |
| Best aspect... Hours... Job satisfaction | `best_aspect_personal_relationships` |
| Worst aspect... Hours... Job satisfaction | `worst_aspect_personal_relationships` |

---

## Dataset: 2021_rws.csv

### Table: Demographics & Employment
| Original Column (Keywords) | New Column Name |
| :--- | :--- |
| Year were you born | `birth_year` |
| What is your gender | `gender` |
| Industry | `industry` |
| Occupation | `occupation` |
| Employed by your organisation | `org_size_total` |
| Manage people | `is_manager` |
| Describe your household | `household_type` |
| Long have you been in your current job | `job_tenure_length` |
| Metro / Regional | `location_type` |

### Table: Remote Work History & Preferences
| Original Column (Keywords) | New Column Name |
| :--- | :--- |
| Spend remote working last year | `remote_time_last_year` |
| Spend remote working in the last 3 months | `remote_time_last_3_months` |
| Preferred to work remotely last year | `preferred_remote_last_year` |
| Preferred to work remotely in the last 3 months | `preferred_remote_last_3_months` |
| Prefer to work remotely (Future) | `preferred_remote_future` |

### Table: Organizational Support
| Original Column (Keywords) | New Column Name |
| :--- | :--- |
| Encouraged people to work remotely | `org_encouragement_score` |
| Well prepared for me to work remotely | `org_preparedness_score` |
| Common for people in my organisation | `org_remote_culture_prevalence` |
| Easy to get permission | `remote_permission_ease` |
| Collaborate with colleagues | `remote_collaboration_ease` |
| Recommend remote working | `remote_recommendation_score` |
| Employer would encourage | `future_employer_support_likelihood` |

### Table: Productivity & Hours
| Original Column (Keywords) | New Column Name |
| :--- | :--- |
| Productivity when you work remotely | `relative_remote_productivity` |
| Workplace: Preparing for work and commuting | `office_day_commute_hours` |
| Workplace: Working | `office_day_work_hours` |
| Workplace: Personal and family time | `office_day_personal_hours` |
| Workplace: Caring and domestic responsibilities | `office_day_caring_hours` |
| Remote: Preparing for work and commuting | `remote_day_commute_hours` |
| Remote: Working | `remote_day_work_hours` |
| Remote: Personal and family time | `remote_day_personal_hours` |
| Remote: Caring and domestic responsibilities | `remote_day_caring_hours` |

### Table: Barriers & Aspects (Descriptive)
| Original Column Pattern | New Column Name Logic |
| :--- | :--- |
| Most significant barrier | `barrier_most_<description>` |
| Least significant barrier | `barrier_least_<description>` |
| Biggest barriers | `barrier_most_<description>` |
| Smallest barriers | `barrier_least_<description>` |
| Worst aspect | `worst_remote_<description>` |
| Best aspect | `best_remote_<description>` |
| Have the following barriers | `barrier_<description>` |
