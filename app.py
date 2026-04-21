import streamlit as st
import random

# --- 1. 問題生成ロジック ---
def generate_stepped_problem(step):
    scenarios = [
        {"names": ["サトシ君", "かすみちゃん", "ごう君"], "item": "ポケモン", "unit": "匹"},
        {"names": ["ピカチュウ", "ゲンガー", "ニャース"], "item": "きのみ", "unit": "個"}
    ]
    scene = random.choice(scenarios)
    names = scene["names"].copy()
    random.shuffle(names)
    
    # 難易度調整
    v_min = random.randint(15 + step, 30 + step * 5)
    d1 = random.randint(10 + step, 20 + step * 2)
    d2 = random.randint(10 + step, 20 + step * 2)
    
    # 最小・中間・最大を確定させてからシャッフル
    vals_sorted = [v_min, v_min + d1, v_min + d1 + d2]
    vals = vals_sorted.copy()
    random.shuffle(vals)
    
    target_idx = random.randint(0, 2)
    
    return {
        "names": names, "vals": vals, "total": sum(vals), 
        "target": names[target_idx], "ans": vals[target_idx],
        "item": scene["item"], "unit": scene["unit"],
        "min_val": v_min
    }

# --- 2. アプリ画面 ---
st.set_page_config(page_title="Geeky.a.Dad's Lab", page_icon="🐭")
st.title("🐭 サトシの特訓：左揃え線分図マスター")

if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.q = generate_stepped_problem(1)
    st.session_state.answered = False

if st.session_state.step > 5:
    st.balloons()
    st.header("🏆 特訓クリア！")
    if st.button("もう一度レベル1から挑戦"):
        st.session_state.step = 1
        st.session_state.q = generate_stepped_problem(1)
        st.session_state.answered = False
        st.rerun()
else:
    q = st.session_state.q
    st.subheader(f"第 {st.session_state.step} 問 / 全5問")
    
    # 文章題の作成
    # 常に names[0] vs [1], [1] vs [2] で比較文を作る
    diff01 = abs(q['vals'][0] - q['vals'][1])
    rel01 = "多い" if q['vals'][0] > q['vals'][1] else "少ない"
    diff12 = abs(q['vals'][1] - q['vals'][2])
    rel12 = "多い" if q['vals'][1] > q['vals'][2] else "少ない"

    st.info(f"""
    {q['names'][0]}、{q['names'][1]}、{q['names'][2]} の{q['item']}を合わせると **{q['total']}{q['unit']}** です。

    ・{q['names'][0]} は {q['names'][1]} より **{diff01}{q['unit']} {rel01}** です。
    ・{q['names'][1]} は {q['names'][2]} より **{diff12}{q['unit']} {rel12}** です。

    **問題： {q['target']} は何{q['unit']}ですか？**
    """)

    user_ans = st.number_input(f"答えを入力", min_value=0, step=1, key=f"in_{st.session_state.step}")

    if st.button("答え合わせ！"):
        st.session_state.answered = True
        if user_ans == q['ans']:
            st.success("✨ 正解！")
        else:
            st.error(f"残念！正解は **{q['ans']}{q['unit']}** でした。")
        
        st.write("---")
        st.markdown("### 📊 ビジュアル線分図解説")
        st.write("左端を $\\square$ （一番少ない人）として揃えてみると...")

        # 視覚的な線分図の描画（columnsを使って左端を揃える）
        max_v = max(q['vals'])
        for i in range(3):
            col1, col2 = st.columns([1, 4])
            with col1:
                st.write(f"**{q['names'][i]}**")
            with col2:
                # 数値に応じた長さのバーを表示
                st.progress(q['vals'][i] / max_v)
                st.caption(f"{q['vals'][i]} {q['unit']}")

        # 積み上げロジックの解説
        m_val = q['min_val']
        over_total = q['total'] - (m_val * 3)
        
        st.markdown(f"""
        **【パパの解き方ポイント】**
        1. 一番少ない人を **$\\square$** とおこう。
        2. 全員の合計（{q['total']}）から「はみ出し分」の合計（{over_total}）を引く。
        3. {q['total']} - {over_total} = **{q['total'] - over_total}** （これが $\\square$ 3つ分！）
        4. $\\square$ ＝ {q['total'] - over_total} ÷ 3 = **{m_val}{q['unit']}**
        5. 聞かれている **{q['target']}** に合わせて、はみ出し分を足せば完了！
        """)

    if st.session_state.answered:
        if st.button("次の問題へ"):
            st.session_state.step += 1
            if st.session_state.step <= 5:
                st.session_state.q = generate_stepped_problem(st.session_state.step)
            st.session_state.answered = False
            st.rerun()
