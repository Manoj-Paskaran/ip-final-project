import country_converter as coco
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.loader import load_data, load_data_from_csv

if "df" not in st.session_state:
    st.session_state.df = load_data_from_csv()


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


fig = chloropleth_empl_country()

st.plotly_chart(st.session_state.df, work_years=2020)
