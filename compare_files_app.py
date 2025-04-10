import streamlit as st
import pandas as pd
import os

# Set page config and custom name on the top-right
st.set_page_config(page_title="Compare Files App", layout="wide")
st.markdown("<div style='text-align: right; font-weight: bold; font-size: 20px;'>SOURAV THAKUR</div>", unsafe_allow_html=True)

# Title
st.title(":bar_chart: File Comparison Tool")
st.markdown("### Upload any two files to compare (Excel, CSV, or others):")

# Accept All File Types
file1 = st.file_uploader("Upload First DDE File", type=None)
file2 = st.file_uploader("Upload Second Taxtech File", type=None)

def read_file(file):
    ext = os.path.splitext(file.name)[-1].lower()
    try:
        if ext in ['.csv']:
            return pd.read_csv(file)
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(file)
        else:
            st.warning(f"Unsupported file type: {ext}. Only Excel or CSV supported for comparison.")
            return None
    except Exception as e:
        st.error(f"Error reading file '{file.name}': {e}")
        return None

if file1 and file2:
    df1 = read_file(file1)
    df2 = read_file(file2)

    if df1 is not None and df2 is not None:
        common_columns = set(df1.columns) & set(df2.columns)

        results = []
        mismatch_notes = []

        for col in common_columns:
            count1, count2 = df1[col].count(), df2[col].count()

            if "id" in col.lower():
                status = "🟡✔" if count1 == count2 else "❌"
                if count1 != count2:
                    mismatch_notes.append(f"{col}: Count in DDE File = {count1}, Count in Taxtech File = {count2}")
                results.append((col, count1, count2, "-", "-", status))
            else:
                df1[col] = pd.to_numeric(df1[col], errors="coerce")
                df2[col] = pd.to_numeric(df2[col], errors="coerce")
                sum1, sum2 = df1[col].sum(), df2[col].sum()

                if count1 == count2 and sum1 == sum2:
                    status = "🟢✔"
                elif count1 == count2:
                    status = "🟡✔"
                else:
                    status = "❌"
                    mismatch_notes.append(f"{col}: Count in DDE File = {count1}, Count in Taxtech File = {count2}")

                results.append((col, count1, count2, f"{sum1:.2f}", f"{sum2:.2f}", status))

        st.markdown("### 📊 Comparison Results:")
        st.table(pd.DataFrame(results, columns=["Column", "Count in DDE File", "Count in Taxtech File", "Sum in DDE File", "Sum in Taxtech File", "Status"]))

        # Show columns not in both
        missing_in_file1 = list(set(df2.columns) - set(df1.columns))
        missing_in_file2 = list(set(df1.columns) - set(df2.columns))

        if missing_in_file1 or missing_in_file2:
            st.markdown("### ⚠ Columns Not Present in Both Files:")

            max_len = max(len(missing_in_file1), len(missing_in_file2))
            missing_in_file1 += ["-"] * (max_len - len(missing_in_file1))
            missing_in_file2 += ["-"] * (max_len - len(missing_in_file2))

            missing_df = pd.DataFrame({
                "Missing in DDE File": missing_in_file1,
                "Missing in Taxtech File": missing_in_file2
            })

            st.table(missing_df)

        # Notepad at the end for mismatch columns
        if mismatch_notes:
            st.markdown("### 📝 Columns with Count Mismatch:")
            default_text = "\n".join(mismatch_notes)
            st.text_area("Review or Edit Count Mismatch Notes Below:", value=default_text, height=200)


