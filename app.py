import streamlit as st
import random

def generate_dynamic_wasazan():
    # 📝 4つのシチュエーション設定（ポケモンゲットを追加）
    scenarios = [
        {
            "category": "👤 登場人物",
            "names": ["サトシ君", "ゴウ君", "かすみちゃん"],
            "unit": "枚", "item": "カード"
        },
        {
            "category": "🐭 ポケモンゲット（新！）",
            "names": ["サトシ君", "ごう君", "かすみちゃん"],
            "unit": "匹", "item": "ゲットしたポケモン"
        },
        {
            "category": "🍓 大好きな果物",
            "names": ["あまおう", "完熟マンゴー", "シャインマスカット"],
            "unit": "個", "item": "数"
        },
        {
            "category": "🍴 定食屋のメニュー",
            "names": ["特製ラザニア", "厚切り焼魚定食", "欲張り唐揚げ定食"],
            "unit": "円", "item": "お値段"
        }
    ]
    
    scene = random.choice(scenarios)
    names = scene["names"].copy()
    random.shuffle(names)
    
    # 🧮 数値と条件（多い・少ない）の決定
    d1 = random.randint(5, 40)
    d2 = random.randint(5, 40)
    
    # 「少ない」が出てもマイナスにならないよう最小値を調整
    base = random.randint(45, 100) 
    
    # 条件のランダム決定 ("多い" または "少ない")
    cond1 = random.choice(["多い", "少ない"])
    cond2 = random.choice(["多い", "少ない"])
    
    # 各値を計算 (names[2] を基準にする)
    val2 = base
    val1 = val2 + d2 if cond2 == "多い" else val2 - d2
    val0 = val1 + d1 if cond1 == "多い" else val1 - d1
    
    total = val0 + val1 + val2
    
    return scene, names, total, d1, d2, cond1, cond2, val0, val1, val2

st.set_page_config(page_title="Geeky.a.Dad's Lab", page_icon="🔢")
st.title("🔢 3人の和差算：サトシ＆ポケモンVer.")

if 'q_data' not in st.session_state:
    st.session_state.q_data = generate_dynamic_wasazan()

scene, names, total, d1, d2, c1, c2, v0, v1, v2 = st.session_state.q_data

st.subheader(f"今回のテーマ：{scene['category']}")
st.info(f"""
{names[0]}、{names[1]}、{names[2]} の{scene['item']}を全部合わせると **{total}{scene['unit']}** です。

・{names[0]} は {names[1]} より **{d1}{scene['unit']} {c1}** です。
・{names[1]} は {names[2]} より **{d2}{scene['unit']} {c2}** です。

このとき、**{names[0]}** は何{scene['unit']}ですか？
""")

if st.button("ヒント（線分図）と解説を見る"):
    st.markdown("**【パパのロジカル解説】**")
    
    # 簡易線分図の描画
    st.code(f"""
    {names[0]}: {"-" * (v0//5)} ({v0}{scene['unit']})
    {names[1]}: {"-" * (v1//5)} ({v1}{scene['unit']})
    {names[2]}: {"-" * (v2//5)} ({v2}{scene['unit']})
    """)
    
    min_val = min(v0, v1, v2)
    over = total - (min_val * 3)
    
    st.write(f"1. 一番少ない数に合わせて、ハミ出している分（合計 {over}{scene['unit']}）を全体から引きます。")
    st.write(f"2. {total} - {over} = {total - over} （これが一番少ない人の3倍です）")
    st.success(f"結果： **{names[0]} は {v0}{scene['unit']}** です！")

if st.button("次の問題を生成（シチュエーションも変更）"):
    st.session_state.q_data = generate_dynamic_wasazan()
    st.rerun()
