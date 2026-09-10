import streamlit as st
import pandas as pd

# قراءة ملف النتائج من نفس مجلد المشروع
df = pd.read_excel("Student_Results.xlsx")

st.title("🏫 نظام الاستعلام عن نتائج الطلاب")
st.write("أدخل اسم الطالب ورقمه الجامعي للاستعلام عن النتيجة.")

student_name = st.text_input("اسم الطالب")
student_id = st.text_input("الرقم الجامعي")

if st.button("🔍 استعلام عن النتيجة"):

    result = df[
        (df["Student_Name"].astype(str).str.strip() == student_name.strip()) &
        (df["Student_ID"].astype(str).str.strip() == student_id.strip())
    ]

    if not result.empty:

        student_result = str(result.iloc[0]["Result"]).strip()

        st.success(f"الطالب: {student_name}")

        if student_result.lower() == "pass":
            st.success("✅ النتيجة: ناجح")
        else:
            st.error("❌ النتيجة: راسب")

    else:
        st.warning("⚠️ لم يتم العثور على طالب بهذه البيانات.")
