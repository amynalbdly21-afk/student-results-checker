import streamlit as st
import pandas as pd

# Read the Excel file
df = pd.read_excel("Student_Results.xlsx")

# Page title
st.title("🎓 Student Results Checker")

st.write("Enter the student's university ID to check the result.")

# Student ID input
student_id = st.text_input("University ID")

# Search button
if st.button("🔍 Search Result"):

    if student_id.strip() == "":
        st.warning("Please enter a university ID.")

    else:
        # Convert input to the same format as Excel values
        try:
            student_id_value = int(student_id.strip())

            result = df[df["Student_ID"] == student_id_value]

            if not result.empty:
                st.success("Student found successfully!")

                # Display student information
                student = result.iloc[0]

                st.subheader("Student Information")

                st.write(f"**University ID:** {student['Student_ID']}")
                st.write(f"**Student Name:** {student['Student_Name']}")

                # Display the student's complete result
                st.subheader("📊 Student Result")

                st.dataframe(result, use_container_width=True)

            else:
                st.error("❌ University ID not found.")

        except ValueError:
            st.error("Please enter a valid university ID.")
