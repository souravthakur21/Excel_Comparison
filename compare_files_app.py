import streamlit as st
import pandas as pd

st.set_page_config(page_title="File Comparison Tool", layout="wide")

# Session state for help toggle
if "show_help" not in st.session_state:
    st.session_state.show_help = False

# Inject custom CSS for footer and button alignment
st.markdown("""
    <style>
        .footer {
            position: fixed;
            right: 20px;
            bottom: 10px;
            font-size: 16px;
            font-weight: bold;
            color: #6c757d;
        }
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .help-btn {
            margin-left: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# Header and Help Button
with st.container():
    cols = st.columns([10, 1])
    with cols[0]:
        st.markdown("<h2 style='display: inline;'>📊 File Comparison Tool</h2>", unsafe_allow_html=True)
    with cols[1]:
        if st.button("❓ Help", key="help_button"):
            st.session_state.show_help = True

# HELP SCREEN ONLY
if st.session_state.show_help:
    st.markdown("### ✅ DDE vs Taxtech File Comparison Tool – User Guide")
    st.markdown("""
    #### 📌 Purpose:
    This tool helps you compare two data files (Excel or CSV) – typically a DDE File and a Taxtech File – to:
    - Match columns by name  
    - Compare row counts and numeric sums  
    - Highlight mismatches and missing columns  

    #### 🛠 How to Use:
    1. **Upload Files**
       - Upload your first file (**DDE File**).
       - Upload your second file (**Taxtech File**).
       - All file types are accepted, but only Excel/CSV are compared.

    2. **Comparison Results**
       - Once uploaded, the app shows a table comparing:
         - Column name  
         - Row count in both files  
         - Sum (for numeric columns)  
         - Status indicators:
            - 🟢✔ = Row count and sum match  
            - 🟡✔ = Only row count matches  
            - ❌ = Row count mismatch

    3. **Missing Columns**
       - Another table lists any columns missing in either file.

    4. **Editable Notes**
       - At the bottom, there’s a text box showing all columns with row count mismatches.
       - You can edit or copy this text for reporting or further analysis.
    """)
    # Close Help
    with st.form("close_help_form"):
        close_help = st.form_submit_button("❌ Close Help")
        if close_help:
            st.session_state.show_help = False
            st.rerun()
    # Footer
    st.markdown("<div class='footer'>BY - SOURAV THAKUR</div>", unsafe_allow_html=True)
    st.stop()  # Prevent main app from rendering

# MAIN APP BELOW
st.markdown("### 📁 Upload Files")

file1 = st.file_uploader("Upload First DDE File", type=None, key="dde")
file2 = st.file_uploader("Upload Second Taxtech File", type=None, key="taxtech")

if file1 and file2:
    try:
        df1 = pd.read_excel(file1) if file1.name.endswith(('.xls', '.xlsx')) else pd.read_csv(file1)
        df2 = pd.read_excel(file2) if file2.name.endswith(('.xls', '.xlsx')) else pd.read_csv(file2)

        st.markdown("### 🔍 Column Comparison")

        comparison_data = []
        all_columns = sorted(set(df1.columns) | set(df2.columns))

        row_count_file1 = len(df1)
        row_count_file2 = len(df2)

        for col in all_columns:
            count1 = df1[col].count() if col in df1 else "-"
            count2 = df2[col].count() if col in df2 else "-"

            sum1 = df1[col].sum() if col in df1 and pd.api.types.is_numeric_dtype(df1[col]) else "-"
            sum2 = df2[col].sum() if col in df2 and pd.api.types.is_numeric_dtype(df2[col]) else "-"

            status = "❌"
            if count1 == count2 and sum1 == sum2:
                status = "🟢✔"
            elif count1 == count2:
                status = "🟡✔"

            comparison_data.append({
                "Column Name": col,
                "DDE Count": count1,
                "Taxtech Count": count2,
                "DDE Sum": sum1,
                "Taxtech Sum": sum2,
                "Status": status
            })

        st.dataframe(pd.DataFrame(comparison_data))

        # MISSING COLUMNS SECTION
        st.markdown("### ❗ Columns Not Present in Both Files")
        missing_in_file1 = set(df2.columns) - set(df1.columns)
        missing_in_file2 = set(df1.columns) - set(df2.columns)

        max_len = max(len(missing_in_file1), len(missing_in_file2))
        missing_df = pd.DataFrame({
            "Missing in DDE File": list(missing_in_file1) + [""] * (max_len - len(missing_in_file1)),
            "Missing in Taxtech File": list(missing_in_file2) + [""] * (max_len - len(missing_in_file2))
        })
        st.dataframe(missing_df)

        # TEXT AREA FOR MISMATCHED ROW COUNTS
        mismatched_notes = ""
        for col in all_columns:
            count1 = df1[col].count() if col in df1 else "-"
            count2 = df2[col].count() if col in df2 else "-"
            if count1 != count2:
                mismatched_notes += f"Column '{col}': DDE File = {count1}, Taxtech File = {count2}\n"

        if mismatched_notes:
            st.markdown("### 📝 Notes (Editable)")
            st.text_area("Row count mismatches:", value=mismatched_notes, height=200)
        else:
            st.success("All column row counts match!")

    except Exception as e:
        st.error(f"Error processing files: {e}")

# Footer
st.markdown("<div class='footer'>BY - SOURAV THAKUR</div>", unsafe_allow_html=True)
