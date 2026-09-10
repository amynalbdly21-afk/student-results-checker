import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(
    page_title="نظام نتائج الطلاب",
    page_icon="🎓",
    layout="centered"
)

# قراءة ملف النتائج
df = pd.read_excel("Student_Results.xlsx")

# حفظ آخر رقم تم الاستعلام عنه
if "searched_id" not in st.session_state:
    st.session_state.searched_id = None

# العنوان
st.title("🎓 نظام الاستعلام عن نتائج الطلاب")

st.write("أدخل الرقم الجامعي ثم اضغط على زر الاستعلام.")

# إدخال الرقم الجامعي
student_id = st.text_input("🆔 الرقم الجامعي")

# زر الاستعلام
if st.button("🔍 استعلام", use_container_width=True):

    if student_id.strip() == "":
        st.warning("⚠️ يرجى إدخال الرقم الجامعي.")
        st.session_state.searched_id = None

    else:
        try:
            student_id_value = int(student_id.strip())

            # البحث عن الطالب
            result = df[df["Student_ID"] == student_id_value]

            if not result.empty:
                st.session_state.searched_id = student_id_value
            else:
                st.error("❌ الرقم الجامعي غير موجود.")
                st.session_state.searched_id = None

        except ValueError:
            st.error("⚠️ يرجى إدخال رقم جامعي صحيح.")
            st.session_state.searched_id = None


# عرض النتيجة
if (
    st.session_state.searched_id is not None
    and student_id.strip().isdigit()
    and int(student_id.strip()) == st.session_state.searched_id
):

    result = df[df["Student_ID"] == st.session_state.searched_id]
    student = result.iloc[0]

    st.success("✅ تم العثور على الطالب بنجاح!")

    # بيانات الطالب
    st.subheader("👨‍🎓 بيانات الطالب")

    st.write(f"**اسم الطالب:** {student['Student_Name']}")
    st.write(f"**الرقم الجامعي:** {student['Student_ID']}")

    # النتيجة
    st.subheader("📊 النتيجة")

    if student["Result"] == "Pass":
        st.success("🎉 PASS — ناجح")
    else:
        st.error("❌ FAIL — راسب")
