import pandas as pd
import plotly.express as px
import streamlit as st

from utils.loader import load_data

if "df" not in st.session_state:
    st.session_state.df = st.cache(load_data)()


def pie_exp_lvl(df: pd.DataFrame, work_years: list[int]):

    exp_lvl = (
        df.query("work_year in @work_years")
        .experience_level.value_counts()
        .sort_index()
    )
    fig = px.pie(names=exp_lvl.index, values=exp_lvl.values, color=exp_lvl.index)
    fig.update_traces(
        textinfo="label+percent+value",
    )

    return fig


def pie_comp_size(df: pd.DataFrame, work_years: list[int]):

    comp_size = (
        df.query("work_year in @work_years").company_size.value_counts().sort_index()
    )
    fig = px.pie(
        names=comp_size.index,
        values=comp_size.values,
        color=comp_size.index,
    )
    fig.update_traces(
        textinfo="label+percent+value",
    )

    return fig


def pie_empl_type(df: pd.DataFrame, work_years: list[int]):

    empl_type = (
        df.query("work_year in @work_years").employment_type.value_counts().sort_index()
    )
    fig = px.pie(
        names=empl_type.index,
        values=empl_type.values,
        color=empl_type.index,
    )
    fig.update_traces(
        textinfo="label+percent+value",
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

fig1 = pie_exp_lvl(df=st.session_state.df, work_years=work_years)
fig2 = pie_comp_size(df=st.session_state.df, work_years=work_years)
fig3 = pie_empl_type(df=st.session_state.df, work_years=work_years)

tab1, tab2, tab3 = st.tabs(["Experience Level", "Company Size", "Employment Type"])

with tab1:
    st.markdown(
        f"""
# Distribution of Experience Level
##### Years: [{', '.join(str(y) for y in work_years)}]
---\
"""
    )

    st.plotly_chart(fig1, use_container_width=True)


with tab2:
    st.markdown(
        f"""
# Distribution of Company Size
##### Years: [{', '.join(str(y) for y in work_years)}]
---\
"""
    )
    st.plotly_chart(fig2, use_container_width=True)


with tab3:
    st.markdown(
        f"""
# Distribution of Employment Type
##### Years: [{', '.join(str(y) for y in work_years)}]
---\
"""
    )
    st.plotly_chart(fig3, use_container_width=True)

    # color_discrete_map={
    #     'Small': '#636efa',
    #     'Medium': '#ef553b',
    #     'Large': '#00cc96'
    # # }
    # color_discrete_sequence=px.colors.qualitative.Plotly,
    # category_orders={
    #     'company_size':['Small', 'Medium', 'Large']
    # }


# st.sidebar.write("""Filter Years:""")

# work_years = []

# if st.sidebar.checkbox(label="2020", value=True):
#     work_years.append(2020)

# if st.sidebar.checkbox(label="2021", value=True):
#     work_years.append(2021)

# if st.sidebar.checkbox(label="2022", value=True):
#     work_years.append(2022)


# color_discrete_map={
#     'Small': '#636efa',
#     'Medium': '#ef553b',
#     'Large': '#00cc96'
# }
