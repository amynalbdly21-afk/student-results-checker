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

# حفظ حالة دخول الإدارة
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False


# العنوان الرئيسي
st.markdown(
    '<div class="main-title">🎓 نظام الاستعلام عن نتائج الطلاب</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">أدخل الرقم الجامعي ثم اضغط على زر الاستعلام</div>',
    unsafe_allow_html=True
)


# إنشاء التبويبات
tab1, tab2 = st.tabs([
    "🔎 استعلام النتائج",
    "🔐 لوحة الإدارة"
])


# ==================================================
# استعلام النتائج
# ==================================================

with tab1:

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


    # عرض بيانات الطالب
    if (
        st.session_state.searched_id is not None
        and student_id.strip().isdigit()
        and int(student_id.strip()) == st.session_state.searched_id
    ):

        result = df[df["Student_ID"] == st.session_state.searched_id]
        student = result.iloc[0]

        # رسالة النجاح
        st.success("✅ تم العثور على الطالب بنجاح!")

        # عنوان البيانات
        st.markdown("### 👨‍🎓 بيانات الطالب")

        # جدول بيانات الطالب
        student_data = pd.DataFrame({
            "البيان": [
                "اسم الطالب",
                "الرقم الجامعي",
                "النتيجة"
            ],
            "المعلومات": [
                str(student["Student_Name"]),
                str(student["Student_ID"]),
                str(student["Result"]).upper()
            ]
        })

        st.table(student_data)

        # النتيجة النهائية
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


# ==================================================
# لوحة الإدارة
# ==================================================

with tab2:

    # عنوان صغير وأنيق
    st.markdown(
        '<div style="font-size:22px; font-weight:bold; margin-bottom:15px;">'
        '🔐 دخول الإدارة'
        '</div>',
        unsafe_allow_html=True
    )

    # كلمة المرور
    password = st.text_input(
        "🔑 كلمة مرور الإدارة",
        type="password"
    )

    # زر الدخول
    if st.button("🔓 دخول", use_container_width=True):

        if password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.admin_logged_in = True
        else:
            st.session_state.admin_logged_in = False
            st.error("❌ كلمة المرور غير صحيحة.")


    # إذا تم تسجيل الدخول
    if st.session_state.get("admin_logged_in", False):

        st.success("✅ تم تسجيل الدخول بنجاح")

        # عنوان الإحصائيات بحجم أصغر
        st.markdown(
            '<div style="font-size:24px; font-weight:bold; '
            'margin-top:15px; margin-bottom:20px;">'
            '📊 إحصائيات الطلاب'
            '</div>',
            unsafe_allow_html=True
        )

        # حساب الإحصائيات
        total_students = len(df)

        passed = (
            df["Result"]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("pass")
            .sum()
        )

        failed = total_students - passed

        pass_rate = (
            passed / total_students * 100
            if total_students > 0 else 0
        )

        fail_rate = (
            failed / total_students * 100
            if total_students > 0 else 0
        )


        # عرض الإحصائيات
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "👨‍🎓 إجمالي الطلاب",
                total_students
            )

        with col2:
            st.metric(
                "✅ الناجحون",
                passed
            )


        col3, col4 = st.columns(2)

        with col3:
            st.metric(
                "❌ الراسبون",
                failed
            )

        with col4:
            st.metric(
                "📈 نسبة النجاح",
                f"{pass_rate:.1f}%"
            )


        st.markdown("---")


        # نسبة الرسوب
        st.metric(
            "📉 نسبة الرسوب",
            f"{fail_rate:.1f}%"
        )


        # الرسم البياني
        st.markdown(
            '<div style="font-size:20px; font-weight:bold; '
            'margin-top:20px; margin-bottom:10px;">'
            '📊 توزيع النتائج'
            '</div>',
            unsafe_allow_html=True
        )

        chart_data = pd.DataFrame({
            "النتيجة": ["ناجح", "راسب"],
            "العدد": [passed, failed]
        })

        st.bar_chart(
            chart_data.set_index("النتيجة")
        )


        # تسجيل الخروج
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.admin_logged_in = False
            st.rerun()
