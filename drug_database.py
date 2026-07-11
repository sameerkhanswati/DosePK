import pandas as pd

# Load the Excel database
df = pd.read_excel("drugs.xlsx")

def get_drug_recommendation(drug_name, crcl):

    result = df[
        (df["Drug"] == drug_name) &
        (df["CrCl_Min"] <= crcl) &
        (df["CrCl_Max"] >= crcl)
    ]

    if result.empty:
        return None

    return result.iloc[0]