import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 設定頁面標題和佈局
st.set_page_config(
    page_title="酷炫客戶互動儀表板",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 儀表板數據生成 ---
@st.cache_data
def generate_data():
    """生成虛擬客戶數據，並快取以提高效能"""
    np.random.seed(42)
    data = {
        '客戶ID': range(1, 1001),
        '年齡': np.random.randint(18, 65, 1000),
        '性別': np.random.choice(['男', '女', '未知'], 1000, p=[0.45, 0.45, 0.1]),
        '地區': np.random.choice(['北部', '中部', '南部', '東部'], 1000, p=[0.5, 0.2, 0.2, 0.1]),
        '購買金額': np.random.randint(100, 10000, 1000),
        '購買日期': pd.to_datetime(pd.date_range('2023-01-01', periods=1000, freq='D'))
    }
    return pd.DataFrame(data)

df = generate_data()

# --- 側邊欄篩選器 ---
st.sidebar.header('數據篩選')

# 年齡滑桿
min_age, max_age = st.sidebar.slider(
    '選擇年齡區間',
    int(df['年齡'].min()),
    int(df['年齡'].max()),
    (int(df['年齡'].min()), int(df['年齡'].max()))
)

# 性別多選框
selected_genders = st.sidebar.multiselect(
    '選擇性別',
    options=df['性別'].unique(),
    default=df['性別'].unique()
)

# 地區下拉選單
selected_region = st.sidebar.selectbox(
    '選擇地區',
    options=['全部'] + list(df['地區'].unique())
)

# 根據篩選條件過濾數據
filtered_df = df[(df['年齡'] >= min_age) & (df['年齡'] <= max_age)]
if selected_genders:
    filtered_df = filtered_df[filtered_df['性別'].isin(selected_genders)]
if selected_region != '全部':
    filtered_df = filtered_df[filtered_df['地區'] == selected_region]

# --- 儀表板主內容 ---
st.title("客戶數據互動儀表板 📊")
st.markdown("使用左側欄的篩選器來探索數據！")

if filtered_df.empty:
    st.warning("沒有符合篩選條件的數據，請調整篩選器。")
else:
    # --- 儀表板卡片 (KPI) ---
    total_sales = int(filtered_df['購買金額'].sum())
    average_age = int(filtered_df['年齡'].mean())
    customer_count = filtered_df.shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**總購買金額**\n\n$ {total_sales:,}", icon="💰")
    with col2:
        st.info(f"**平均客戶年齡**\n\n{average_age} 歲", icon="👤")
    with col3:
        st.info(f"**總客戶數**\n\n{customer_count} 人", icon="👥")
    
    st.markdown("---")
    
    # --- 圖表區塊 ---
    st.subheader('數據可視化')
    
    # 購買金額直方圖 (Histogram)
    fig_hist = px.histogram(
        filtered_df,
        x='購買金額',
        nbins=50,
        title='購買金額分佈',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # 年齡與購買金額散點圖 (Scatter Plot)
    fig_scatter = px.scatter(
        filtered_df,
        x='年齡',
        y='購買金額',
        color='性別',
        hover_name='客戶ID',
        title='年齡與購買金額關係',
        color_discrete_map={'男': 'blue', '女': 'pink', '未知': 'gray'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # 地區銷售圓餅圖 (Pie Chart)
    sales_by_region = filtered_df.groupby('地區')['購買金額'].sum().reset_index()
    fig_pie = px.pie(
        sales_by_region,
        values='購買金額',
        names='地區',
        title='各地區總購買金額',
        hole=0.3
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # --- 原始數據區塊 ---
    st.markdown("---")
    st.subheader('原始數據預覽')
    st.dataframe(filtered_df.head(10))
