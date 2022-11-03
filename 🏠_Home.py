import streamlit as st

from utils.loader import load_data_from_database


if "df" not in st.session_state:
    st.session_state.df = load_data_from_database()


st.image('./images/cover.jpeg')

st.markdown(
f"""
<p align='center'>

### Informatics Practices Investigatory Project (2022-23)
---
## Web-based Interactive Dashboard for
# Global Salaries in AI/ML and Big Data

---
</p>


### About the Dataset:

**Source**: https://salaries.ai-jobs.net/download/

**Shape**: `{st.session_state.df.shape[0]}` _rows_ x `{st.session_state.df.shape[1]}` _columns_

**Columns**:
""",
unsafe_allow_html=True
)


st.markdown("""
1. **work_year**: The year the salary was paid. 
1. **experience_level**: The experience level in the job during the year with the following possible values:  
    - Junior  
    - Intermediate  
    - Expert  
    - Director  

1. **employment_type**: The type of employment for the role:
    - Part-time
    - Full-time
    - Contract
    - Freelance

1. **job_title**: The role worked in during the year.

1. **salary_in_usd**: The total gross salary amount paid in USD. 

1. **employee_residence**: Employee's primary country of residence in during the work year

1. **remote_ratio**: The overall amount of work done remotely, possible values are as follows:
    - No remote work (less than 20%)
    - Partially remote
    - Fully remote (more than 80%)

1. **company_location**: The country of the employer's main office or contracting branch

1. **company_size**: The average number of people that worked for the company during the year.
    - Small (less than 50 employees)
    - Medium (50 to 250 employees)
    - Large (more than 250 employees)

""",
unsafe_allow_html=True
) 


st.dataframe(st.session_state.df.sample(n=5, random_state=42))

# import plotly.express as px
# import country_converter as coco

# import pandas as pd
