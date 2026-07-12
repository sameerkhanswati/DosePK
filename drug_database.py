import pandas as pd

# Read Excel
df = pd.read_excel("drugs.xlsx")

# Remove extra spaces
df["Drug Name"] = df["Drug Name"].astype(str).str.strip()
df["CrCl Range (mL/min)"] = df["CrCl Range (mL/min)"].astype(str).str.strip()


def get_drug_recommendation(drug_name, crcl):

    drug_name = drug_name.strip()

    # Get all rows for selected drug
    print("Selected Drug:", drug_name)

    print("Drugs in Excel:")
    print(df["Drug Name"].tolist())

    drug_rows = df[df["Drug Name"].str.strip().str.lower() == drug_name.strip().lower()]

    print("Selected Drug:", drug_name)
    print("Calculated CrCl:", crcl)
    print("Matching rows:")
    print(drug_rows)  # Temporary debugging

    if drug_rows.empty:
        return None

    for _, row in drug_rows.iterrows():
        print("Checking range:", row["CrCl Range (mL/min)"])
        rng = row["CrCl Range (mL/min)"]

        rng = rng.replace("≥", ">=").replace("–", "-")

        if rng.startswith(">="):
            value = float(rng[2:])
            if crcl >= value:
                return row

        elif "-" in rng:
            low, high = rng.split("-")
            if float(low) <= crcl <= float(high):
                return row

        elif rng.startswith("<"):
            value = float(rng[1:])
            if crcl < value:
                return row

    return None