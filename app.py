import streamlit as st
import pandas as pd

# قراءة ملف النتائج
df = pd.read_excel("Student_Results.xlsx")

# حفظ آخر رقم تم الاستعلام عنه
if "searched_id" not in st.session_state:
    st.session_state.searched_id = None

# عنوان الموقع
st.title("🎓 نظام الاستعلام عن نتائج الطلاب")

st.write("أدخل الرقم الجامعي ثم اضغط على زر الاستعلام.")

# خانة الرقم الجامعي
student_id = st.text_input("الرقم الجامعي")

# إذا تم مسح الرقم، يتم حذف نتيجة البحث
if student_id.strip() == "":
    st.session_state.searched_id = None

# زر الاستعلام
if st.button("🔍 استعلام"):

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
                # حفظ الرقم الذي تم الاستعلام عنه
                st.session_state.searched_id = student_id_value

            else:
                st.error("❌ الرقم الجامعي غير موجود.")
                st.session_state.searched_id = None

        except ValueError:
            st.error("⚠️ يرجى إدخال رقم جامعي صحيح.")
            st.session_state.searched_id = None


# عرض النتيجة فقط إذا كان الرقم موجودًا
# وهو نفس الرقم الذي تم الاستعلام عنه
if (
    student_id.strip() != ""
    and st.session_state.searched_id is not None
    and student_id.strip().isdigit()
    and int(student_id.strip()) == st.session_state.searched_id
):

    result = df[df["Student_ID"] == st.session_state.searched_id]
    student = result.iloc[0]

    st.success("✅ تم العثور على الطالب بنجاح!")

    st.subheader("👨‍🎓 بيانات الطالب")

    st.write(f"**الرقم الجامعي:** {student['Student_ID']}")
    st.write(f"**اسم الطالب:** {student['Student_Name']}")

    st.subheader("📊 نتيجة الطالب")

    st.dataframe(result, use_container_width=True)
