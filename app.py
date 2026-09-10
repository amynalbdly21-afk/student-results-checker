
import streamlit as st
import pandas as pd

# قراءة ملف النتائج
file_path = "Student_Results.xlsx"
df = pd.read_excel(file_path)

# عنوان الموقع
st.title("🏫 نظام الاستعلام عن نتائج الطلاب")
st.write("أدخل اسم الطالب ورقمه الجامعي للاستعلام عن النتيجة.")

# خانات الإدخال
student_name = st.text_input("اسم الطالب")
student_id = st.text_input("الرقم الجامعي")

# زر الاستعلام
if st.button("🔍 استعلام عن النتيجة"):

    result = df[
        (df["Student_Name"].astype(str).str.strip() == student_name.strip()) &
        (df["Student_ID"].astype(str).str.strip() == student_id.strip())
    ]

    if not result.empty:
        student_result = result.iloc[0]["Result"]

        st.success(f"الطالب: {student_name}")

        if student_result == "Pass":
            st.success("✅ النتيجة: ناجح")
        else:
            st.error("❌ النتيجة: راسب")

    else:
        st.warning("⚠️ لم يتم العثور على طالب بهذه البيانات.")
