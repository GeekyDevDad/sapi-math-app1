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
st.title("🐭 サトシの特訓：色分け線分図マスター")

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
    
    # 比較文の作成
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
        st.markdown("### 📊 パパの色分け線分図（積み上げ式）")
        
        m_val = q['min_val']
        max_v = max(q['vals'])
        
        # HTML/CSSで色分け線分図を作成
        for i in range(3):
            val = q['vals'][i]
            over = val - m_val
            
            # 割合計算（表示用）
            blue_pct = (m_val / max_v) * 100
            red_pct = (over / max_v) * 100
            
            st.write(f"**{q['names'][i]}** ({val}{q['unit']})")
            st.markdown(f"""
                <div style="display: flex; width: 100%; background-color: #eee; height: 25px; border-radius: 5px; margin-bottom: 15px;">
                    <div style="width: {blue_pct}%; background-color: #2e86de; border-right: 2px solid white; border-radius: 5px 0 0 5px;"></div>
                    <div style="width: {red_pct}%; background-color: #ee5253; border-radius: 0 5px 5px 0;"></div>
                </div>
            """, unsafe_allow_html=True)

        over_total = q['total'] - (m_val * 3)
        
        st.markdown(f"""
        **【ロジック解説】**
        - <span style="color: #2e86de; font-weight: bold;">青色の部分</span> は、一番少ない人と同じ「基本のカタマリ」です。
        - <span style="color: #ee5253; font-weight: bold;">赤色の部分</span> は、そこから増えた「はみ出し分」です。
        
        1. まず、全体の **{q['total']}** から、赤い部分の合計 **{over_total}** を引きます。
        2. {q['total']} - {over_total} = **{q['total'] - over_total}** （これが青い箱3つ分！）
        3. 青い箱1つ（一番少ない人） ＝ {q['total'] - over_total} ÷ 3 = **{m_val}{q['unit']}**
        4. あとは聞かれている人の「赤い部分」を足せば答えが出るよ！
        """, unsafe_allow_html=True)

    if st.session_state.answered:
        if st.button("次の問題へ"):
            st.session_state.step += 1
            if st.session_state.step <= 5:
                st.session_state.q = generate_stepped_problem(st.session_state.step)
            st.session_state.answered = False
            st.rerun()
