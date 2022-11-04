import pandas as pd
import plotly.express as px
import streamlit as st

from utils.loader import load_data

if "df" not in st.session_state:
    st.session_state.df = st.cache(load_data)()


def box_sal_exp(df: pd.DataFrame, work_years: list[int]):

    df_sub = df.query("work_year in @work_years").sort_values(by="experience_level")

    fig = px.box(
        df_sub,
        x="experience_level",
        y="salary_in_usd",
        color="experience_level",
        labels={
            "experience_level": "Experience Level",
            "salary_in_usd": "Salary in USD",
        },
    )

    return fig


def box_sal_comp_size(df: pd.DataFrame, work_years: list[int]):

    df_sub = df.query("work_year in @work_years").sort_values(by="company_size")

    fig = px.box(
        df_sub,
        x="company_size",
        y="salary_in_usd",
        color="company_size",
        labels={"company_size": "Company Size", "salary_in_usd": "Salary in USD"},
    )

    return fig


def box_sal_empl_type(df: pd.DataFrame, work_years: list[int]):

    df_sub = df.query("work_year in @work_years").sort_values(by="employment_type")
    fig = px.box(
        df_sub,
        x="employment_type",
        y="salary_in_usd",
        color="employment_type",
        labels={"employment_type": "Employment Type", "salary_in_usd": "Salary in USD"},
    )

    return fig


work_years = []

work_years.extend(
    list(
        range(
            2020, (st.sidebar.slider(label="Year", min_value=2020, max_value=2022) + 1)
        )
    )
)


fig1 = box_sal_exp(st.session_state.df, work_years)
fig2 = box_sal_comp_size(st.session_state.df, work_years)
fig3 = box_sal_empl_type(st.session_state.df, work_years)


tab1, tab2, tab3 = st.tabs(["Experience Level", "Company Size", "Employment Type"])

with tab1:
    st.markdown(
        f"""
# Characteristics of Salary by Experience Level
##### Years: [{', '.join(str(y) for y in work_years)}]
---\
"""
    )

    st.plotly_chart(fig1, use_container_width=True)


with tab2:
    st.markdown(
        f"""
# Characteristics of Salary by Company Size
##### Years: [{', '.join(str(y) for y in work_years)}]
---\
"""
    )
    st.plotly_chart(fig2)


with tab3:
    st.markdown(
        f"""
# Characteristics of Salary by Employment Type
##### Years: [{', '.join(str(y) for y in work_years)}]
---\
"""
    )
    st.plotly_chart(fig3)
