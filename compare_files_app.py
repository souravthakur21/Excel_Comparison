import streamlit as st
import pandas as pd

# Set Title
st.title("📊 Excel File Comparison Tool")

st.markdown("### Upload two Excel files for comparison:")

# Upload Files
file1 = st.file_uploader("Upload First File", type=["xlsx"])
file2 = st.file_uploader("Upload Second File", type=["xlsx"])

if file1 and file2:
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    if list(df1.columns) != list(df2.columns):
        st.error("⚠ Column names do not match. Please check your files!")
    else:
        results = []
        for col in df1.columns:
            count1, count2 = df1[col].count(), df2[col].count()
            
            # If column contains "ID" or "id", only count, no sum
            if "id" in col.lower():
                status = "🟡✔" if count1 == count2 else "❌"
                results.append((col, count1, count2, "-", "-", status))
            else:
                # Convert to numeric (ignore errors)
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
        
        # Display Results
        st.markdown("### 📊 Comparison Results:")
        st.table(pd.DataFrame(results, columns=["Column", "Count in File1", "Count in File2", "Sum in File1", "Sum in File2", "Status"]))
