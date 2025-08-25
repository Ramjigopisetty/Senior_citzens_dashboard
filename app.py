import streamlit as st
import pandas as pd
import os
from datetime import date
import gspread
from google.oauth2.service_account import Credentials

# ---------- Google Sheets Setup ----------
SHEET_ID = "1L5pgfxHu6DMFYkZ474rqPz2fvF8KQp1byaOofYy091M"  # Change this to your Google Sheet name
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Authenticate with service account
creds = Credentials.from_service_account_file("creds.json", scopes=SCOPES)
client = gspread.authorize(creds)

try:
    sheet = client.open_by_key(SHEET_ID).sheet1
except Exception as e:
    st.error(f"❌ Could not open Google Sheet with ID {SHEET_ID}. "
         f"Make sure your service account email has access (Editor role). Error: {e}")

    st.stop()

# ---------- Helpers ----------
COLUMNS = [
    "PatientID","Name","PhoneNumber","MedicationName","Dosage","Frequency",
    "LastAdministeredDate","NextDueDate","Time","Notes"
]

def load_data():
    """Load data from Google Sheets into DataFrame"""
    records = sheet.get_all_records()
    if not records:
        return pd.DataFrame(columns=COLUMNS)
    return pd.DataFrame(records)

def save_data(df: pd.DataFrame):
    """Overwrite Google Sheet with DataFrame contents"""
    data = [df.columns.tolist()] + df.fillna("").values.tolist()
    sheet.clear()
    sheet.update(data)

def rerun():
    """Safe rerun for different Streamlit versions"""
    try:
        st.rerun()
    except Exception:
        try:
            st.experimental_rerun()
        except Exception:
            pass

# ---------- App Setup ----------
st.set_page_config(page_title="Senior Medication Dashboard", layout="wide")
st.title("💊 Senior Medication Dashboard")

# Session state defaults
for key, default in {
    "show_add_form": False,
    "show_modify_form": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

df = load_data()

# ---------- Top Actions ----------
col_a, col_b = st.columns([1,1])
with col_a:
    if st.button("➕ Add New Patient", key="add_btn"):
        st.session_state.show_add_form = True
with col_b:
    st.button("⏰ Set Reminder", key="rem_btn")  # placeholder for future

# ---------- Add New Patient Form ----------
if st.session_state.show_add_form:
    with st.form("add_form", clear_on_submit=False):
        st.subheader("Add New Patient Record")
        c1, c2, c3 = st.columns(3)
        with c1:
            pid = st.text_input("Patient ID")
            dosage = st.text_input("Dosage")
            last_date = st.text_input(
                "Last Administered Date",
                value=date.today().strftime("%m/%d/%Y")
            )
        with c2:
            name = st.text_input("Name")
            phone = st.text_input("Phone Number")
            freq = st.text_input("Frequency")
            next_date = st.text_input(
                "Next Due Date",
                value=date.today().strftime("%m/%d/%Y")
            )
        with c3:
            med = st.text_input("Medication Name")
            time_ = st.text_input("Time (e.g., 09:00 AM)")
            notes = st.text_input("Notes")

        sb1, sb2 = st.columns([1,1])
        with sb1:
            submitted = st.form_submit_button("Save", use_container_width=True)
        with sb2:
            cancel = st.form_submit_button("Cancel", use_container_width=True)

        if cancel:
            st.session_state.show_add_form = False
            rerun()

        if submitted:
            if not pid:
                st.error("⚠️ Patient ID is required.")
            elif pid in df["PatientID"].astype(str).tolist():
                st.error("⚠️ Patient ID already exists. Please use a unique ID.")
            else:
                new_row = {
                    "PatientID": pid,
                    "Name": name,
                    "PhoneNumber": phone,
                    "MedicationName": med,
                    "Dosage": dosage,
                    "Frequency": freq,
                    "LastAdministeredDate": last_date,
                    "NextDueDate": next_date,
                    "Time": time_,
                    "Notes": notes,
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)
                st.session_state.show_add_form = False
                st.success("✅ New patient added.")
                rerun()

# ---------- Table ----------
st.dataframe(df, use_container_width=True)

# ---------- Manage Records ----------
st.subheader("Manage Records")
if len(df) == 0:
    st.info("No records available.")
else:
    ids = df["PatientID"].astype(str).tolist()
    selected_id = st.selectbox("Patient ID:", ids, key="manage_select")

    left, right = st.columns([1,1])
    with left:
        if st.button("✏️ Modify Record", key="mod_btn"):
            st.session_state.show_modify_form = True
    with right:
        if st.button("🗑️ Delete Record", key="del_btn"):
            df2 = df[df["PatientID"].astype(str) != selected_id].copy()
            save_data(df2)
            st.success(f"🗑️ Record with Patient ID {selected_id} deleted.")
            rerun()

    if st.session_state.show_modify_form:
        record = df[df["PatientID"].astype(str) == selected_id].iloc[0].to_dict()
        with st.form("modify_form", clear_on_submit=False):
            st.subheader(f"Modify Record — Patient ID: {selected_id}")
            c1, c2, c3 = st.columns(3)
            with c1:
                name = st.text_input("Name", value=record["Name"])
                phone = st.text_input("Phone Number", value=record.get("PhoneNumber",""))
                dosage = st.text_input("Dosage", value=record["Dosage"])
                last_date = st.text_input("Last Administered Date", value=record["LastAdministeredDate"])
            with c2:
                med = st.text_input("Medication Name", value=record["MedicationName"])
                freq = st.text_input("Frequency", value=record["Frequency"])
                next_date = st.text_input("Next Due Date", value=record["NextDueDate"])
            with c3:
                time_ = st.text_input("Time", value=record["Time"])
                notes = st.text_input("Notes", value=record["Notes"])

            sb1, sb2 = st.columns([1,1])
            with sb1:
                save = st.form_submit_button("Save Changes", use_container_width=True)
            with sb2:
                cancel = st.form_submit_button("Cancel", use_container_width=True)

            if cancel:
                st.session_state.show_modify_form = False
                rerun()

            if save:
                mask = df["PatientID"].astype(str) == selected_id
                df.loc[mask, COLUMNS[1:]] = \
                    [name, phone, med, dosage, freq, last_date, next_date, time_, notes]
                save_data(df)
                st.session_state.show_modify_form = False
                st.success(f"✅ Record for Patient ID {selected_id} updated.")
                rerun()

# ---------- Export ----------
st.subheader("Export Data")
st.write("Download the current medication list as a CSV file. Any changes you've made will be included.")
st.download_button(
    label="⬇️ Download Reminders CSV",
    data=load_data().to_csv(index=False).encode("utf-8"),
    file_name="reminders.csv",
    mime="text/csv",
    key="dl_btn",
)
