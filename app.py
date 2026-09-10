
import streamlit as st
import pandas as pd

df = pd.read_excel("Student_Results.xlsx")

st.title("🏫 نظام الاستعلام عن نتائج الطلاب")

# عرض بيانات الملف للتأكد من وصول الموقع إليها
st.write("أسماء الأعمدة:")
st.write(df.columns.tolist())

st.write("أول 5 سجلات:")
st.dataframe(df.head())

student_name = st.text_input("اسم الطالب")
student_id = st.text_input("الرقم الجامعي")

if st.button("🔍 استعلام عن النتيجة"):

    name = student_name.strip()
    sid = student_id.strip()

    result = df[
        (df["Student_Name"].astype(str).str.strip() == name) &
        (df["Student_ID"].astype(str).str.replace(".0", "", regex=False).str.strip() == sid)
    ]

    if not result.empty:
        student_result = str(result.iloc[0]["Result"]).strip()

        if student_result.lower() == "pass":
            st.success("✅ النتيجة: ناجح")
        else:
            st.error("❌ النتيجة: راسب")
    else:
        st.warning("⚠️ لم يتم العثور على طالب بهذه البيانات.")
