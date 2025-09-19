# 載入 Streamlit 函式庫
import streamlit as st

# 設定網頁標題
st.title('我的第一個 Streamlit 應用程式')

# 顯示文字
st.write('哈囉，這是 Streamlit！')
st.write('你可以在這個頁面展示資料、圖表和互動式介面。')

# 建立一個滑桿
x = st.slider('請選擇一個數字')
st.write('你選擇的數字是：', x)