from pathlib import Path

import country_converter as coco
import pandas as pd

csv_path = r".\data\salaries.csv"

df = pd.read_csv(csv_path)

df = df.drop(columns=["salary", "salary_currency"])

df["working_overseas"] = df.employee_residence != df.company_location

df = df.replace(
    {
        "remote_ratio": {
            0: "No remote work",
            50: "Partially remote",
            100: "Fully remote",
        },
        "experience_level": {
            "EN": "Junior",
            "MI": "Intermediate",
            "SE": "Expert",
            "EX": "Director",
        },
        "employment_type": {
            "PT": "Part-time",
            "FT": "Full-time",
            "CT": "Contract",
            "FL": "Freelance",
        },
        "company_size": {
            "S": "Small",
            "M": "Medium",
            "L": "Large",
        },
        "employee_residence": dict(
            zip(
                df.employee_residence,
                coco.convert(df.employee_residence, to="name_short"),
            )
        ),
        "company_location": dict(
            zip(
                df.company_location,
                coco.convert(df.company_location, to="name_short"),
            )
        ),
    },
)

df.to_csv(
    r"data\salaries_clean.csv",
    index=False,
)
