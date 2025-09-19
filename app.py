import streamlit as st
import pymssql
import pandas as pd
import matplotlib.pyplot as plt

# 確保你的 secrets.toml 中有這些憑證
# 在 Streamlit Cloud 部署時，會自動讀取
@st.cache_resource
def get_connection():
    return pymssql.connect(
        server=st.secrets["sql_server"]["server"],
        user=st.secrets["sql_server"]["username"],
        password=st.secrets["sql_server"]["password"],
        database=st.secrets["sql_server"]["database"]
    )

@st.cache_data
def load_data():
    conn = get_connection()
    query = "SELECT DonateAmountTwd FROM PrDonateForm;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title('捐款金額分佈圖')

# 載入資料
try:
    df = load_data()
    
    if not df.empty:
        # 清理資料：移除無效值，確保是數字
        df['DonateAmountTwd'] = pd.to_numeric(df['DonateAmountTwd'], errors='coerce').dropna()
        
        if not df.empty:
            st.write('### 捐款金額（新台幣）分佈')
            
            # 建立直方圖
            fig, ax = plt.subplots()
            ax.hist(df['DonateAmountTwd'], bins=20, edgecolor='black')
            ax.set_title('捐款金額直方圖')
            ax.set_xlabel('金額')
            ax.set_ylabel('筆數')
            
            # 在 Streamlit 中顯示圖表
            st.pyplot(fig)
            
            # 顯示一些統計資訊
            st.write('### 統計資訊')
            st.write(df['DonateAmountTwd'].describe())
        else:
            st.error("資料庫中沒有有效的捐款金額資料。")
    else:
        st.warning("PrDonateForm 表格中沒有任何資料。")

except Exception as e:
    st.error(f"無法連接到資料庫或讀取資料：{e}")