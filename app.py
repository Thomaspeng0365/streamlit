import streamlit as st
import random
import time

def main():
    st.title("線上抽獎小工具")

    st.markdown("---")

    st.write("請輸入所有參與抽獎的人名，每個名字用逗號分隔：")
    names_input = st.text_area("參與者名單（例如：小明,小華,小白）", height=100)
    
    participants = [name.strip() for name in names_input.split(',') if name.strip()]

    if st.button("開始抽獎！"):
        if not participants:
            st.warning("請輸入至少一位參與者！")
        else:
            st.info(f"本次抽獎的參與者共有 {len(participants)} 位：\n{', '.join(participants)}")
            
            # 模擬抽獎過程
            with st.spinner('幸運兒正在產生中...'):
                time.sleep(3)
            
            winner = random.choice(participants)
            
            st.balloons()  # 顯示氣球動畫
            st.success("🎉🎉🎉")
            st.success(f"恭喜！本次的幸運兒是： **{winner}**")
            st.success("🎉🎉🎉")

if __name__ == "__main__":
    main()
