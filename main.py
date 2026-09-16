import streamlit as st
import random
import streamlit.components.v1 as components

st.set_page_config(
    page_title="거지 탈출 RPG",
    page_icon="💰",
    layout="centered"
)

# =========================
# 스테이지
# =========================
STAGES = [
    {
        "name": "1 STAGE · 시골 탈출",
        "icon": "🌾",
        "goal": 1_000_000,
        "art": "🌾   🏚️   🌳   🌾",
        "desc": "시골에서 돈을 모아 탈출하자!"
    },
    {
        "name": "2 STAGE · 길거리 탈출",
        "icon": "🚶",
        "goal": 5_000_000,
        "art": "🏢   🛣️   🏪   🚶",
        "desc": "길거리에서 더 큰돈을 모으자!"
    },
    {
        "name": "3 STAGE · 반지하 탈출",
        "icon": "🏠",
        "goal": 50_000_000,
        "art": "🪟   🏠   📦   🚪",
        "desc": "반지하를 벗어나 1층으로 올라가자!"
    },
    {
        "name": "4 STAGE · 1층 탈출",
        "icon": "🏡",
        "goal": 250_000_000,
        "art": "🏡   🌳   🚗   🧍",
        "desc": "더 좋은 집을 위해 계속 돈을 모으자!"
    },
    {
        "name": "5 STAGE · 지방도시 탈출",
        "icon": "🏙️",
        "goal": 1_250_000_000,
        "art": "🏢   🏢   🚗   🏢",
        "desc": "최종 목표를 달성하고 탈출을 완성하자!"
    }
]

