import streamlit as st
import random

# --- 1. 問題生成ロジック ---
def generate_step_problem(step):
    # 名前とカテゴリー
    names_original = ["サトシ君", "かすみちゃん", "ごう君"]
    item_type = random.choice(["ポケモン", "きのみ"])
    unit = "匹" if item_type == "ポケモン" else "個"
    
    # 難易度調整（ステップが上がるごとに数値と差を大きくする）
    base_val = random.randint(15 + step, 30 + step * 5)
    d1 = random.randint(5 + step, 15 + step * 2) # AとBの差
    d2 = random.randint(5 + step, 15 + step * 2) # BとCの差
    
    # 登場順をシャッフル
    display_names = names_original.copy()
    random.shuffle(display_names)
    
    # 誰を最小にするか、誰の答えを求めるかを決定
    # ここでは計算を安定させるため、内部的に[最小, 中間, 最大]を計算してから名前に割り当てる
    vals = [base_val, base_val + d1, base_val + d1 + d2]
    random.shuffle(vals)
    
    # 誰の答えを求めるか（ターゲット）
    target_idx = random.randint(0, 2)
    target_name = display_names[target_idx]
    correct_val = vals[target_idx]
    
    # 合計
    total = sum(vals)
    
    # 「〜より多い/少ない」の文章を作成
    # names[0] と names[1] の関係
    rel1 = "多い" if vals[0] > vals[1] else "少ない"
    diff1 = abs(vals[0] - vals[1])
    
    # names[1] と names[2] の関係
    rel2 = "多い" if vals[1] > vals[2] else "少ない"
    diff2 = abs(vals[1] - vals[2])
    
    return {
        "names": display_names, "total": total, "item": item_type, "unit": unit,
        "d1": diff1, "r1": rel1, "d2": diff2, "r2": rel2,
        "target": target_name, "ans": correct_val, "all_vals": vals
    }

# --- 2. アプリ表示 ---
st.set_page_config(page_title="Geeky.a.Dad's Lab", page_icon="🐭")
st.title("🔢 ポケモン和差算：ターゲット・シャッフル")

# セッション初期化
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.q = generate_step_problem(1)
    st.session_state.answered = False

# 全5問終了後の画面
if st.session_state.step > 5:
    st.balloons()
    st.header("🏆 特訓完了！")
    st.write("全5問のシャッフル特訓をクリアしました。君の読解力は最高だ！")
    if st.button("もう一度最初からチャレンジ"):
        st.session_state.step = 1
        st.session_state.q = generate_step_problem(1)
        st.session_state.answered = False
        st.rerun()
else:
    q = st.session_state.q
    st.subheader(f"第 {st.session_state.step} 問 / 全5問 (Lv.{st.session_state.step})")
    
    st.info(f"""
    {q['names'][0]}、{q['names'][1]}、{q['names'][2]} の {q['item']}を合わせると **{q['total']}{q['unit']}** です。

    ・{q['names'][0]} は {q['names'][1]} より **{q['d1']}{q['unit']} {q['r1']}** です。
    ・{q['names'][1]} は {q['names'][2]} より **{q['d2']}{q['unit']} {q['r2']}** です。

    **【問題】 {q['target']} は何{q['unit']}ですか？**
    """)

    user_input = st.number_input(f"{q['target']} の数値を入力", min_value=0, step=1, key=f"input_{st.session_state.step}")

    if st.button("答え合わせ！"):
        st.session_state.answered = True
        if user_input == q['ans']:
            st.success(f"✨ 正解！{q['target']} は {q['ans']}{q['unit']} だね！")
        else:
            st.error(f"残念！正解は **{q['ans']}{q['unit']}** でした。")
        
        # 線分図と積み上げ解説
        st.write("---")
        st.markdown("**【パパの積み上げ式解説】**")
        
        min_v = min(q['all_vals'])
        st.code(f"""
        {q['names'][0]}: {"-" * (q['all_vals'][0]//3)} ({q['all_vals'][0]}{q['unit']})
        {q['names'][1]}: {"-" * (q['all_vals'][1]//3)} ({q['all_vals'][1]}{q['unit']})
        {q['names'][2]}: {"-" * (q['all_vals'][2]//3)} ({q['all_vals'][2]}{q['unit']})
        """)
        
        st.write(f"一番少ない人を $\square$ とすると：")
        st.write(f"（$\square \\times 3$）＋（他2人のハミ出し合計）＝ {q['total']}")

    if st.session_state.answered:
        if st.button("次の問題へ"):
            st.session_state.step += 1
            if st.session_state.step <= 5:
                st.session_state.q = generate_step_problem(st.session_state.step)
            st.session_state.answered = False
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("### Geeky.a.Dad's Note")
st.sidebar.caption("名前が変わると、問題文を最後まで読む癖がつくよ！")
