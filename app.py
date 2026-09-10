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

.block-container {
    max-width: 650px;
    padding-top: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* العنوان الرئيسي */
.main-title {
    text-align: center;
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 6px;
    line-height: 1.4;
}

/* الوصف */
.subtitle {
    text-align: center;
    font-size: 16px;
    opacity: 0.75;
    margin-bottom: 24px;
}

/* بطاقة الطالب */
.student-card {
    padding: 18px;
    border-radius: 14px;
    background-color: #1f232b;
    border: 1px solid #343943;
    margin-top: 12px;
    margin-bottom: 18px;
}

/* عنوان بيانات الطالب */
.student-card h3 {
    margin-top: 0;
    margin-bottom: 16px;
    font-size: 20px;
}

/* نتيجة النجاح */
.result-pass {
    padding: 16px;
    border-radius: 12px;
    background-color: #123d2b;
    color: #5cff9d;
    text-align: center;
    font-size: 21px;
    font-weight: 700;
    margin-top: 10px;
}

/* نتيجة الرسوب */
.result-fail {
    padding: 16px;
    border-radius: 12px;
    background-color: #45252b;
    color: #ff7b86;
    text-align: center;
    font-size: 21px;
    font-weight: 700;
    margin-top: 10px;
}

/* تحسين الهاتف */
@media (max-width: 600px) {

    .block-container {
        padding-top: 1.2rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    .main-title {
        font-size: 25px;
    }

    .subtitle {
        font-size: 14px;
        margin-bottom: 20px;
    }

    .student-card {
        padding: 15px;
    }

    .result-pass,
    .result-fail {
        font-size: 19px;
        padding: 14px;
    }
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

        st.markdown(
            '<div class="result-pass">✅ PASS — ناجح</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="result-fail">❌ FAIL — راسب</div>',
            unsafe_allow_html=True
)
