import streamlit as st
import random
import streamlit.components.v1 as components

st.set_page_config(page_title="거지 탈출 RPG", page_icon="💰", layout="centered")

STAGES = [
    {"name":"1 STAGE · 시골 탈출","bg":"🌾","goal":1_000_000,"art":"🌾  🏚️  🌳  🌾"},
    {"name":"2 STAGE · 길거리 탈출","bg":"🚶","goal":5_000_000,"art":"🏢  🛣️  🏪  🚶"},
    {"name":"3 STAGE · 반지하 탈출","bg":"🏠","goal":50_000_000,"art":"🪟  🏠  📦  🚪"},
    {"name":"4 STAGE · 1층 탈출","bg":"🏡","goal":250_000_000,"art":"🏡  🌳  🚗  🧍"},
    {"name":"5 STAGE · 지방도시 탈출","bg":"🏙️","goal":1_250_000_000,"art":"🏢  🏢  🚗  🏢"},
]

def init():
    values = {
        "money":0, "stage":0, "click_value":1000, "extra_clicks":0,
        "click_level":0, "extra_level":0, "cleared":[],
        "effect":None, "rps_result":"", "odd_result":""
    }
    for k,v in values.items():
        if k not in st.session_state:
            st.session_state[k] = v

def fmt(n):
    n = int(n)
    if n >= 100_000_000: return f"{n/100_000_000:.2f}억 원"
    if n >= 10_000: return f"{n/10_000:.1f}만 원"
    return f"{n:,}원"

def upgrade_cost(level):
    return int(1000 * (1.5 ** level))

def effect(amount, effect_id):
    # 클릭 직후 표시되는 독립 iframe 효과
    components.html(f"""
    <div class="money-effect">+{amount:,}원</div>
    <style>
    body {{ margin:0; background:transparent; overflow:hidden; }}
    .money-effect {{
        position:fixed; left:50%; top:45%;
        transform:translate(-50%,20px);
        color:#ffe45c; font:bold 34px Arial;
        text-shadow:0 3px 8px #000;
        white-space:nowrap;
        animation:moneyUp .9s ease-out forwards;
    }}
    @keyframes moneyUp {{
        0% {{opacity:0; transform:translate(-50%,25px) scale(.75)}}
        15% {{opacity:1; transform:translate(-50%,0) scale(1.05)}}
        100% {{opacity:0; transform:translate(-50%,-120px) scale(1)}}
    }}
    </style>
    <script>
    try {{
        const C=window.AudioContext||window.webkitAudioContext;
        const c=new C(), o=c.createOscillator(), g=c.createGain();
        o.type="sine";
        o.frequency.setValueAtTime(600,c.currentTime);
        o.frequency.exponentialRampToValueAtTime(850,c.currentTime+.08);
        g.gain.setValueAtTime(.001,c.currentTime);
        g.gain.exponentialRampToValueAtTime(.08,c.currentTime+.01);
        g.gain.exponentialRampToValueAtTime(.001,c.currentTime+.13);
        o.connect(g); g.connect(c.destination); o.start();
        o.stop(c.currentTime+.14);
    }} catch(e) {{}}
    </script>
    """, height=170)

init()

st.markdown("""
<style>
.stApp{background:linear-gradient(180deg,#181818,#080808);color:#fff}
.block-container{max-width:700px;padding-top:1rem}
.title{text-align:center;font-size:2.35rem;font-weight:900}
.sub{text-align:center;color:#999;margin-bottom:14px}
.scene{height:205px;border-radius:22px;border:1px solid #444;position:relative;
display:flex;align-items:center;justify-content:center;overflow:hidden;box-shadow:0 15px 35px #0008}
.scene0{background:linear-gradient(#84ccef 0 54%,#70834d 54% 100%)}
.scene1{background:linear-gradient(#8cc9ee 0 48%,#666 48% 100%)}
.scene2{background:linear-gradient(#444 0 50%,#121212 50% 100%)}
.scene3{background:linear-gradient(#82ccef 0 54%,#687c50 54% 100%)}
.scene4{background:linear-gradient(#72bee8 0 54%,#555 54% 100%)}
.art{font-size:60px;text-shadow:0 5px 7px #0006}
.character{position:absolute;bottom:15px;font-size:62px;filter:drop-shadow(0 6px 4px #0008)}
.stage{text-align:center;font-size:1.3rem;font-weight:900;margin-top:10px}
.card{background:#111;border:1px solid #383838;border-radius:18px;padding:15px;text-align:center;margin:10px 0}
.money{font-size:2.45rem;font-weight:900;color:#ffe45c}
.income{font-size:1.12rem;font-weight:900;color:#7dff8a;margin-top:5px}
.need{font-weight:900;color:#ffabab;margin-top:5px}
.bar{height:14px;background:#333;border-radius:99px;overflow:hidden;margin-top:10px}
.fill{height:100%;background:linear-gradient(90deg,#ffb900,#ffe45c)}
.section{font-size:1.3rem;font-weight:900;margin:20px 0 9px}
.shop{background:#191919;border:1px solid #333;border-radius:16px;padding:15px;min-height:145px}
.price{color:#ffe45c;font-weight:900;margin-top:12px}
</style>
""", unsafe_allow_html=True)

s = STAGES[st.session_state.stage]
total_click = st.session_state.click_value * (1 + st.session_state.extra_clicks)
needed = max(0, s["goal"] + 1 - st.session_state.money)
progress = min(100, st.session_state.money / s["goal"] * 100)

