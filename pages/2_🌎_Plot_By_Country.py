import country_converter as coco
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.loader import load_data

if "df" not in st.session_state:
    st.session_state.df = st.cache(load_data)()


def chloropleth_empl_country(
    df: pd.DataFrame, work_years: list[int], experience_levels: list[str]
):

    cn = (
        df.query("work_year in @work_years and experience_level in @experience_levels")
        .employee_residence.value_counts()
        .to_frame()
        .reset_index()
        .rename(columns={"index": "country", "employee_residence": "no_of_empls"})
    )

    fig = px.choropleth(
        cn,
        locations=coco.convert(names=cn.country, to="ISO3"),
        color="no_of_empls",
        range_color=(0, cn.no_of_empls.quantile(0.98)),
        hover_name="country",
        labels={
            "no_of_empls": "No. of Employees",
        },
    )

    return fig


def chloropleth_sal_country(
    df: pd.DataFrame, work_years: list[int], experience_levels: list[str]
):

    sal_by_country = (
        df.query("work_year in @work_years and experience_level in @experience_levels")
        .groupby(["salary_in_usd", "company_location"])
        .size()
        .reset_index()
        .groupby("company_location")
        .median()
        .reset_index()
    )

    fig = px.choropleth(
        locations=coco.convert(names=sal_by_country.company_location, to="ISO3"),
        color=sal_by_country.salary_in_usd,
    )

    return fig


st.sidebar.write("Filter Years: ")

work_years = []

work_years.extend(
    list(
        range(
            2020, (st.sidebar.slider(label="Year", min_value=2020, max_value=2022) + 1)
        )
    )
)

st.sidebar.write("Filter Experience Levels: ")
experience_levels = []

if st.sidebar.checkbox(label="Junior", value=True):
    experience_levels.append("Junior")

if st.sidebar.checkbox(label="Intermediate", value=True):
    experience_levels.append("Intermediate")

if st.sidebar.checkbox(label="Expert", value=True):
    experience_levels.append("Expert")

if st.sidebar.checkbox(label="Director", value=True):
    experience_levels.append("Director")


fig = chloropleth_empl_country(
    st.session_state.df, work_years=work_years, experience_levels=experience_levels
)

fig_2 = chloropleth_sal_country(
    st.session_state.df, work_years=work_years, experience_levels=experience_levels
)

tab1, tab2 = st.tabs(["No. of Employees", "Median Salary"])

with tab1:
    st.markdown(
        f"""
# No. of Employees by Country
---
##### Years: [{', '.join(str(y) for y in work_years)}]
##### Exp. Levels: [{', '.join(experience_levels)}]
"""
    )

    st.plotly_chart(fig)


with tab2:
    st.markdown(
        f"""
# Median Salary by Country
---
##### Years: [{', '.join(str(y) for y in work_years)}]
##### Exp. Levels: [{', '.join(experience_levels)}]
"""
    )

    st.plotly_chart(fig_2)

    #         title=f"Distribution of Employees in years: \
    # [{', '.join(str(y) for y in work_years)}] \
    # and experience_levels: \
    # [{', '.join(experience_levels)}]",
    # animation_frame=df.work_year.unique(),


# if st.sidebar.checkbox(label="2020", value=True):
#     work_years.append(2020)

# if st.sidebar.checkbox(label="2021", value=True):
#     work_years.append(2021)

# if st.sidebar.checkbox(label="2022", value=True):
#     work_years.append(2022)
