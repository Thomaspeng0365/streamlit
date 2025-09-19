import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_iris

# 設定頁面標題
st.set_page_config(page_title="互動式機器學習應用", layout="wide")

st.title("鳶尾花分類器 🌸")
st.markdown("使用左側欄調整模型參數，並在右側欄輸入新數據進行預測。")

# --- 數據載入 ---
@st.cache_data
def load_data():
    """載入鳶尾花數據集並轉換為 DataFrame"""
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    df['target_names'] = pd.Series(iris.target).map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})
    return df, iris.target_names

df, target_names = load_data()

# --- 側邊欄：模型參數調整 ---
st.sidebar.header('模型參數調整')
n_estimators = st.sidebar.slider(
    '樹的數量 (n_estimators)', 1, 100, 10,
    help="隨機森林模型中決策樹的數量。值越大，模型通常越精準，但訓練時間越長。"
)
max_depth = st.sidebar.slider(
    '樹的最大深度 (max_depth)', 1, 20, 5,
    help="決策樹的最大深度。控制模型複雜度，避免過度擬合 (Overfitting)。"
)

# --- 數據集分割與模型訓練 ---
X = df.drop(['target', 'target_names'], axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

@st.cache_resource
def train_model(n_estimators, max_depth):
    """訓練隨機森林模型並快取"""
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)
    return model

model = train_model(n_estimators, max_depth)

# --- 主內容：模型評估 ---
st.subheader('模型評估')

# 進行預測
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

st.success(f"模型精準度：**{accuracy:.2f}**")

st.info("改變左側欄的參數，可以觀察模型精準度的變化！")

# --- 數據輸入與預測 ---
st.markdown("---")
st.subheader('輸入數據進行預測')

# 建立四個輸入滑桿
col1, col2 = st.columns(2)
with col1:
    sepal_length = st.slider("花萼長度 (cm)", float(X['sepal length (cm)'].min()), float(X['sepal length (cm)'].max()), 5.4)
    sepal_width = st.slider("花萼寬度 (cm)", float(X['sepal width (cm)'].min()), float(X['sepal width (cm)'].max()), 3.4)
with col2:
    petal_length = st.slider("花瓣長度 (cm)", float(X['petal length (cm)'].min()), float(X['petal length (cm)'].max()), 1.3)
    petal_width = st.slider("花瓣寬度 (cm)", float(X['petal width (cm)'].min()), float(X['petal width (cm)'].max()), 0.2)

# 整理輸入數據
new_data = pd.DataFrame([[sepal_length, sepal_width, petal_length, petal_width]],
                       columns=['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)'])

# 進行預測
prediction = model.predict(new_data)
predicted_class = target_names[prediction[0]]

st.markdown("---")
st.success(f"根據您的輸入，模型預測該花為：**{predicted_class}**")
