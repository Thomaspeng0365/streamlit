import streamlit as st
import random
import time

def select_winner(participants):
    """從參與者名單中隨機選出一位中獎者。"""
    if not participants:
        return None
    return random.choice(participants)

def main():
    st.title("線上抽獎小工具")
    st.markdown("---")
    
    # 讓使用者輸入參與者名單
    st.markdown("### 請輸入所有參與抽獎的人名")
    st.markdown("請在下方輸入名單，每個名字用逗號分隔（例如：小明,小華,小白）")

    participants_input = st.text_area("參與者名單", height=150)
    
    # 將輸入的字串轉換成列表，並移除多餘的空白
    participants = [name.strip() for name in participants_input.split(',') if name.strip()]

    # 抽獎按鈕
    if st.button("開始抽獎！"):
        if not participants:
            st.warning("請輸入至少一位參與者！")
        else:
            st.info(f"本次抽獎的參與者共有 {len(participants)} 位：\n{', '.join(participants)}")
            
            # 模擬抽獎過程，增加互動性
            with st.spinner('幸運兒正在產生中...'):
                time.sleep(3)
            
            # 隨機選出一位中獎者
            winner = select_winner(participants)
            
            st.balloons()  # 顯示氣球動畫
            st.success("🎉🎉🎉")
            st.success(f"恭喜！本次的幸運兒是： **{winner}**")
            st.success("🎉🎉🎉")

if __name__ == "__main__":
    main()
