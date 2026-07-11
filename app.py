from drug_database import get_drug_recommendation
import streamlit as st
import pandas as pd

# Test Login
USERNAME = "harisaziz"
PASSWORD = "avoidit"

if "login" not in st.session_state:
    st.session_state.login = False


if not st.session_state.login:

    st.title("🔐 DosePK Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")


    if st.button("Login"):

        if username == USERNAME and password == PASSWORD:
            st.session_state.login = True
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid Username or Password")


    st.stop()


# Your pharmacy app starts below this line
# ==========================
# PAGE CONFIGURATION
# ==========================
st.set_page_config(
    page_title="DosePK",
    page_icon="💊",
    layout="centered"
)

# ==========================
# SIDEBAR
# ==========================
with st.sidebar:
    st.title("💊 DosePK")
    st.info("""
**Developer:** Haris Aziz

**Program:** Doctor of Pharmacy (Pharm-D)

**Purpose:** Renal Dose Adjustment Calculator
""")

# ==========================
# TITLE
# ==========================
st.markdown("""
# 💊 DosePK
### Clinical Decision Support System (CDSS)

**Renal Dose Adjustment Calculator**

---
""")

# ==========================
# PATIENT INFORMATION
# ==========================
st.header("👤 Patient Information")

age = st.number_input(
    "Age (Years)",
    min_value=1,
    max_value=120,
    value=18
)

gender = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

weight = st.number_input(
    "Weight (kg)",
    min_value=1.0,
    max_value=300.0,
    value=70.0
)
height = st.number_input(
    "Height (cm)",
    min_value=50.0,
    max_value=250.0,
    value=170.0
)

# BMI Calculation
height_m = height / 100

bmi = weight / (height_m ** 2)

st.subheader("⚖️ Body Mass Index (BMI)")
st.write(f"BMI: **{bmi:.2f}**")

if bmi < 18.5:
    st.info("BMI Category: Underweight")

elif bmi < 25:
    st.success("BMI Category: Normal Weight")

elif bmi < 30:
    st.warning("BMI Category: Overweight")

else:
    st.error("BMI Category: Obese")

scr = st.number_input(
    "Serum Creatinine (mg/dL)",
    min_value=0.1,
    max_value=20.0,
    value=1.0,
    step=0.1
)

# ==========================
# DRUG SELECTION
# ==========================
st.header("💊 Select Drug")

# Read all drugs from Excel
df = pd.read_excel("drugs.xlsx")

# Remove duplicates and sort alphabetically
drug_list = sorted(df["Drug"].unique())

drug = st.selectbox(
    "Drug",
    drug_list
)

# ==========================
# CALCULATE BUTTON
# ==========================
if st.button("Calculate"):

    # Cockcroft-Gault Formula
    if gender == "Male":
        crcl = ((140 - age) * weight) / (72 * scr)
    else:
        crcl = (((140 - age) * weight) / (72 * scr)) * 0.85

    st.success("✅ Calculation Completed")

    st.subheader("📊 Results")
    st.write(f"### Creatinine Clearance (CrCl): **{crcl:.2f} mL/min**")

    # ==========================
    # CKD STAGE
    # ==========================
    if crcl >= 90:
        stage = "🟢 Normal Kidney Function"
    elif crcl >= 60:
        stage = "🟡 Mild Renal Impairment"
    elif crcl >= 30:
        stage = "🟠 Moderate Renal Impairment"
    elif crcl >= 15:
        stage = "🔴 Severe Renal Impairment"
    else:
        stage = "⚫ Kidney Failure"

    st.subheader("🩺 Kidney Function Stage")
    st.info(stage)

    # ==========================
    # DOSE RECOMMENDATION
    # ==========================
    st.subheader("💊 Recommended Dose")

    recommendation = get_drug_recommendation(drug, crcl)

    if recommendation is not None:
        
        dose = recommendation["Recommended_Dose"]
        monitoring = recommendation["Monitoring"]
        warning = recommendation["Warning"]

        if str(dose) == "nan":
            dose = "Not Available"

        if str(monitoring) == "nan":
            monitoring = "No monitoring information."

        if str(warning) == "nan":
            warning = "No warning."

    else:
        dose = "No recommendation available."
        monitoring = "-"
        warning = "-"

    st.success(f"💊 Recommended Dose: {dose}")

    # ==========================
    # MONITORING
    # ==========================
    st.subheader("🩸 Monitoring")
    st.warning(f"⚠ {warning}")

    st.info(f"""
**Monitoring Required:**

{monitoring}
""")

    # ==========================
    # DISCLAIMER
    # ==========================
    st.markdown("---")
    st.caption(
        "⚠ This software is for educational and research purposes only. "
        "Always verify dosing recommendations using hospital guidelines or Lexicomp."
    )