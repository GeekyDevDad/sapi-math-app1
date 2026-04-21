import streamlit as st
import random

def generate_wasazan_3():
    # 3人の差をランダムに設定
    diff_ab = random.randint(5, 30)
    diff_bc = random.randint(5, 30)
    
    # 一番少ない人を基準（C）にする
    c_val = random.randint(20, 100)
    b_val = c_val + diff_bc
    a_val = b_val + diff_ab
    
    total = a_val + b_val + c_val
    return total, diff_ab, diff_bc, a_val, b_val, c_val

st.set_page_config(page_title="Geeky.a.Dad's Lab", page_icon="🔢")
st.title("🔢 3人の和差算：線分図シミュレーター")

if 'q_data' not in st.session_state:
    st.session_state.q_data = generate_wasazan_3()

total, d_ab, d_bc, a, b, c = st.session_state.q_data

st.info(f"A, B, Cの合計は {total}枚です。AはBより {d_ab}枚多く、BはCより {d_bc}枚多いです。Aは何枚？")

if st.button("ヒント（線分図イメージ）を表示"):
    # テキストで線分図を表現
    st.markdown(f"""
    **【線分図のイメージ】**
    ```text
    C: |----------| ({c}枚：ここを基準にする)
    B: |----------|---{d_bc}---|
    A: |----------|---{d_bc}---|---{d_ab}---|
    ```
    """)
    
    st.write("---")
    st.write("**【ステップバイステップ解説】**")
    
    # 計算過程をロジカルに表示
    step1 = d_bc
    step2 = d_bc + d_ab
    over = step1 + step2
    
    st.write(f"① Cより「はみ出している分」を計算します。")
    st.write(f"  ・Bのはみ出し：{step1}枚")
    st.write(f"  ・Aのはみ出し：{step1} + {d_ab} = {step2}枚")
    st.write(f"  ・合計のはみ出し：{over}枚")
    
    st.write(f"② 全体から「はみ出し」を引くと、Cが3人分になります。")
    st.write(f"  ・{total} - {over} = {total - over}枚")
    
    st.write(f"③ Cの枚数を出し、そこからAを求めます。")
    st.write(f"  ・C：{total - over} ÷ 3 = **{c}枚**")
    st.write(f"  ・A：{c} + {step1} + {d_ab} = **{a}枚**")

if st.button("次の問題へ"):
    st.session_state.q_data = generate_wasazan_3()
    st.rerun()
