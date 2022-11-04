import country_converter as coco
import pandas as pd
import plotly.express as px


def bar_job_title(df, work_years: list[int]):
    df_sub = df.query("work_year in @work_years")
    top_10_jt = df_sub.job_title.value_counts()[:10].index.to_list()
    jt = (
        df_sub.groupby(by=["job_title", "experience_level"])
        .salary_in_usd.count()
        .reset_index()
        .rename(columns={"salary_in_usd": "no_of_empls"})
        .set_index("job_title")
        .loc[top_10_jt]
        .reset_index()
    )
    fig = px.bar(
        jt,
        x="job_title",
        y="no_of_empls",
        color="experience_level",
        title=f'Top Job Titles in the years: {", ".join(str(y) for y in work_years)}',
        labels={
            "job_title": "Job Title",
            "no_of_empls": "No. of Employees",
            "experience_level": "Experience Level",
        },
    )

    return fig
