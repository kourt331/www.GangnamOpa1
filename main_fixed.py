import streamlit as st
import time
import streamlit.components.v1 as components

st.set_page_config(
    page_title="거지 탈출 RPG",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# 게임 데이터
# -----------------------------
STAGES = [
    {
        "name": "1 STAGE · 시골 탈출",
        "short": "시골",
        "background": "🌾",
        "description": "시골에서 돈을 모아 새로운 삶을 시작하자!",
        "goal": 1_000_000,
    },
    {
        "name": "2 STAGE · 길거리 탈출",
        "short": "길거리",
        "background": "🚶",
        "description": "길거리에서 더 큰돈을 모아 반지하를 탈출하자!",
        "goal": 5_000_000,
    },
    {
        "name": "3 STAGE · 반지하 탈출",
        "short": "반지하",
        "background": "🏠",
        "description": "반지하를 벗어나 1층 집으로 올라가자!",
        "goal": 50_000_000,
    },
    {
        "name": "4 STAGE · 1층 탈출",
        "short": "1층집",
        "background": "🏡",
        "description": "더 넓은 집을 위해 2억 5천만 원을 모으자!",
        "goal": 250_000_000,
    },
    {
        "name": "5 STAGE · 지방도시 탈출",
        "short": "지방도시 아파트",
        "background": "🏙️",
        "description": "지방도시 아파트를 넘어 최종 목표에 도전하자!",
        "goal": 1_250_000_000,
    },
]

DEFAULT_MONEY_PER_CLICK = 1_000
BASE_UPGRADE_COST = 1_000


def init_game():
    defaults = {
        "money": 0,
        "stage": 0,
        "money_per_click": DEFAULT_MONEY_PER_CLICK,
        "extra_clicks": 0,
        "click_upgrade_level": 0,
        "extra_click_level": 0,
        "last_gain": 0,
        "gain_id": 0,
        "cleared_stages": [],
        "game_complete": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def format_money(value):
    value = int(value)
    if value >= 100_000_000:
        return f"{value / 100_000_000:.2f}억 원"
    if value >= 10_000:
        return f"{value / 10_000:.1f}만 원"
    return f"{value:,}원"


def upgrade_cost(level):
    # 1회차 1,000원, 이후 50% 상승
    return int(BASE_UPGRADE_COST * (1.5 ** level))


def make_sound_and_effect(amount, effect_id):
    # Web Audio API를 이용한 아주 짧은 효과음 + 떠오르는 +금액
    html = f"""
    <div id="gain-{effect_id}" style="
        position:fixed;
        left:50%;
        top:42%;
        transform:translate(-50%, -50%);
        z-index:9999;
        pointer-events:none;
        font-family:Arial,sans-serif;
        font-size:30px;
        font-weight:900;
        color:#ffe45c;
        text-shadow:0 3px 8px #000;
        animation:floatUp 0.85s ease-out forwards;
    ">+{amount:,}</div>
    <style>
    @keyframes floatUp {{
        0% {{ opacity:0; transform:translate(-50%, -20%); }}
        15% {{ opacity:1; }}
        100% {{ opacity:0; transform:translate(-50%, -170%); }}
    }}
    </style>
    <script>
    (() => {{
        try {{
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (!AudioCtx) return;
            const ctx = new AudioCtx();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = "sine";
            osc.frequency.setValueAtTime(520, ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(760, ctx.currentTime + 0.08);
            gain.gain.setValueAtTime(0.0001, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.08, ctx.currentTime + 0.01);
            gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.12);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + 0.13);
        }} catch (e) {{}}
    }})();
    </script>
    """
    components.html(html, height=1)


init_game()

# -----------------------------
# CSS
# -----------------------------
st.markdown(
    """
<style>
    .stApp {
        background:
            radial-gradient(circle at 50% 0%, rgba(255,220,100,.13), transparent 35%),
            linear-gradient(180deg, #171717 0%, #0d0d0d 100%);
        color: #f5f5f5;
    }

    .block-container {
        max-width: 680px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    .game-title {
        text-align:center;
        font-size:2.2rem;
        font-weight:900;
        letter-spacing:-2px;
        margin-bottom:.1rem;
    }

    .sub-title {
        text-align:center;
        color:#aaa;
        margin-bottom:1rem;
    }

    .stage-card {
        border:1px solid #3a3a3a;
        border-radius:20px;
        overflow:hidden;
        background:#191919;
        box-shadow:0 12px 35px rgba(0,0,0,.35);
        margin-bottom:14px;
    }

    .stage-bg {
        height:155px;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:90px;
        background:
            linear-gradient(rgba(0,0,0,.08), rgba(0,0,0,.5)),
            linear-gradient(135deg,#4c4938,#222);
    }

    .stage-info {
        padding:14px 17px 8px;
    }

    .stage-name {
        font-size:1.25rem;
        font-weight:900;
    }

    .stage-description {
        color:#aaa;
        font-size:.9rem;
        margin-top:3px;
    }

    .money-box {
        text-align:center;
        padding:12px;
        margin:8px 0 10px;
        background:#111;
        border-radius:16px;
        border:1px solid #333;
    }

    .money {
        color:#ffe45c;
        font-size:2.25rem;
        font-weight:900;
    }

    .goal {
        color:#aaa;
        font-size:.9rem;
    }

    .bar {
        height:14px;
        background:#303030;
        border-radius:99px;
        overflow:hidden;
        margin-top:9px;
    }

    .fill {
        height:100%;
        background:linear-gradient(90deg,#ffbd17,#ffe45c);
        border-radius:99px;
        transition:width .2s;
    }

    .shop-title {
        font-size:1.25rem;
        font-weight:900;
        margin:16px 0 8px;
    }

    .hint {
        text-align:center;
        color:#888;
        font-size:.82rem;
        margin-top:4px;
    }

    button[kind="primary"] {
        min-height:68px !important;
        border-radius:18px !important;
        font-size:1.25rem !important;
        font-weight:900 !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap:10px;
    }
</style>
""",
    unsafe_allow_html=True,
)

stage = STAGES[st.session_state.stage]
goal = stage["goal"]

# -----------------------------
# 헤더
# -----------------------------
st.markdown('<div class="game-title">💸 거지 탈출 RPG</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">클릭해서 돈을 벌고, 업그레이드해서 다음 스테이지로 탈출하세요.</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# 스테이지 표시
# -----------------------------
stage_progress = min(100, st.session_state.money / goal * 100)

st.markdown(
    f"""
<div class="stage-card">
    <div class="stage-bg">{stage["background"]}</div>
    <div class="stage-info">
        <div class="stage-name">{stage["name"]}</div>
        <div class="stage-description">{stage["description"]}</div>
    </div>
</div>

<div class="money-box">
    <div class="goal">현재 보유금</div>
    <div class="money">{format_money(st.session_state.money)}</div>
    <div class="goal">목표: {format_money(goal)} 초과</div>
    <div class="bar">
        <div class="fill" style="width:{stage_progress:.2f}%"></div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# 클릭
# -----------------------------
if st.button(
    f"💰 돈 벌기  +{st.session_state.money_per_click:,}원",
    type="primary",
    use_container_width=True,
):
    gain = st.session_state.money_per_click * (1 + st.session_state.extra_clicks)
    st.session_state.money += gain
    st.session_state.last_gain = gain
    st.session_state.gain_id += 1

    # 화면 갱신 전 효과를 표시
    make_sound_and_effect(gain, st.session_state.gain_id)

    # 스테이지 클리어 판정
    if st.session_state.money > goal:
        if st.session_state.stage not in st.session_state.cleared_stages:
            st.session_state.cleared_stages.append(st.session_state.stage)

        if st.session_state.stage < len(STAGES) - 1:
            st.session_state.stage += 1
        else:
            st.session_state.game_complete = True

    st.rerun()

st.markdown(
    f'<div class="hint">현재 클릭 1회 = {st.session_state.money_per_click:,}원 × {1 + st.session_state.extra_clicks}회 취급</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# 상점
# -----------------------------
st.markdown('<div class="shop-title">🛒 상점</div>', unsafe_allow_html=True)

click_cost = upgrade_cost(st.session_state.click_upgrade_level)
extra_cost = upgrade_cost(st.session_state.extra_click_level)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div style="background:#1b1b1b;border:1px solid #333;border-radius:16px;padding:15px;min-height:155px;">
        <b>💵 클릭 수익 +1,000원</b><br>
        <span style="color:#999;font-size:.85rem;">레벨 {st.session_state.click_upgrade_level}</span><br><br>
        <span style="color:#ffe45c;font-weight:900;">{click_cost:,}원</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        f"구매 · {click_cost:,}원",
        key="buy_click",
        use_container_width=True,
        disabled=st.session_state.money < click_cost,
    ):
        st.session_state.money -= click_cost
        st.session_state.money_per_click += 1_000
        st.session_state.click_upgrade_level += 1
        st.rerun()

with col2:
    st.markdown(
        f"""
        <div style="background:#1b1b1b;border:1px solid #333;border-radius:16px;padding:15px;min-height:155px;">
        <b>⚡ 클릭당 +1회 취급</b><br>
        <span style="color:#999;font-size:.85rem;">레벨 {st.session_state.extra_click_level}</span><br><br>
        <span style="color:#ffe45c;font-weight:900;">{extra_cost:,}원</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        f"구매 · {extra_cost:,}원",
        key="buy_extra",
        use_container_width=True,
        disabled=st.session_state.money < extra_cost,
    ):
        st.session_state.money -= extra_cost
        st.session_state.extra_clicks += 1
        st.session_state.extra_click_level += 1
        st.rerun()

# -----------------------------
# 진행 상황
# -----------------------------
st.markdown('<div class="shop-title">🗺️ 탈출 진행도</div>', unsafe_allow_html=True)

for i, s in enumerate(STAGES):
    if i in st.session_state.cleared_stages:
        status = "✅ 클리어"
    elif i == st.session_state.stage:
        status = "🔥 진행 중"
    else:
        status = "🔒 잠김"

    st.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding:11px 13px;
            margin:5px 0;
            border-radius:12px;
            background:{'#24200f' if i == st.session_state.stage else '#171717'};
            border:1px solid {'#806d20' if i == st.session_state.stage else '#292929'};
        ">
            <span><b>{s["background"]} {s["short"]}</b></span>
            <span style="color:#aaa;font-size:.85rem;">{format_money(s["goal"])} · {status}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# 게임 완료 / 초기화
# -----------------------------
if st.session_state.game_complete:
    st.success("🎉 최종 탈출 성공! 모든 스테이지를 클리어했습니다!")

st.divider()

if st.button("🔄 게임 처음부터", use_container_width=True):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.caption("※ 게임의 기본 구조와 아이디어를 바탕으로 제작한 개인 프로젝트입니다.")
