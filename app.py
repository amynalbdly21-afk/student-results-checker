import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(
    page_title="نتائج الطلاب",
    page_icon="🎓",
    layout="centered"
)

# تنسيق الواجهة
st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

.student-card {
    padding: 22px;
    border-radius: 15px;
    background-color: #1f232b;
    border: 1px solid #343943;
    margin-top: 15px;
}

.result-pass {
    padding: 18px;
    border-radius: 12px;
    background-color: #123d2b;
    color: #5cff9d;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    margin-top: 15px;
}

.result-fail {
    padding: 18px;
    border-radius: 12px;
    background-color: #45252b;
    color: #ff7b86;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    margin-top: 15px;
}

</style>
""", unsafe_allow_html=True)


# قراءة ملف النتائج
df = pd.read_excel("Student_Results.xlsx")


# حفظ آخر رقم تم الاستعلام عنه
if "searched_id" not in st.session_state:
    st.session_state.searched_id = None


# العنوان
st.markdown(
    '<div class="main-title">🎓 نظام الاستعلام عن نتائج الطلاب</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">أدخل الرقم الجامعي ثم اضغط على زر الاستعلام</div>',
    unsafe_allow_html=True
)


# إدخال الرقم الجامعي
student_id = st.text_input(
    "🆔 الرقم الجامعي",
    placeholder="مثال: 1001"
)


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

    # رسالة النجاح
    st.success("✅ تم العثور على الطالب بنجاح!")

    # بطاقة بيانات الطالب
    st.markdown(
        '<div class="student-card">',
        unsafe_allow_html=True
    )

    st.markdown("### 👨‍🎓 بيانات الطالب")

    st.write(f"**اسم الطالب:** {student['Student_Name']}")
    st.write(f"**الرقم الجامعي:** {student['Student_ID']}")

    st.markdown("</div>", unsafe_allow_html=True)

    # النتيجة
    st.markdown("### 📊 النتيجة")

    if str(student["Result"]).strip().lower() == "pass":

        # 🎈 احتفال عند النجاح
        st.balloons()

        st.markdown(
            '<div class="result-pass">🎉 PASS — ناجح 🎉</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="result-fail">❌ FAIL — راسب</div>',
            unsafe_allow_html=True
        )
