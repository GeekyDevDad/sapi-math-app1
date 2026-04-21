import streamlit as st
import random

# --- 1. 問題生成ロジック ---
def generate_stepped_problem(step):
    # 登場人物とシチュエーション
    scenarios = [
        {"names": ["サトシ君", "かすみちゃん", "ごう君"], "item": "ポケモン", "unit": "匹"},
        {"names": ["ピカチュウ", "ゲンガー", "ニャース"], "item": "きのみ", "unit": "個"}
    ]
    scene = random.choice(scenarios)
    names = scene["names"].copy()
    random.shuffle(names) # 役割をシャッフル
    
    # 難易度調整（ステップアップ）
    min_val = random.randint(15 + step, 30 + step * 5) # 一番少ない人の数
    d1 = random.randint(10 + step, 20 + step * 2) # 最小と中間の差
    d2 = random.randint(10 + step, 20 + step * 2) # 中間と最大の差
    
    # 内部的に[最小, 中間, 最大]の値を確定
    v_min = min_val
    v_mid = v_min + d1
    v_max = v_mid + d2
    
    vals = [v_min, v_mid, v_max]
    random.shuffle(vals) # 名前と数値を紐付け
    
    # ターゲット（誰の答えを求めるか）を決定
    target_idx = random.randint(0, 2)
    target_name = names[target_idx]
    correct_val = vals[target_idx]
    
    total = sum(vals)
    
    # 文章作成用の比較（AはBより〜）
    # names[0] vs names[1]
    r1 = "多い" if vals[0] > vals[1] else "少ない"
    diff1 = abs(vals[0] - vals[1])
    # names[1] vs names[2]
    r2 = "多い" if vals[1] > vals[2] else "少ない"
    diff2 = abs(vals[1] - vals[2])
    
    return {
        "names": names, "vals": vals, "total": total, "target": target_name, "ans": correct_val,
        "d1": diff1, "r1": r1, "d2": diff2, "r2": r2, "item": scene["item"], "unit": scene["unit"]
    }

# --- 2. アプリ画面 ---
st.set_page_config(page_title="Geeky.a.Dad's Lab", page_icon="🐭")
st.title("🐭 サトシの特訓：積み上げ線分図マスター")

if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.q = generate_stepped_problem(1)
    st.session_state.answered = False

if st.session_state.step > 5:
    st.balloons()
    st.header("🏆 特訓クリア！")
    st.write("全5問のシャッフル問題を突破しました！")
    if st.button("もう一度レベル1から挑戦"):
        st.session_state.step = 1
        st.session_state.q = generate_stepped_problem(1)
        st.session_state.answered = False
        st.rerun()
else:
    q = st.session_state.q
    st.subheader(f"第 {st.session_state.step} 問 / 全5問")
    
    st.info(f"""
    {q['names'][0]}、{q['names'][1]}、{q['names'][2]} の{q['item']}を合わせると **{q['total']}{q['unit']}** です。

    ・{q['names'][0]} は {q['names'][1]} より **{q['d1']}{q['unit']} {q['r1']}** です。
    ・{q['names'][1]} は {q['names'][2]} より **{q['d2']}{q['unit']} {q['r2']}** です。

    **問題： {q['target']} は何{q['unit']}ですか？**
    """)

    user_ans = st.number_input(f"{q['target']}の答えを入力", min_value=0, step=1, key=f"in_{st.session_state.step}")

    if st.button("答え合わせ！"):
        st.session_state.answered = True
        if user_ans == q['ans']:
            st.success("✨ 正解！完璧なロジックだ！")
        else:
            st.error(f"残念！正解は **{q['ans']}{q['unit']}** でした。")
        
        # --- 積み上げ式・徹底解説 ---
        st.write("---")
        st.markdown("### 📊 パパの積み上げ式・徹底解説")
        
        # 誰が一番少ないか探す
        m_val = min(q['vals'])
        m_name = q['names'][q['vals'].index(m_val)]
        
        # 各自の「はみ出し」を計算
        over_list = [v - m_val for v in q['vals']]
        
        st.code(f"""
        {q['names'][0]}: |----------|{"---" if over_list[0]>0 else ""}{over_list[0] if over_list[0]>0 else ""}
        {q['names'][1]}: |----------|{"---" if over_list[1]>0 else ""}{over_list[1] if over_list[1]>0 else ""}
        {q['names'][2]}: |----------|{"---" if over_list[2]>0 else ""}{over_list[2] if over_list[2]>0 else ""}
        """)
        
        total_over = sum(over_list)
        st.markdown(f"""
        1. 一番少ない **{m_name}** を $\\square$ とおいて、全員を左に揃えよう。
        2. 全員の「はみ出し」を合計すると： **{total_over}{q['unit']}**
        3. 全体から引くと、$\\square$ が3個分になるよ： {q['total']} - {total_over} = **{q['total'] - total_over}**
        4. $\\square$ （{m_name}） ＝ {q['total'] - total_over} ÷ 3 = **{m_val}{q['unit']}**
        """)
        
        if q['target'] != m_name:
            st.write(f"5. 最後に聞かれている **{q['target']}** を計算： {m_val} + {q['ans'] - m_val} = **{q['ans']}{q['unit']}**")

    if st.session_state.answered:
        if st.button("次のレベルへ"):
            st.session_state.step += 1
            if st.session_state.step <= 5:
                st.session_state.q = generate_stepped_problem(st.session_state.step)
            st.session_state.answered = False
            st.rerun()
