import streamlit as st
from utils import parse_pdf, calculate_credits

st.set_page_config(page_title="學分查詢系統", layout="centered")

st.title("📘 學生總學分查詢系統")

uploaded_file = st.file_uploader("請上傳課程成績 PDF", type="pdf")
if uploaded_file:
    try:
        df = parse_pdf(uploaded_file)
        result = calculate_credits(df)
        
        st.success(f"✅ 已通過學分總數：{result['total_passed_credits']} 學分")
        st.info(f"📉 目前尚缺 {128 - result['total_passed_credits']} 學分（畢業門檻為 128 學分）")
        
        if not result["failed_courses"].empty:
            st.error("❌ 不通過課程：")
            st.dataframe(result["failed_courses"])
        
        if not result["zero_credit_courses"].empty:
            st.warning("⚠️ 學分為 0 的課程：")
            st.dataframe(result["zero_credit_courses"])
        
    except Exception as e:
        st.error(f"解析失敗：{e}")
