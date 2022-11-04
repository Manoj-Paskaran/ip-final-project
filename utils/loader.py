import country_converter as coco
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine


def load_data() -> pd.DataFrame:

    try:
        connection = create_engine(
            f"mysql+pymysql://root:{st.secrets.root_password}@localhost:3306/data"
        ).connect()

        df = pd.read_sql_table(table_name="salaries", con=connection, schema="data")

    finally:
        connection.close()

    return clean_df(df)


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    remote_ratio_map = {
        0: "No remote work",
        50: "Partially remote",
        100: "Fully remote",
    }

    experience_level_map = {
        "EN": "Junior",
        "MI": "Intermediate",
        "SE": "Expert",
        "EX": "Director",
    }

    employment_type_map = {
        "PT": "Part-time",
        "FT": "Full-time",
        "CT": "Contract",
        "FL": "Freelance",
    }

    company_size_map = {
        "S": "Small",
        "M": "Medium",
        "L": "Large",
    }

    df: pd.DataFrame = (
        df.astype(
            {
                "work_year": "category",
                "experience_level": pd.CategoricalDtype(
                    experience_level_map.keys(), ordered=True
                ),
                "employment_type": pd.CategoricalDtype(
                    employment_type_map.keys(), ordered=True
                ),
                "company_size": pd.CategoricalDtype(
                    company_size_map.keys(), ordered=True
                ),
                "remote_ratio": pd.CategoricalDtype(
                    remote_ratio_map.keys(), ordered=True
                ),
            }
        )
        .drop(columns=["salary", "salary_currency"])
        .replace(
            {
                "remote_ratio": remote_ratio_map,
                "experience_level": experience_level_map,
                "employment_type": employment_type_map,
                "company_size": company_size_map,
                "employee_residence": dict(
                    zip(
                        df.employee_residence.unique(),
                        coco.convert(df.employee_residence.unique(), to="name_short"),
                    )
                ),
                "company_location": dict(
                    zip(
                        df.company_location.unique(),
                        coco.convert(df.company_location.unique(), to="name_short"),
                    )
                ),
            },
        )
        .assign(working_overseas=lambda x: x.employee_residence != x.company_location)
    )
    return df


def load_data_from_csv() -> pd.DataFrame:

    csv_path = r"C:\dev\data-science\projects\ip-final-project\data\salaries.csv"
    df = pd.read_csv(csv_path)
    return clean_df(df)


# def load_data_uncached() -> pd.DataFrame:
#     return load_data_from_csv()

# load_data_from_csv = st.cache(load_data_from_csv)
# load_data_from_database = st.cache(load_data_from_database)


# if __name__ == '__main__':
#     df = load_data_from_csv()
#     print(df)

#     df = load_data_from_database()
#     print(df)


# from dotenv import load_dotenv
# # Loading MySQL Root Password
# load_dotenv()

# from pathlib import Path

# import pandas as pd
# import country_converter as coco
# import streamlit as st


# def load_data():

#     remote_ratio_map = {
#         0: "No remote work",
#         50: "Partially remote",
#         100: "Fully remote",
#     }

#     experience_level_map = {
#         "EN": "Junior",
#         "MI": "Intermediate",
#         "SE": "Expert",
#         "EX": "Director",
#     }

#     employment_type_map = {
#         "PT": "Part-time",
#         "FT": "Full-time",
#         "CT": "Contract",
#         "FL": "Freelance",
#     }

#     company_size_map = {
#         "S": "Small",
#         "M": "Medium",
#         "L": "Large",
#     }

#     data_path = Path(__file__).parent.joinpath(r'data\salaries.csv')

#     df: pd.DataFrame = (
#         pd.read_csv(data_path)
#         .astype(
#             {
#                 "work_year": "category",
#                 "experience_level": pd.CategoricalDtype(
#                     experience_level_map.keys(), ordered=True
#                 ),
#                 "employment_type": pd.CategoricalDtype(
#                     employment_type_map.keys(), ordered=True
#                 ),
#                 "company_size": pd.CategoricalDtype(
#                     company_size_map.keys(), ordered=True
#                 ),
#                 "remote_ratio": pd.CategoricalDtype(
#                     remote_ratio_map.keys(), ordered=True
#                 ),
#             }
#         )
#         .drop(columns=["salary", "salary_currency"])
#     )

#     df["working_overseas"] = df.employee_residence != df.company_location

#     df = df.replace(
#         {
#             "remote_ratio": remote_ratio_map,
#             "experience_level": experience_level_map,
#             "employment_type": employment_type_map,
#             "company_size": company_size_map,
#             "employee_residence": dict(
#                 zip(
#                     df.employee_residence.unique(),
#                     coco.convert(df.employee_residence.unique(), to="name_short"),
#                 )
#             ),
#             "company_location": dict(
#                 zip(
#                     df.company_location.unique(),
#                     coco.convert(df.company_location.unique(), to="name_short"),
#                 )
#             ),
#         },
#     )

#     return df

# # load_data_from_sql():

# load_data_uncached = load_data

# load_data = st.cache(load_data)

# if __name__ == "__main__":
#     df = load_data_uncached()
#     print(df)
#     # print(Path(__file__).parent.joinpath(r'data\salaries.csv'))


# def load_df_to_mysql() -> None:

#     print("Load df to mysql is running...")
#     df = pd.read_csv(DATA_FOLDER.joinpath('salaries.csv'))

#     try:
#         connection = create_engine(
#             f"mysql+pymysql://root:{os.environ.get('ROOT_PASSWORD')}@localhost:3306/data"
#         ).connect()

#         df.to_sql(
#             name='salaries',
#             con=connection,
#             schema='data',
#             if_exists='replace',
#             index=False
#         )

#     finally:
#         connection.close()
