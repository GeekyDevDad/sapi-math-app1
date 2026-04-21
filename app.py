import streamlit as st
import random

def generate_wasazan_3_random():
    # 3つのシチュエーション設定
    scenarios = [
        {
            "category": "👤 登場人物",
            "names": ["サトシ君", "ごう君", "かすみちゃん"],
            "unit": "枚",
            "item": "カード"
        },
        {
            "category": "👤 登場ポケモン",
            "names": ["ピカチュウ", "ニャース", "ゲンガー"],
            "unit": "枚",
            "item": "カード"
        },
        {
            "category": "🍎 果物",
            "names": ["リンゴ", "みかん", "バナナ"],
            "unit": "個",
            "item": "数"
        },
        {
            "category": "🍱 定食屋",
            "names": ["ハンバーグ定食", "焼魚定食", "唐揚げ定食"],
            "unit": "円",
            "item": "値段"
        }
    ]
    
    scene = random.choice(scenarios)
    names = scene["names"]
    random.shuffle(names) # A, B, Cの役割もランダムに入れ替え
    
    # 数値計算
    diff_1 = random.randint(5, 30)
    diff_2 = random.randint(5, 30)
    base = random.randint(20, 100)
    
    # 3つの値を計算（cを最小とする）
    c_val = base
    b_val = c_val + diff_2
    a_val = b_val + diff_1
    total = a_val + b_val + c_val
    
    return scene, names, total, diff_1, diff_2, a_val, b_val, c_val

st.set_page_config(page_title="Geeky.a.Dad's Lab", page_icon="🔢")
st.title("🔢 3人の和差算：変幻自在Ver.")

if 'q_data' not in st.session_state:
    st.session_state.q_data = generate_wasazan_3_random()

scene, names, total, d1, d2, a, b, c = st.session_state.q_data

st.subheader(f"今回のテーマ：{scene['category']}")
st.info(f"""
{names[0]}、{names[1]}、{names[2]}の{scene['item']}を合わせると **{total}{scene['unit']}** です。
・{names[0]} は {names[1]} より **{d1}{scene['unit']}** 多いです。
・{names[1]} は {names[2]} より **{d2}{scene['unit']}** 多いです。
このとき、**{names[0]}** は何{scene['unit']}ですか？
""")

if st.button("ヒント（線分図）と解説を表示"):
    st.markdown(f"""
    **【線分図イメージ】**
    ```text
    {names[2]}: |----------| ({c}{scene['unit']}：基準)
    {names[1]}: |----------|---{d2}---|
    {names[0]}: |----------|---{d2}---|---{d1}---|
    ```
    """)
    
    over = d2 + (d2 + d1)
    st.write(f"① 一番少ない **{names[2]}** より「はみ出している分」の合計を計算：")
    st.success(f" {d2} + ({d2} + {d1}) = **{over}{scene['unit']}**")
    
    st.write(f"② 全体から引いて、{names[2]}の3倍の値を出す：")
    st.success(f" {total} - {over} = **{total - over}{scene['unit']}**")
    
    st.write(f"③ 1つ分を出し、求めたい {names[0]} を計算：")
    st.success(f" {names[2]} ＝ {total - over} ÷ 3 = {c}{scene['unit']}\n\n {names[0]} ＝ {c} + {d2} + {d1} = **{a}{scene['unit']}**")

if st.button("次の問題（シチュエーション変更）"):
    st.session_state.q_data = generate_wasazan_3_random()
    st.rerun()
