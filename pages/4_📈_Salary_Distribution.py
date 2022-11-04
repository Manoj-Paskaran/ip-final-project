import pandas as pd
import plotly.figure_factory as ff
import streamlit as st

from utils.loader import load_data

if "df" not in st.session_state:
    st.session_state.df = st.cache(load_data)()


def dist_sal_by_work_year(df):

    y2020 = df.query("work_year == 2020")
    y2021 = df.query("work_year == 2021")
    y2022 = df.query("work_year == 2022")

    hist_data = [y2020.salary_in_usd, y2021.salary_in_usd, y2022.salary_in_usd]
    group_labels = ["2020", "2021", "2022"]

    fig = ff.create_distplot(hist_data, group_labels, show_hist=False)

    return fig


def dist_sal_by_exp_level(df: pd.DataFrame):
    exp_level_sal = df[["experience_level", "salary_in_usd"]]

    entry_salary = exp_level_sal.query("experience_level == 'Junior'")
    executive_salary = exp_level_sal.query("experience_level == 'Director'")
    mid_salary = exp_level_sal.query("experience_level == 'Intermediate'")
    senior_salary = exp_level_sal.query("experience_level == 'Expert'")

    hist_data = [
        entry_salary.salary_in_usd,
        mid_salary.salary_in_usd,
        senior_salary.salary_in_usd,
        executive_salary.salary_in_usd,
    ]
    group_labels = ["Junior", "Intermediate", "Expert", "Director"]

    fig = ff.create_distplot(
        hist_data,
        group_labels,
        show_hist=False,
    )

    return fig


def dist_sal_by_company_size(df):
    exp_level_sal = df[["experience_level", "salary_in_usd"]]

    c_size = df[["company_size", "salary_in_usd"]]
    small = exp_level_sal.loc[c_size["company_size"] == "Small"]
    medium = exp_level_sal.loc[c_size["company_size"] == "Medium"]
    large = exp_level_sal.loc[c_size["company_size"] == "Large"]

    hist_data = [
        small["salary_in_usd"],
        medium["salary_in_usd"],
        large["salary_in_usd"],
    ]
    group_labels = ["Small", "Mid", "Large"]

    fig = ff.create_distplot(hist_data, group_labels, show_hist=False)

    return fig


fig1 = dist_sal_by_work_year(st.session_state.df)
fig2 = dist_sal_by_exp_level(st.session_state.df)
fig3 = dist_sal_by_company_size(st.session_state.df)


tab1, tab2, tab3 = st.tabs(["Work Year", "Experience Level", "Company Size"])

with tab1:
    st.markdown(
        f"""
# Distribution of Salary by Work Year

"""
    )

    st.plotly_chart(fig1, use_container_width=True)


with tab2:
    st.markdown(
        f"""
# Distribution of Salary by Experience Level
"""
    )
    st.plotly_chart(fig2)


with tab3:
    st.markdown(
        f"""
# Distribution of Salary by Company Size
"""
    )
    st.plotly_chart(fig3)
