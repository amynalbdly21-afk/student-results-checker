import streamlit as st
import pandas as pd

# قراءة ملف النتائج
df = pd.read_excel("Student_Results.xlsx")

# عنوان الموقع
st.title("🎓 نظام الاستعلام عن نتائج الطلاب")

st.write("أدخل الرقم الجامعي للطالب ثم اضغط على زر الاستعلام.")

# إدخال الرقم الجامعي
student_id = st.text_input("الرقم الجامعي")

# زر الاستعلام
search_clicked = st.button("🔍 استعلام")

# إذا تم الضغط على زر الاستعلام
if search_clicked:

    if student_id.strip() == "":
        st.warning("⚠️ يرجى إدخال الرقم الجامعي.")

    else:
        try:
            # تحويل الرقم إلى رقم صحيح
            student_id_value = int(student_id.strip())

            # البحث عن الطالب
            result = df[df["Student_ID"] == student_id_value]

            if not result.empty:
                st.success("✅ تم العثور على الطالب بنجاح!")

                student = result.iloc[0]

                st.subheader("👨‍🎓 بيانات الطالب")

                st.write(f"**الرقم الجامعي:** {student['Student_ID']}")
                st.write(f"**اسم الطالب:** {student['Student_Name']}")

                st.subheader("📊 نتيجة الطالب")

                st.dataframe(result, use_container_width=True)

            else:
                st.error("❌ الرقم الجامعي غير موجود.")

        except ValueError:
            st.error("⚠️ يرجى إدخال رقم جامعي صحيح.")
