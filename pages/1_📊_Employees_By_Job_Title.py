import streamlit as st
import pandas as pd
import plotly.express as px

from utils.loader import load_data_from_database

if "df" not in st.session_state:
    st.session_state.df = load_data_from_database()


def bar_job_title(df: pd.DataFrame, work_years: list[int]):

    if work_years == []:
        return None, None

    df_sub = df.query("work_year in @work_years")

    top_jt = df_sub.job_title.value_counts().head(15)

    jt = (
        df_sub.groupby(by=["job_title", "experience_level"])
        .salary_in_usd.count()
        .reset_index()
        .rename(columns={"salary_in_usd": "no_of_empls"})
        .set_index("job_title")
        .loc[top_jt.index.to_list()]
        .reset_index()
    )

    no_1_jt = jt.query("job_title == @top_jt.head(1).index.values[0]")

    fig = px.bar(
        jt,
        x="job_title",
        y="no_of_empls",
        color="experience_level",
        labels={
            "job_title": "Job Title",
            "no_of_empls": "No. of Employees",
            "experience_level": "Experience Level",
        },
    )

    return no_1_jt, fig

def bar_sal_job_title(df: pd.DataFrame, work_years: list[int]):

    if work_years == []:
        return None, None

    df_sub = df.query("work_year in @work_years")

    ms =(
        df_sub
        .groupby(['job_title', 'experience_level'])
        .salary_in_usd
        .median()
        .reset_index()
        .rename(columns={"salary_in_usd": "median_salary"})
    )

    top_ms = ms.groupby('job_title').median_salary.sum().nlargest(15)

    no_1_ms = ms.query("job_title == @top_ms.head(1).index.values[0]")

    ms10 = (
        ms
        .set_index('job_title')
        .loc[top_ms.index.to_list()]
        .reset_index()

    )

    fig = px.bar(
        ms10,
        x="job_title",
        y="median_salary",
        color="experience_level",
        labels={
            'median_salary': "Median Salary",
            'job_title': 'Job Title'
        }
    )

    return no_1_ms, fig


st.sidebar.write("""Filter Years:""")

work_years = []

if st.sidebar.checkbox(label="2020", value=True):
    work_years.append(2020)

if st.sidebar.checkbox(label="2021", value=True):
    work_years.append(2021)

if st.sidebar.checkbox(label="2022", value=True):
    work_years.append(2022)

# st.sidebar.write("Filter Experience Levels: ")
# st.sidebar.checkbox(label="Junior")
# st.sidebar.checkbox(label="Intermediate")
# st.sidebar.checkbox(label="Expert")
# st.sidebar.checkbox(label="Director")


# st.sidebar.slider(label="year", min_value=2020, max_value=2022)

no_1_jt, fig_jt = bar_job_title(df=st.session_state.df, work_years=work_years)
no_1_ms, fig_ms = bar_sal_job_title(df=st.session_state.df, work_years=work_years)

tab1, tab2 = st.tabs(["No. of Employees", "Median Salary"])

with tab1:
    st.markdown(
        f"""\
    # No. of Employees *by* Job Title
    ##### Years: [{', '.join(str(y) for y in work_years)}]
    ---\
    """
    )



    if no_1_jt is not None:
        left, right = st.columns(2)
        left.metric(label="Top Job Title", value=no_1_jt.job_title.iloc[0])
        right.metric(label="Total No.of Employees", value=no_1_jt.no_of_empls.sum())

    if fig_jt is not None:
        st.plotly_chart(fig_jt)


with tab2:
    st.markdown(
        f"""\
        # Median Salary by Job Title
        ##### Years: [{', '.join(str(y) for y in work_years)}]
        ---\

        """
    )
    if no_1_ms is not None:
        left, right = st.columns([2, 1])
        left.metric(label="Highest Paying Job Title", value=no_1_ms.job_title.iloc[0])
        right.metric(label="Median Salary", value=f"{no_1_ms.median_salary.sum(): ,} USD", )

    if fig_ms is not None:
        st.plotly_chart(fig_ms)

# with right:
# max_job_title = jt.sort_values(by='no_of_empls', ascending=False).iloc[0].job_title
# st.write(jt[max_job_title])
