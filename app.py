import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

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


# إنشاء ملف PDF
def create_pdf(student):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    elements = []

    elements.append(
        Paragraph("Student Result", title_style)
    )

    data = [
        ["Information", "Value"],
        ["Student Name", str(student["Student_Name"])],
        ["Student ID", str(student["Student_ID"])],
        ["Result", str(student["Result"]).upper()]
    ]

    table = Table(
        data,
        colWidths=[180, 250]
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f232b")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 12),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ])
    )

    elements.append(table)

    document.build(elements)

    buffer.seek(0)

    return buffer


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

    # رسالة العثور على الطالب
    st.success("✅ تم العثور على الطالب بنجاح!")

    # بيانات الطالب
    st.markdown("### 👨‍🎓 بيانات الطالب")

    student_data = {
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
    }

    result_table = pd.DataFrame(student_data)

    st.table(result_table)

    # النتيجة النهائية
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

    # إنشاء PDF
    pdf_file = create_pdf(student)

    # زر تحميل PDF
    st.download_button(
        label="📄 تحميل النتيجة PDF",
        data=pdf_file,
        file_name=f"Student_Result_{student['Student_ID']}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
