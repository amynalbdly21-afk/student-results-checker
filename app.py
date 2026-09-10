import streamlit as st
import pandas as pd

df = pd.read_excel("Student_Results.xlsx")

st.title("فحص بيانات الطلاب")

st.write("بيانات الملف كما يقرأها الموقع:")
st.dataframe(df)

st.write("القيم الفعلية للرقم الجامعي:")
for x in df["Student_ID"]:
    st.write(repr(x))

st.write("القيم الفعلية للأسماء:")
for x in df["Student_Name"]:
    st.write(repr(x))
