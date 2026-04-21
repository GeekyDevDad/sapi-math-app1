import streamlit as st
import random

def generate_complex_wasazan():
    # シチュエーション（ポケモンゲットに固定）
    names = ["サトシ君", "かすみちゃん", "ごう君"]
    # 難易度調整：サトシを最小にする
    satoshi = random.randint(15, 40)
    diff_sk = random.randint(15, 40) # サトシとカスミの差
    diff_kg = random.randint(10, 30) # カスミとゴウの差
    
    kasumi = satoshi + diff_sk
    gou = kasumi + diff_kg
    total = satoshi + kasumi + gou
    
    return names, total, diff_sk, diff_kg, satoshi, kasumi, gou

st.set_page_config(page_title="Geeky.a.Dad's Lab", page_icon="🐭")
st.title("🔢 ポケモン算数：線分図ハック")

if 'q_data' not in st.session_state:
    st.session_state.q_data = generate_complex_wasazan()

names, total, d_sk, d_kg, v_s, v_k, v_g = st.session_state.q_data

st.info(f"""
{names[0]}、{names[1]}、{names[2]} のゲットしたポケモンを合わせると **{total}匹** です。

・{names[0]} は {names[1]} より **{d_sk}匹 少ない** です。
・{names[1]} は {names[2]} より **{d_kg}匹 少ない** です。

このとき、**{names[0]}** は何匹ですか？
""")

user_input = st.number_input("サトシ君の数を入力:", min_value=0, step=1)

if st.button("判定 ＆ パパのロジカル解説"):
    if user_input == v_s:
        st.success("✨ 正解！完璧な理解だね。")
    else:
        st.error(f"惜しい！正解は {v_s}匹 でした。")
    
    st.write("---")
    st.subheader("📊 左揃えの線分図で見ると？")
    
    # 左揃えの視覚的表現
    st.code(f"""
    サトシ: |----------| (□匹)
    かすみ: |----------|---{d_sk}---| (□ + {d_sk}匹)
    ごう　: |----------|---{d_sk}---|---{d_kg}---| (□ + {d_sk + d_kg}匹)
    """)
    
    st.markdown(f"""
    **【解説】一番少ないサトシ君を $\square$ とすると：**
    1. かすみちゃんは、サトシより **{d_sk}匹** 多い。
    2. ごう君は、かすみよりさらに {d_kg}匹 多いので、サトシより **{d_sk + d_kg}匹** 多い。
    3. 全員の合計は、$(\square \\times 3) + {d_sk} + {d_sk + d_kg} = {total}$ になるね！
    
    **計算：**
    - はみ出しの合計：${d_sk} + {d_sk + d_kg} = {d_sk + d_sk + d_kg}$ 
    - $\square \\times 3 = {total} - {d_sk + d_sk + d_kg} = {total - (d_sk + d_sk + d_kg)}$
    - $\square = {total - (d_sk + d_sk + d_kg)} \\div 3 = {v_s}$ 匹！
    """)

if st.button("次の問題へ"):
    st.session_state.q_data = generate_complex_wasazan()
    st.rerun()