def init_game():
    defaults = {
        "money": 0,
        "stage": 0,
        "click_value": 1_000,
        "extra_clicks": 0,
        "click_level": 0,
        "extra_level": 0,
        "cleared": [],
        "rps_result": "",
        "odd_result": "",
        "last_gain": 0,
        "show_effect": False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def money_text(value):
    value = int(value)

    if value >= 100_000_000:
        return f"{value / 100_000_000:.2f}억 원"
    elif value >= 10_000:
        return f"{value / 10_000:.1f}만 원"
    else:
        return f"{value:,}원"

def upgrade_cost(level):
    # 1,000 → 1,500 → 2,250 → 3,375 ...
    return int(1_000 * (1.5 ** level))

def click_effect(amount):
    components.html(
        f"""
        <style>
        html, body {{
            margin: 0;
            padding: 0;
            background: transparent;
            overflow: hidden;
        }}

        .gain {{
            position: fixed;
            left: 50%;
            top: 25px;
            transform: translateX(-50%);
            z-index: 99999;
            color: #ffe45c;
            font-family: Arial, sans-serif;
            font-size: 34px;
            font-weight: 900;
            text-shadow: 0 3px 8px rgba(0,0,0,.9);
            white-space: nowrap;
            animation: gain 1.0s ease-out forwards;
        }}

        @keyframes gain {{
            0% {{
                opacity: 0;
                transform: translate(-50%, 25px) scale(.75);
            }}
            15% {{
                opacity: 1;
                transform: translate(-50%, 0) scale(1.08);
            }}
            100% {{
                opacity: 0;
                transform: translate(-50%, -90px) scale(1);
            }}
        }}
        </style>

        <div class="gain">+{amount:,}원</div>

        <script>
        try {{
            const AudioContext = window.AudioContext || window.webkitAudioContext;

            if (AudioContext) {{
                const audio = new AudioContext();
                const oscillator = audio.createOscillator();
                const gain = audio.createGain();

                oscillator.type = "sine";
                oscillator.frequency.setValueAtTime(600, audio.currentTime);
                oscillator.frequency.exponentialRampToValueAtTime(
                    900,
                    audio.currentTime + 0.1
                );

                gain.gain.setValueAtTime(0.001, audio.currentTime);
                gain.gain.exponentialRampToValueAtTime(
                    0.08,
                    audio.currentTime + 0.01
                );
                gain.gain.exponentialRampToValueAtTime(
                    0.001,
                    audio.currentTime + 0.15
                );

                oscillator.connect(gain);
                gain.connect(audio.destination);

                oscillator.start();
                oscillator.stop(audio.currentTime + 0.16);
            }}
        }} catch(error) {{}}
        </script>
        """,
        height=130
    )

init_game()

# =========================
# 디자인
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 50% 0%, rgba(255,215,80,.10), transparent 35%),
            linear-gradient(180deg, #181818 0%, #080808 100%);
        color: white;
    }

    .block-container {
        max-width: 700px;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    .title {
        text-align: center;
        font-size: 2.35rem;
        font-weight: 900;
        letter-spacing: -2px;
    }

    .subtitle {
        text-align: center;
        color: #999;
        margin-bottom: 15px;
    }

    .scene {
        height: 210px;
        border-radius: 22px;
        border: 1px solid #444;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 15px 40px rgba(0,0,0,.5);
    }

    .scene0 {
        background: linear-gradient(
            180deg,
            #83cbed 0%,
            #d7efb3 53%,
            #70834b 54%,
            #4e602f 100%
        );
    }

    .scene1 {
        background: linear-gradient(
            180deg,
            #8cc9ed 0%,
            #cfd2d4 48%,
            #666 49%,
            #303030 100%
        );
    }

    .scene2 {
        background: linear-gradient(
            180deg,
            #555 0%,
            #333 49%,
            #161616 50%,
            #090909 100%
        );
    }

    .scene3 {
        background: linear-gradient(
            180deg,
            #83caed 0%,
            #dfe9ed 54%,
            #7a8b60 55%,
            #53603f 100%
        );
    }

    .scene4 {
        background: linear-gradient(
            180deg,
            #75bee7 0%,
            #dce2e5 54%,
            #626262 55%,
            #292929 100%
        );
    }

    .art {
        font-size: 58px;
        text-shadow: 0 5px 8px rgba(0,0,0,.35);
    }

    .character {
        position: absolute;
        bottom: 14px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 64px;
        filter: drop-shadow(0 6px 5px rgba(0,0,0,.5));
    }

    .stage-name {
        text-align: center;
        font-size: 1.35rem;
        font-weight: 900;
        margin-top: 10px;
    }

    .description {
        text-align: center;
        color: #aaa;
        margin-bottom: 10px;
    }

    .money-card {
        background: #111;
        border: 1px solid #383838;
        border-radius: 18px;
        padding: 15px;
        text-align: center;
        margin: 10px 0;
    }

    .money-label {
        color: #999;
    }

    .money {
        color: #ffe45c;
        font-size: 2.45rem;
        font-weight: 900;
    }

    .income {
        color: #7dff8a;
        font-size: 1.12rem;
        font-weight: 900;
        margin-top: 5px;
    }

    .need {
        color: #ffaaaa;
        font-weight: 900;
        margin-top: 6px;
    }

    .progress {
        height: 14px;
        background: #333;
        border-radius: 99px;
        overflow: hidden;
        margin-top: 10px;
    }

    .fill {
        height: 100%;
        background: linear-gradient(90deg,#ffb900,#ffe45c);
    }

    .section {
        font-size: 1.3rem;
        font-weight: 900;
        margin: 20px 0 9px;
    }

    .shop {
        background: #191919;
        border: 1px solid #333;
        border-radius: 16px;
        padding: 15px;
        min-height: 145px;
    }

    .shop-price {
        color: #ffe45c;
        font-weight: 900;
        margin-top: 12px;
    }

    button[kind="primary"] {
        min-height: 68px !important;
        border-radius: 18px !important;
        font-size: 1.2rem !important;
        font-weight: 900 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# 현재 스테이지
# =========================
stage = STAGES[st.session_state.stage]
total_click = st.session_state.click_value * (1 + st.session_state.extra_clicks)

# "목표 금액을 넘는 순간"이므로 목표+1까지 필요한 금액
needed = max(0, stage["goal"] + 1 - st.session_state.money)
progress = min(100, (st.session_state.money / stage["goal"]) * 100)

st.markdown(
    '<div class="title">💸 거지 탈출 RPG</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">클릭해서 돈을 벌고 · 업그레이드하고 · 도박해서 탈출하자!</div>',
    unsafe_allow_html=True
)

# =========================
# 배경
# =========================
st.markdown(
    f"""
    <div class="scene scene{st.session_state.stage}">
        <div class="art">{stage["art"]}</div>
        <div class="character">🧍</div>
    </div>

    <div class="stage-name">
        {stage["icon"]} {stage["name"]}
    </div>

    <div class="description">
        {stage["desc"]}
    </div>

    <div class="money-card">
        <div class="money-label">현재 보유 금액</div>
        <div class="money">{money_text(st.session_state.money)}</div>

        <div class="income">
            🖱️ 클릭 1회 총 수익: +{total_click:,}원
        </div>

        <div class="need">
            🎯 클리어까지 {money_text(needed)}
        </div>

        <div class="money-label">
            목표: {money_text(stage["goal"])} 초과
        </div>

        <div class="progress">
            <div class="fill" style="width:{progress:.2f}%"></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# 클릭
# =========================
clicked = st.button(
    f"💰 돈 벌기  +{total_click:,}원",
    type="primary",
    use_container_width=True
)

if clicked:
    # 핵심 수정:
    # st.session_state에 'effect' 같은 별도 튜플을 저장하지 않고
    # 버튼이 눌린 동일한 실행에서 바로 효과를 출력한다.
    st.session_state.money += total_click
    st.session_state.last_gain = total_click
    st.session_state.show_effect = True

    # 스테이지 클리어
    if st.session_state.money > stage["goal"]:
        if st.session_state.stage not in st.session_state.cleared:
            st.session_state.cleared.append(st.session_state.stage)

        if st.session_state.stage < len(STAGES) - 1:
            st.session_state.stage += 1
            st.toast("🎉 스테이지 클리어! 다음 지역으로 이동합니다.")
        else:
            st.balloons()
            st.success("🏆 최종 탈출 성공! 모든 스테이지를 클리어했습니다.")

# 클릭 효과를 버튼 클릭과 같은 실행에서 표시
if clicked and st.session_state.show_effect:
    click_effect(st.session_state.last_gain)
    st.session_state.show_effect = False

# =========================
# 상점
# =========================
st.markdown('<div class="section">🛒 상점</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

click_cost = upgrade_cost(st.session_state.click_level)
extra_cost = upgrade_cost(st.session_state.extra_level)

with col1:
    st.markdown(
        f"""
        <div class="shop">
            <b>💵 클릭 수익 +1,000원</b><br>
            <small>
                레벨: {st.session_state.click_level}<br>
                기본 클릭 수익: {st.session_state.click_value:,}원
            </small>
            <div class="shop-price">가격 {click_cost:,}원</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        f"구매 · {click_cost:,}원",
        key="click_upgrade",
        use_container_width=True,
        disabled=st.session_state.money < click_cost
    ):
        st.session_state.money -= click_cost
        st.session_state.click_value += 1_000
        st.session_state.click_level += 1
        st.rerun()

with col2:
    st.markdown(
        f"""
        <div class="shop">
            <b>⚡ 클릭당 +1회 취급</b><br>
            <small>
                레벨: {st.session_state.extra_level}<br>
                현재 클릭 취급: {1 + st.session_state.extra_clicks}회
            </small>
            <div class="shop-price">가격 {extra_cost:,}원</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        f"구매 · {extra_cost:,}원",
        key="extra_upgrade",
        use_container_width=True,
        disabled=st.session_state.money < extra_cost
    ):
        st.session_state.money -= extra_cost
        st.session_state.extra_clicks += 1
        st.session_state.extra_level += 1
        st.rerun()

# =========================
# 도박장
# =========================
st.markdown('<div class="section">🎰 도박장</div>', unsafe_allow_html=True)

bet = st.number_input(
    "베팅 금액",
    min_value=0,
    max_value=int(st.session_state.money),
    value=0,
    step=1_000
)

gamble1, gamble2 = st.columns(2)

# 가위바위보
with gamble1:
    st.markdown("#### ✊ 가위바위보")
    st.caption("승리: 베팅금만큼 추가 획득 / 패배: 베팅금 손실")

    player = st.selectbox(
        "내 선택",
        ["✊ 바위", "✌️ 가위", "🖐️ 보"],
        key="rps_player"
    )

    if st.button(
        "가위바위보 하기",
        key="rps_play",
        use_container_width=True,
        disabled=bet <= 0
    ):
        choices = ["✊ 바위", "✌️ 가위", "🖐️ 보"]
        enemy = random.choice(choices)

        p = choices.index(player)
        e = choices.index(enemy)

        if p == e:
            result = f"🤝 무승부! 상대도 {enemy} · 베팅금 반환"
        elif (
            (p == 0 and e == 1)
            or (p == 1 and e == 2)
            or (p == 2 and e == 0)
        ):
            st.session_state.money += bet
            result = f"🎉 승리! 상대: {enemy} · +{bet:,}원"
        else:
            st.session_state.money -= bet
            result = f"💀 패배! 상대: {enemy} · -{bet:,}원"

        st.session_state.rps_result = result
        st.rerun()

    if st.session_state.rps_result:
        st.info(st.session_state.rps_result)

# 홀짝
with gamble2:
    st.markdown("#### 🪙 홀짝")
    st.caption("맞히면 베팅금만큼 추가 획득 / 틀리면 베팅금 손실")

    odd_choice = st.selectbox(
        "내 선택",
        ["홀", "짝"],
        key="odd_player"
    )

    if st.button(
        "홀짝 하기",
        key="odd_play",
        use_container_width=True,
        disabled=bet <= 0
    ):
        number = random.randint(1, 100)
        answer = "홀" if number % 2 else "짝"

        if odd_choice == answer:
            st.session_state.money += bet
            result = f"🎉 정답! {number} → {answer} · +{bet:,}원"
        else:
            st.session_state.money -= bet
            result = f"💀 틀림! {number} → {answer} · -{bet:,}원"

        st.session_state.odd_result = result
        st.rerun()

    if st.session_state.odd_result:
        st.info(st.session_state.odd_result)

# =========================
# 진행도
# =========================
st.markdown('<div class="section">🗺️ 탈출 진행도</div>', unsafe_allow_html=True)

for i, s in enumerate(STAGES):
    if i in st.session_state.cleared:
        status = "✅ 클리어"
    elif i == st.session_state.stage:
        status = "🔥 진행 중"
    else:
        status = "🔒 잠김"

    st.markdown(
        f"""
        <div style="
            padding:11px;
            margin:5px 0;
            background:#171717;
            border-radius:12px;
            display:flex;
            justify-content:space-between;
            border:1px solid #292929;
        ">
            <b>{s["icon"]} {s["name"]}</b>
            <span style="color:#aaa">{money_text(s["goal"])} · {status}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# 초기화
# =========================
st.divider()

if st.button("🔄 게임 처음부터", use_container_width=True):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.caption("개인 게임 개발 프로젝트 · Streamlit")
