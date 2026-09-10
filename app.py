import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(
    page_title="Student Results Checker",
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

# خانة الرقم الجامعي
student_id = st.text_input(
    "🆔 الرقم الجامعي",
    placeholder="مثال: 1003"
)

# إذا تم مسح الرقم
if student_id.strip() == "":
    st.session_state.searched_id = None

# زر الاستعلام
if st.button("🔍 استعلام", use_container_width=True):

    if student_id.strip() == "":
        st.warning("⚠️ يرجى إدخال الرقم الجامعي.")
        st.session_state.searched_id = None

    else:
        try:
            # تحويل الرقم إلى رقم صحيح
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
    student_id.strip() != ""
    and st.session_state.searched_id is not None
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

    result_value = str(student["Result"]).strip()

    if result_value.lower() == "pass":

        st.success("🎉 PASS — ناجح")

    elif result_value.lower() == "fail":

        st.error("❌ FAIL — راسب")

    else:

        st.info(f"📋 النتيجة: {result_value}")
