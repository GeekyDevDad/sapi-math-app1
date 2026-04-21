import streamlit as st
import random

def generate_wasazan():
    """和差算の数値替え問題を生成する"""
    # 差は2の倍数、合計は差より大きく、かつ合計+差が偶数になるように調整
    diff = random.randrange(4, 30, 2)
    total = random.randint(diff + 20, 150)
    
    # 答えが整数になるための調整
    if (total + diff) % 2 != 0:
        total += 1
        
    larger = (total + diff) // 2
    smaller = total - larger
    
    return total, diff, larger, smaller

st.set_page_config(page_title="Geeky.a.Dad's Math Lab", page_icon="🔢")
st.title("🔢 算数数値替えドリル：和差算")
st.write("「答えを覚える」のは今日でおしまい。本質を理解するための初見問題生成ツール。")

if 'q_data' not in st.session_state:
    st.session_state.q_data = generate_wasazan()

total, diff, larger, smaller = st.session_state.q_data

st.subheader("【問題】")
st.info(f"A君とB君が持っているカードの合計は {total} 枚です。A君はB君より {diff} 枚多く持っています。A君は何枚持っていますか？")

if st.button("解答を表示"):
    st.success(f"式：({total} + {diff}) ÷ 2 = {larger}\n\n答え：{larger} 枚")
    if st.button("次の問題へ"):
        st.session_state.q_data = generate_wasazan()
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("### Geeky.a.Dad's Status")
st.write("私立小・サピックス・サッカー三昧の合間に。ラザニアの層を重ねるように、知識の層を積み上げよう。")
