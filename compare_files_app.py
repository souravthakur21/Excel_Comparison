import streamlit as st
import pandas as pd
import os

def convert_to_excel(file):
    """Convert CSV to DataFrame."""
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error converting CSV to DataFrame: {e}")
        return None

# Set Streamlit to use Render's assigned port
port = os.getenv("PORT", 8501)
st.set_page_config(page_title="Compare Files App", layout="wide")

# Set Title
st.title(":bar_chart: File Comparison Tool (Excel & CSV)")
st.markdown("### Upload two files for comparison (Excel or CSV):")

# Upload Files
file1 = st.file_uploader("Upload First File", type=["xlsx", "csv"])
file2 = st.file_uploader("Upload Second File", type=["xlsx", "csv"])

if file1 and file2:
    # Convert CSV to DataFrame if needed
    ext1 = os.path.splitext(file1.name)[-1].lower()
    ext2 = os.path.splitext(file2.name)[-1].lower()
    
    df1 = convert_to_excel(file1) if ext1 == ".csv" else pd.read_excel(file1)
    df2 = convert_to_excel(file2) if ext2 == ".csv" else pd.read_excel(file2)

    # Proceed if files were successfully loaded
    if df1 is not None and df2 is not None:
        common_columns = set(df1.columns) & set(df2.columns)
        
        results = []
        for col in common_columns:
            count1, count2 = df1[col].count(), df2[col].count()
            
            if "id" in col.lower():
                status = "🟡✔" if count1 == count2 else "❌"
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
                    
                results.append((col, count1, count2, f"{sum1:.2f}", f"{sum2:.2f}", status))
        
        # Display Comparison Results
        st.markdown("### 📊 Comparison Results:")
        st.table(pd.DataFrame(results, columns=["Column", "Count in File1", "Count in File2", "Sum in File1", "Sum in File2", "Status"]))
        
        # Identify missing columns
        missing_in_file1 = list(set(df2.columns) - set(df1.columns))
        missing_in_file2 = list(set(df1.columns) - set(df2.columns))

        if missing_in_file1 or missing_in_file2:
            st.markdown("### ⚠ Columns Not Present in Both Files:")

            # Pad the shorter list with "-"
            max_len = max(len(missing_in_file1), len(missing_in_file2))
            missing_in_file1 += ["-"] * (max_len - len(missing_in_file1))
            missing_in_file2 += ["-"] * (max_len - len(missing_in_file2))

            # Create the DataFrame
            missing_df = pd.DataFrame({
                f"Missing in {file1.name}": missing_in_file1,
                f"Missing in {file2.name}": missing_in_file2
            })

            st.table(missing_df)
