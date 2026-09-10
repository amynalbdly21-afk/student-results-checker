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

/* خلفية الصفحة */
.stApp {
    background-color: white;
    color: #222222;
}

/* العنوان */
.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    margin-bottom: 10px;
    color: #222222;
}

/* الوصف */
.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
    color: #555555;
}

/* بطاقة الطالب */
.student-card {
    padding: 22px;
    border-radius: 15px;
    background-color: #f8f9fa;
    border: 1px solid #dddddd;
    margin-top: 15px;
}

/* نتيجة النجاح */
.result-pass {
    padding: 18px;
    border-radius: 12px;
    background-color: #e8f8ef;
    color: #16834b;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    margin-top: 15px;
}

/* نتيجة الرسوب */
.result-fail {
    padding: 18px;
    border-radius: 12px;
    background-color: #fdebed;
    color: #d33b4b;
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

        # 🎈 احتفال بالنجاح
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
