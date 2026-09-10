import streamlit as st
import pandas as pd
import unicodedata

# قراءة ملف النتائج
df = pd.read_excel("Student_Results.xlsx")

st.title("🏫 نظام الاستعلام عن نتائج الطلاب")
st.write("أدخل اسم الطالب ورقمه الجامعي للاستعلام عن النتيجة.")

student_name = st.text_input("اسم الطالب")
student_id = st.text_input("الرقم الجامعي")


def clean_text(text):
    text = str(text)
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u200f", "").replace("\u200e", "")
    text = " ".join(text.split())
    return text.strip()


if st.button("🔍 استعلام عن النتيجة"):

    input_name = clean_text(student_name)
    input_id = clean_text(student_id)

    names = df["Student_Name"].apply(clean_text)
    ids = df["Student_ID"].apply(clean_text)

    result = df[
        (names == input_name) &
        (ids == input_id)
    ]

    if not result.empty:

        student_result = clean_text(result.iloc[0]["Result"])

        if student_result.lower() == "pass":
            st.success(f"✅ الطالب: {student_name}")
            st.success("النتيجة: ناجح")

        elif student_result.lower() == "fail":
            st.success(f"✅ الطالب: {student_name}")
            st.error("النتيجة: راسب")

    else:
        st.warning("⚠️ لم يتم العثور على طالب بهذه البيانات.")
