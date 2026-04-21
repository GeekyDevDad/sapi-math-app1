import streamlit as st
import random

def generate_wasazan_3():
    # 3人の差をランダムに設定
    diff_ab = random.randint(5, 30)
    diff_bc = random.randint(5, 30)
    
    # 一番少ない人を基準（Cとする）にして、AとBの値を決める
    base = random.randint(20, 100)
    c = base
    b = c + diff_bc
    a = b + diff_ab
    
    total = a + b + c
    return total, diff_ab, diff_bc, a, b, c

st.set_page_config(page_title="Geeky.a.Dad's Math Lab", page_icon="🔢")
st.title("🔢 算数数値替え：和差算（3人Ver.）")
st.write("「線分図」をマスターするための3人パターン。")

if 'q_data_3' not in st.session_state:
    st.session_state.q_data_3 = generate_wasazan_3()

total, d_ab, d_bc, a, b, c = st.session_state.q_data_3

st.subheader("【問題】")
st.info(f"""
A、B、Cの3人が持っているカードを合わせると全部で **{total}枚** です。
・A君はB君より **{d_ab}枚** 多いです。
・B君はC君より **{d_bc}枚** 多いです。
このとき、A君は何枚持っていますか？
""")

if st.button("解答と線分図のヒントを表示"):
    st.success(f"""
**【考え方：一番少ないCに合わせる】**
1. 全体から「はみ出している分」を引きます。
   - BがCより多い分：{d_bc}枚
   - AがCより多い分：{d_bc} + {d_ab} = {d_bc + d_ab}枚
2. 全体 {total} - ({d_bc} + {d_bc + d_ab}) = {total - (d_bc + d_bc + d_ab)}枚
3. これが「Cの3倍」なので、 {total - (d_bc + d_bc + d_ab)} ÷ 3 = {c}枚（Cの枚数）
4. A君は {c} + {d_bc} + {d_ab} = **{a}枚**

**答え：{a}枚**
""")
    if st.button("次の問題へ"):
        st.session_state.q_data_3 = generate_wasazan_3()
        st.rerun()