st.markdown('<div class="title">💸 거지 탈출 RPG</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">클릭해서 돈을 벌고, 업그레이드와 도박으로 탈출하자!</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="scene scene{st.session_state.stage}">
  <div class="art">{s["art"]}</div>
  <div class="character">🧍</div>
</div>
<div class="stage">{s["bg"]} {s["name"]}</div>
<div class="card">
  <div style="color:#999">현재 보유 금액</div>
  <div class="money">{fmt(st.session_state.money)}</div>
  <div class="income">🖱️ 클릭 1회 총 수익: +{total_click:,}원</div>
  <div class="need">🎯 클리어까지 {fmt(needed)}</div>
  <div style="color:#999">목표: {fmt(s["goal"])} 초과</div>
  <div class="bar"><div class="fill" style="width:{progress:.2f}%"></div></div>
</div>
""", unsafe_allow_html=True)

if st.button(f"💰 돈 벌기  +{total_click:,}원", type="primary", use_container_width=True):
    st.session_state.money += total_click
    st.session_state.effect = (total_click, st.session_state.get("effect", (0,0))[1] + 1)
    if st.session_state.money > s["goal"]:
        if st.session_state.stage not in st.session_state.cleared:
            st.session_state.cleared.append(st.session_state.stage)
        if st.session_state.stage < 4:
            st.session_state.stage += 1
            st.toast("🎉 스테이지 클리어!")
        else:
            st.balloons()
            st.toast("🏆 최종 탈출 성공!")
    st.rerun()

if st.session_state.effect:
    effect(st.session_state.effect[0], st.session_state.effect[1])

st.markdown('<div class="section">🛒 상점</div>', unsafe_allow_html=True)
a,b=st.columns(2)
cc=upgrade_cost(st.session_state.click_level)
ec=upgrade_cost(st.session_state.extra_level)

with a:
    st.markdown(f'<div class="shop"><b>💵 클릭 수익 +1,000원</b><br><small>레벨 {st.session_state.click_level}<br>기본 클릭 수익: {st.session_state.click_value:,}원</small><div class="price">가격 {cc:,}원</div></div>',unsafe_allow_html=True)
    if st.button(f"구매 · {cc:,}원",key="clickup",use_container_width=True,disabled=st.session_state.money<cc):
        st.session_state.money-=cc
        st.session_state.click_value+=1000
        st.session_state.click_level+=1
        st.rerun()

with b:
    st.markdown(f'<div class="shop"><b>⚡ 클릭당 +1회 취급</b><br><small>레벨 {st.session_state.extra_level}<br>현재 취급 횟수: {1+st.session_state.extra_clicks}회</small><div class="price">가격 {ec:,}원</div></div>',unsafe_allow_html=True)
    if st.button(f"구매 · {ec:,}원",key="extraup",use_container_width=True,disabled=st.session_state.money<ec):
        st.session_state.money-=ec
        st.session_state.extra_clicks+=1
        st.session_state.extra_level+=1
        st.rerun()

st.markdown('<div class="section">🎰 도박장</div>',unsafe_allow_html=True)
bet=st.number_input("베팅 금액",min_value=0,max_value=int(st.session_state.money),value=0,step=1000)

g1,g2=st.columns(2)

with g1:
    st.markdown("#### ✊ 가위바위보")
    choice=st.selectbox("내 선택",["✊ 바위","✌️ 가위","🖐️ 보"],key="rps_choice")
    if st.button("가위바위보 하기",key="rps",use_container_width=True,disabled=bet<=0):
        options=["✊ 바위","✌️ 가위","🖐️ 보"]
        enemy=random.choice(options)
        p,e=options.index(choice),options.index(enemy)
        if p==e:
            result=f"🤝 무승부! 상대도 {enemy} · 베팅금 반환"
        elif (p==0 and e==1) or (p==1 and e==2) or (p==2 and e==0):
            st.session_state.money+=bet
            result=f"🎉 승리! 상대: {enemy} · +{bet:,}원"
        else:
            st.session_state.money-=bet
            result=f"💀 패배! 상대: {enemy} · -{bet:,}원"
        st.session_state.rps_result=result
        st.rerun()
    if st.session_state.rps_result: st.info(st.session_state.rps_result)

with g2:
    st.markdown("#### 🪙 홀짝")
    oe=st.selectbox("내 선택",["홀","짝"],key="odd_choice")
    if st.button("홀짝 하기",key="odd",use_container_width=True,disabled=bet<=0):
        n=random.randint(1,100)
        actual="홀" if n%2 else "짝"
        if oe==actual:
            st.session_state.money+=bet
            result=f"🎉 정답! {n} → {actual} · +{bet:,}원"
        else:
            st.session_state.money-=bet
            result=f"💀 틀림! {n} → {actual} · -{bet:,}원"
        st.session_state.odd_result=result
        st.rerun()
    if st.session_state.odd_result: st.info(st.session_state.odd_result)

st.markdown('<div class="section">🗺️ 탈출 진행도</div>',unsafe_allow_html=True)
for i,x in enumerate(STAGES):
    status="✅ 클리어" if i in st.session_state.cleared else ("🔥 진행 중" if i==st.session_state.stage else "🔒 잠김")
    st.markdown(f'<div style="padding:11px;margin:5px 0;background:#171717;border-radius:12px;display:flex;justify-content:space-between"><b>{x["bg"]} {x["name"]}</b><span>{fmt(x["goal"])} · {status}</span></div>',unsafe_allow_html=True)

st.divider()
if st.button("🔄 게임 처음부터",use_container_width=True):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()
