import streamlit as st
import random

# --- ロジック関数 ---
def generate_step_problem(step):
    """
    ステップ（1〜5）に合わせて難易度を調整して問題を生成する
    """
    # カテゴリー設定
    scenarios = [
        {"names": ["サトシ君", "ゴウ君", "カスミちゃん"], "unit": "匹", "item": "ポケモンをゲットした数"},
        {"names": ["ピカチュウ", "ゲンガー", "ニャース"], "unit": "匹", "item": "きのみを集めた数"}
    ]
    scene = random.choice(scenarios)
    names = scene["names"]
    random.shuffle(names)
    
    # 難易度設定（ステップが上がるごとに数字を大きくする）
    base_range = (5 + step * 5, 20 + step * 10)
    diff_range = (2 + step, 10 + step * 5)
    
    c_val = random.randint(*base_range)
    d1 = random.randint(*diff_range)
    d2 = random.randint(*diff_range)
    
    # 「多い」「少ない」のパターンをランダムに決定
    # pattern 0: AはBより多い, BはCより多い
    # pattern 1: AはBより少ない, BはCより多い ...など
    p1 = random.choice(["多い", "少ない"])
    p2 = random.choice(["多い", "少ない"])
    
    # 実際の値を計算
    b_val = c_val + d2 if p2 == "多い" else c_val - d2
    # Bがマイナスにならないよう調整
    if b_val < 5: 
        b_val = 5
        d2 = abs(b_val - c_val)
        
    a_val = b_val + d1 if p1 == "多い" else b_val - d1
    # Aがマイナスにならないよう調整
    if a_val < 5:
        a_val = 5
        d1 = abs(a_val - b_val)
        
    total = a_val + b_val + c_val
    
    return {
        "scene": scene, "names": names, "total": total,
        "d1": d1, "p1": p1, "d2": d2, "p2": p2,
        "a": a_val, "b": b_val, "c": c_val
    }

# --- アプリ表示 ---
st.set_page_config(page_title="Geeky.a.Dad's Lab", page_icon="🐭")
st.title("🐭 サトシのポケモン算数特訓（全5問）")

# セッション状態の初期化
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.score = 0
    st.session_state.q_data = generate_step_problem(1)
    st.session_state.finished = False

if st.session_state.finished:
    st.balloons()
    st.header("🏆 特訓完了！")
    st.write(f"全5問の特訓が終わりました。お疲れ様！")
    if st.button("もう一度最初からチャレンジする"):
        st.session_state.step = 1
        st.session_state.score = 0
        st.session_state.q_data = generate_step_problem(1)
        st.session_state.finished = False
        st.rerun()
else:
    q = st.session_state.q_data
    st.subheader(f"第 {st.session_state.step} 問 / 全5問")
    
    st.info(f"""
    {q['names'][0]}、{q['names'][1]}、{q['names'][2]} の {q['scene']['item']}を全部合わせると **{q['total']}{q['scene']['unit']}** です。
    
    ・{q['names'][0]} は {q['names'][1]} より **{q['d1']}{q['scene']['unit']} {q['p1']}** です。
    ・{q['names'][1]} は {q['names'][2]} より **{q['d2']}{q['scene']['unit']} {q['p2']}** です。
    
    このとき、**{q['names'][0]}** は何{q['scene']['unit']}ですか？
    """)

    if st.button("答え合わせ・解説を表示"):
        st.markdown("**【線分図のヒント】**")
        # 簡易的な線分図ロジック
        sorted_vals = sorted([("A", q['a']), ("B", q['b']), ("C", q['c'])], key=lambda x: x[1])
        base_name = [n for n, v in [ (q['names'][0], q['a']), (q['names'][1], q['b']), (q['names'][2], q['c']) ] if v == min(q['a'], q['b'], q['c'])][0]
        
        st.code(f"""
        {q['names'][0]}: {"-" * (q['a']//2)} ({q['a']}匹)
        {q['names'][1]}: {"-" * (q['b']//2)} ({q['b']}匹)
        {q['names'][2]}: {"-" * (q['c']//2)} ({q['c']}匹)
        """)
        
        st.success(f"正解は **{q['a']} {q['scene']['unit']}** です！")
        
        if st.session_state.step < 5:
            if st.button("次の問題へ"):
                st.session_state.step += 1
                st.session_state.q_data = generate_step_problem(st.session_state.step)
                st.rerun()
        else:
            if st.button("結果を見る"):
                st.session_state.finished = True
                st.rerun()
