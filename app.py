import streamlit as st
import pandas as pd

# قراءة ملف النتائج
df = pd.read_excel("Student_Results.xlsx")


# حذف النتيجة عند تغيير أو مسح الرقم
def clear_result():
    st.session_state.result = None


# إنشاء متغير لحفظ نتيجة البحث
if "result" not in st.session_state:
    st.session_state.result = None


# عنوان الموقع
st.title("🎓 نظام الاستعلام عن نتائج الطلاب")

st.write("أدخل الرقم الجامعي ثم اضغط على زر الاستعلام.")


# إدخال الرقم الجامعي
student_id = st.text_input(
    "الرقم الجامعي",
    on_change=clear_result
)


# زر الاستعلام
if st.button("🔍 استعلام"):

    if student_id.strip() == "":
        st.warning("⚠️ يرجى إدخال الرقم الجامعي.")

    else:
        try:
            # تحويل الرقم إلى رقم صحيح
            student_id_value = int(student_id.strip())

            # البحث عن الطالب
            result = df[df["Student_ID"] == student_id_value]

            if not result.empty:
                # حفظ النتيجة
                st.session_state.result = result

            else:
                st.error("❌ الرقم الجامعي غير موجود.")

        except ValueError:
            st.error("⚠️ يرجى إدخال رقم جامعي صحيح.")


# عرض النتيجة المحفوظة
if st.session_state.result is not None:

    result = st.session_state.result
    student = result.iloc[0]

    st.success("✅ تم العثور على الطالب بنجاح!")

    st.subheader("👨‍🎓 بيانات الطالب")

    st.write(f"**الرقم الجامعي:** {student['Student_ID']}")
    st.write(f"**اسم الطالب:** {student['Student_Name']}")

    st.subheader("📊 نتيجة الطالب")

    st.dataframe(result, use_container_width=True)
