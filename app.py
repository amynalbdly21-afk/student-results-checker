
import streamlit as st
import pandas as pd

# قراءة ملف النتائج
df = pd.read_excel("Student_Results.xlsx")

st.title("🏫 نظام الاستعلام عن نتائج الطلاب")
st.write("أدخل اسم الطالب ورقمه الجامعي للاستعلام عن النتيجة.")

student_name = st.text_input("اسم الطالب")
student_id = st.text_input("الرقم الجامعي")

if st.button("🔍 استعلام عن النتيجة"):

    # تنظيف البيانات قبل المقارنة
    names = df["Student_Name"].astype(str).str.strip()
    ids = df["Student_ID"].astype(str).str.strip()

    # البحث بالاسم والرقم
    result = df[
        (names == student_name.strip()) &
        (ids.str.replace(".0", "", regex=False) == student_id.strip())
    ]

    if not result.empty:

        student_result = str(result.iloc[0]["Result"]).strip()

        if student_result.lower() == "pass":
            st.success(f"✅ الطالب {student_name}: ناجح")
        elif student_result.lower() == "fail":
            st.error(f"❌ الطالب {student_name}: راسب")
        else:
            st.info(f"النتيجة: {student_result}")

    else:
        st.warning("⚠️ لم يتم العثور على طالب بهذه البيانات.")
