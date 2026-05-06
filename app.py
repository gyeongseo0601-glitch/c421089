import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="총괄생산계획 최적화",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS 스타일 ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
    --primary: #0f62fe;
    --primary-dark: #0043ce;
    --accent: #42be65;
    --danger: #fa4d56;
    --warning: #f1c21b;
    --bg: #161616;
    --surface: #262626;
    --surface2: #393939;
    --border: #525252;
    --text: #f4f4f4;
    --text-muted: #a8a8a8;
}

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans KR', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

.stApp { background-color: var(--bg); }

/* 사이드바 */
section[data-testid="stSidebar"] {
    background-color: #1a1a1a;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stMarkdown h2 {
    color: var(--primary);
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: 1.5rem;
}

/* 헤더 배너 */
.header-banner {
    background: linear-gradient(135deg, #0f62fe 0%, #0043ce 50%, #001d6c 100%);
    padding: 2rem 2.5rem;
    border-radius: 0;
    margin: -1rem -1rem 2rem -1rem;
    position: relative;
    overflow: hidden;
}
.header-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: rgba(255,255,255,0.03);
    border-radius: 50%;
}
.header-banner h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #fff;
    margin: 0;
    letter-spacing: -0.02em;
}
.header-banner p {
    color: rgba(255,255,255,0.65);
    margin: 0.4rem 0 0;
    font-size: 0.95rem;
    font-weight: 300;
}
.header-tag {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    color: #fff;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.2rem 0.6rem;
    border-radius: 2px;
    margin-bottom: 0.8rem;
}

/* KPI 카드 */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    margin-bottom: 2rem;
}
.kpi-card {
    background: var(--surface);
    padding: 1.5rem;
    position: relative;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--primary);
}
.kpi-card.green::before { background: var(--accent); }
.kpi-card.red::before   { background: var(--danger); }
.kpi-card.yellow::before { background: var(--warning); }
.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    font-family: 'IBM Plex Mono', monospace;
    color: var(--text);
    line-height: 1;
}
.kpi-unit {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
    font-family: 'IBM Plex Mono', monospace;
}

/* 섹션 헤더 */
.section-header {
    border-left: 3px solid var(--primary);
    padding-left: 0.75rem;
    margin: 2rem 0 1rem;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
    letter-spacing: -0.01em;
}

/* 테이블 */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
}
.styled-table th {
    background: var(--surface2);
    color: var(--text-muted);
    font-weight: 600;
    font-size: 0.7rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.6rem 1rem;
    text-align: right;
    border-bottom: 1px solid var(--border);
}
.styled-table th:first-child { text-align: left; }
.styled-table td {
    padding: 0.55rem 1rem;
    text-align: right;
    border-bottom: 1px solid #2e2e2e;
    color: var(--text);
}
.styled-table td:first-child { text-align: left; color: var(--text-muted); }
.styled-table tr:hover td { background: var(--surface); }
.styled-table .highlight { color: var(--accent); font-weight: 600; }
.styled-table .alert { color: var(--danger); font-weight: 600; }

/* 상태 뱃지 */
.badge {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 2px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.06em;
}
.badge-ok { background: rgba(66,190,101,0.15); color: var(--accent); }
.badge-warn { background: rgba(241,194,27,0.15); color: var(--warning); }
.badge-err { background: rgba(250,77,86,0.15); color: var(--danger); }

/* Plotly 다크 배경 */
.js-plotly-plot .plotly .modebar { background: transparent !important; }

/* 탭 */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    color: var(--text-muted);
    font-family: 'IBM Plex Sans KR', sans-serif;
    font-size: 0.85rem;
    font-weight: 500;
    padding: 0.75rem 1.5rem;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: var(--primary) !important;
    border-bottom: 2px solid var(--primary) !important;
    background: transparent !important;
}

/* 슬라이더/인풋 */
.stSlider > div > div > div { background: var(--primary) !important; }
.stNumberInput input { background: var(--surface2) !important; color: var(--text) !important; border-color: var(--border) !important; }

/* 버튼 */
.stButton > button {
    background: var(--primary) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'IBM Plex Sans KR', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    padding: 0.6rem 1.5rem !important;
    transition: background 0.15s !important;
}
.stButton > button:hover { background: var(--primary-dark) !important; }

.infeasible-banner {
    background: rgba(250,77,86,0.1);
    border: 1px solid var(--danger);
    border-left: 4px solid var(--danger);
    padding: 1rem 1.5rem;
    border-radius: 2px;
    color: var(--danger);
    font-weight: 600;
}
.feasible-banner {
    background: rgba(66,190,101,0.1);
    border: 1px solid var(--accent);
    border-left: 4px solid var(--accent);
    padding: 1rem 1.5rem;
    border-radius: 2px;
    color: var(--accent);
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# ── Pyomo 최적화 함수 ─────────────────────────────────────────
def solve_app(params, demand, model_type="LP"):
    """총괄생산계획 최적화 (Pyomo)"""
    try:
        from pyomo.environ import (
            ConcreteModel, Var, Objective, Constraint, SolverFactory,
            NonNegativeReals, NonNegativeIntegers, minimize, value, Set
        )

        D = demand
        TH = len(D)
        TIME = range(0, TH + 1)
        T = range(1, TH + 1)

        type_var = NonNegativeIntegers if model_type == "IP" else NonNegativeReals

        m = ConcreteModel()

        # 결정변수
        m.W = Var(TIME, domain=type_var, bounds=(0, None))
        m.H = Var(TIME, domain=type_var, bounds=(0, None))
        m.L = Var(TIME, domain=type_var, bounds=(0, None))
        m.P = Var(TIME, domain=type_var, bounds=(0, None))
        m.I = Var(TIME, domain=NonNegativeReals, bounds=(0, None))
        m.S = Var(TIME, domain=NonNegativeReals, bounds=(0, None))
        m.C = Var(TIME, domain=type_var, bounds=(0, None))
        m.O = Var(TIME, domain=NonNegativeReals, bounds=(0, None))

        p = params

        # 목적함수: 비용 최소화
        # Z = 정규임금비 + 초과시간노동비 + 고용비 + 해고비 + 재고유지비 + 재고부족비 + 재료비 + 하청비
        reg_wage = p['reg_wage'] * p['work_hours'] * p['work_days']  # 시간당 임금 × 8 × 20
        m.Cost = Objective(
            expr=sum(
                reg_wage * m.W[t]
                + p['ot_wage'] * m.O[t]
                + p['hire_cost'] * m.H[t]
                + p['fire_cost'] * m.L[t]
                + p['inv_cost'] * m.I[t]
                + p['backlog_cost'] * m.S[t]
                + p['mat_cost'] * m.P[t]
                + p['sub_cost'] * m.C[t]
                for t in T
            ),
            sense=minimize
        )

        # 제약조건
        # 노동력
        m.labor = Constraint(T, rule=lambda m, t: m.W[t] == m.W[t-1] + m.H[t] - m.L[t])

        # 생산능력: P_t <= (work_days×work_hours / std_time) × W_t + O_t/std_time
        prod_per_worker = p['work_days'] * p['work_hours'] / p['std_time']
        m.capacity = Constraint(T, rule=lambda m, t:
            m.P[t] <= prod_per_worker * m.W[t] + m.O[t] / p['std_time']
        )

        # 재고균형
        m.inventory = Constraint(T, rule=lambda m, t:
            m.I[t] == m.I[t-1] + m.P[t] + m.C[t] - D[t-1] - m.S[t-1] + m.S[t]
        )

        # 초과근무 제한
        m.overtime = Constraint(T, rule=lambda m, t: m.O[t] <= p['max_ot'] * m.W[t])

        # 초기 조건
        m.W_0 = Constraint(rule=lambda m: m.W[0] == p['init_workers'])
        m.I_0 = Constraint(rule=lambda m: m.I[0] == p['init_inv'])
        m.S_0 = Constraint(rule=lambda m: m.S[0] == 0)

        # 최종 조건
        m.last_inv = Constraint(rule=lambda m: m.I[TH] >= p['final_inv'])
        m.last_short = Constraint(rule=lambda m: m.S[TH] == 0)

        # 솔버 실행
        solver = SolverFactory('glpk')
        result = solver.solve(m, tee=False)

        status = str(result.solver.termination_condition)
        if status != 'optimal':
            return None, status

        # 결과 추출 (t=0은 초기조건으로 고정, H/L/P/C/O는 t=1부터 유효)
        def safe_val(var, t):
            try:
                v = value(var[t])
                return v if v is not None else 0.0
            except Exception:
                return 0.0

        res = {
            'cost': value(m.Cost),
            # W, I, S: t=0(초기값) 포함
            'W': [safe_val(m.W, t) for t in TIME],
            'I': [safe_val(m.I, t) for t in TIME],
            'S': [safe_val(m.S, t) for t in TIME],
            # H, L, P, C, O: t=0은 의미없으므로 None으로 채움
            'H': [None] + [safe_val(m.H, t) for t in T],
            'L': [None] + [safe_val(m.L, t) for t in T],
            'P': [None] + [safe_val(m.P, t) for t in T],
            'C': [None] + [safe_val(m.C, t) for t in T],
            'O': [None] + [safe_val(m.O, t) for t in T],
        }
        return res, 'optimal'

    except Exception as e:
        return None, str(e)


# ── 차트 공통 레이아웃 ─────────────────────────────────────────
CHART_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='IBM Plex Sans KR, IBM Plex Mono', color='#a8a8a8', size=11),
    xaxis=dict(showgrid=False, zeroline=False, color='#525252',
               tickfont=dict(color='#a8a8a8')),
    yaxis=dict(showgrid=True, gridcolor='#2e2e2e', zeroline=False, color='#525252',
               tickfont=dict(color='#a8a8a8')),
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#a8a8a8', size=10)),
    hovermode='x unified',
)

COLORS = {
    'blue':   '#0f62fe',
    'green':  '#42be65',
    'red':    '#fa4d56',
    'yellow': '#f1c21b',
    'purple': '#be95ff',
    'cyan':   '#33b1ff',
    'orange': '#ff832b',
    'teal':   '#08bdba',
}

def months(n):
    return [f"{i}월" for i in range(1, n+1)]


# ── 사이드바 ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏭 APP 총괄생산계획")

    st.markdown("## 📊 수요 설정")
    st.caption("계획기간의 월별 예상수요 (단위: 개)")

    n_months = st.selectbox("계획기간 (개월)", [6, 9, 12], index=0)
    default_demand = [1600, 3000, 3200, 3800, 2200, 2200,
                      2500, 2800, 3100, 2700, 2400, 2100][:n_months]

    demand_inputs = []
    cols = st.columns(2)
    for i in range(n_months):
        with cols[i % 2]:
            val = st.number_input(f"{i+1}월", min_value=0, max_value=20000,
                                  value=default_demand[i], step=100, key=f"d{i}")
            demand_inputs.append(val)

    st.markdown("## ⚙️ 파라미터 설정")

    with st.expander("👷 인력", expanded=True):
        init_workers = st.number_input("초기 종업원 수 (명)", 1, 500, 80)
        reg_wage     = st.number_input("정규임금 (천원/시간)", 1, 20, 4)
        ot_wage      = st.number_input("초과근무임금 (천원/시간)", 1, 30, 6)
        hire_cost    = st.number_input("고용비용 (천원/인)", 0, 2000, 300)
        fire_cost    = st.number_input("해고비용 (천원/인)", 0, 2000, 500)
        work_days    = st.number_input("작업일수 (일/월)", 1, 31, 20)
        work_hours   = st.number_input("작업시간 (시간/일)", 1, 24, 8)
        max_ot       = st.number_input("초과시간 상한 (시간/인/월)", 0, 50, 10)
        std_time     = st.number_input("작업표준시간 (시간/개)", 1, 20, 4)

    with st.expander("📦 재고/생산"):
        init_inv     = st.number_input("초기재고 (개)", 0, 10000, 1000)
        final_inv    = st.number_input("최종재고 목표 (개)", 0, 5000, 500)
        inv_cost     = st.number_input("재고유지비 (천원/개/월)", 0, 50, 2)
        backlog_cost = st.number_input("부재고비용 (천원/개/월)", 0, 50, 5)
        mat_cost     = st.number_input("재료비 (천원/개)", 0, 100, 10)
        sub_cost     = st.number_input("하청비용 (천원/개)", 0, 200, 30)

    st.markdown("## 🔧 최적화 설정")
    model_type = st.radio("모델 유형", ["LP (선형계획)", "IP (정수계획)"],
                          index=0, horizontal=True)
    model_type_key = "LP" if model_type.startswith("LP") else "IP"

    run_btn = st.button("🚀 최적화 실행", use_container_width=True)


# ── 파라미터 딕셔너리 ─────────────────────────────────────────
params = dict(
    init_workers=init_workers,
    reg_wage=reg_wage,
    ot_wage=ot_wage,
    hire_cost=hire_cost,
    fire_cost=fire_cost,
    work_days=work_days,
    work_hours=work_hours,
    max_ot=max_ot,
    std_time=std_time,
    init_inv=init_inv,
    final_inv=final_inv,
    inv_cost=inv_cost,
    backlog_cost=backlog_cost,
    mat_cost=mat_cost,
    sub_cost=sub_cost,
)


# ── 헤더 ──────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
  <div class="header-tag">Smart Manufacturing · S&amp;OP</div>
  <h1>총괄생산계획 최적화 시스템</h1>
  <p>Pyomo 기반 원예장비 제조업체 총괄생산계획(APP) · Aggregate Production Planning</p>
</div>
""", unsafe_allow_html=True)


# ── 세션 상태 초기화 ──────────────────────────────────────────
if 'result' not in st.session_state:
    st.session_state.result = None
    st.session_state.demand = demand_inputs
    st.session_state.status = None

if run_btn:
    with st.spinner("최적화 중..."):
        res, status = solve_app(params, demand_inputs, model_type_key)
    st.session_state.result = res
    st.session_state.demand = demand_inputs
    st.session_state.status = status

result = st.session_state.result
demand = st.session_state.demand
status = st.session_state.status


# ── 결과 없을 때 안내 ─────────────────────────────────────────
if result is None and status is None:
    st.info("👈 왼쪽 사이드바에서 수요와 파라미터를 설정한 후 **최적화 실행** 버튼을 누르세요.")

    # 기본 수요 미리보기
    st.markdown('<div class="section-header">수요 미리보기</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months(len(demand_inputs)), y=demand_inputs,
        marker_color=COLORS['blue'], opacity=0.8, name='예상수요'
    ))
    fig.update_layout(**CHART_LAYOUT, title='', height=280)
    st.plotly_chart(fig, use_container_width=True)
    st.stop()

elif result is None:
    st.markdown(f"""<div class="infeasible-banner">
    ⚠️ 최적해를 찾지 못했습니다 — 상태: <code>{status}</code><br>
    파라미터 또는 수요를 조정한 후 다시 실행해 주세요.
    </div>""", unsafe_allow_html=True)
    st.stop()


# ── 결과 파싱 ─────────────────────────────────────────────────
TH = len(demand)
T_range = range(1, TH + 1)
mo = months(TH)

W = result['W']
H = result['H']
L = result['L']
P = result['P']
I = result['I']
S = result['S']
C = result['C']
O = result['O']

# None 안전 처리 헬퍼
def n(v): return v if v is not None else 0.0

# 비용 분해
reg_wage_val = params['reg_wage'] * params['work_hours'] * params['work_days']
cost_reg  = [reg_wage_val           * n(W[t]) for t in T_range]
cost_ot   = [params['ot_wage']      * n(O[t]) for t in T_range]
cost_hire = [params['hire_cost']    * n(H[t]) for t in T_range]
cost_fire = [params['fire_cost']    * n(L[t]) for t in T_range]
cost_inv  = [params['inv_cost']     * n(I[t]) for t in T_range]
cost_back = [params['backlog_cost'] * n(S[t]) for t in T_range]
cost_mat  = [params['mat_cost']     * n(P[t]) for t in T_range]
cost_sub  = [params['sub_cost']     * n(C[t]) for t in T_range]

total_cost   = result['cost']
total_hire_n = sum(n(H[t]) for t in T_range)
total_fire_n = sum(n(L[t]) for t in T_range)
max_backlog  = max(n(S[t]) for t in T_range)
service_rate = 1 - sum(n(S[t]) for t in T_range) / (sum(demand) + 1e-9)


# ── KPI 카드 ─────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">총 비용</div>
    <div class="kpi-value">{total_cost/1e6:.1f}</div>
    <div class="kpi-unit">백만 원 (천원 기준)</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-label">서비스율</div>
    <div class="kpi-value">{service_rate*100:.1f}</div>
    <div class="kpi-unit">% (부재고 제외 비율)</div>
  </div>
  <div class="kpi-card yellow">
    <div class="kpi-label">총 고용 인원</div>
    <div class="kpi-value">{total_hire_n:.0f}</div>
    <div class="kpi-unit">명 (기간 합계)</div>
  </div>
  <div class="kpi-card {"red" if total_fire_n > 0 else "green"}">
    <div class="kpi-label">총 해고 인원</div>
    <div class="kpi-value">{total_fire_n:.0f}</div>
    <div class="kpi-unit">명 (기간 합계)</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="feasible-banner">✅ 최적해 도출 완료 — {model_type_key} 모델 · 총 비용 <strong>{total_cost:,.0f} 천원</strong></div>',
            unsafe_allow_html=True)
st.markdown("")

# ── 탭 ───────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 생산·수요 분석",
    "👷 인력 계획",
    "📦 재고 현황",
    "💰 비용 분석",
    "📋 상세 결과표",
])


# ═══════════════════════════════════════════════════════════
# TAB 1 — 생산·수요 분석
# ═══════════════════════════════════════════════════════════
with tab1:
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown('<div class="section-header">수요 vs 생산 vs 하청</div>',
                    unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=mo, y=[demand[i] for i in range(TH)],
            name='수요', marker_color=COLORS['blue'], opacity=0.7
        ))
        fig.add_trace(go.Bar(
            x=mo, y=[n(P[t]) for t in T_range],
            name='생산량', marker_color=COLORS['green'], opacity=0.85
        ))
        fig.add_trace(go.Bar(
            x=mo, y=[n(C[t]) for t in T_range],
            name='하청', marker_color=COLORS['orange'], opacity=0.85
        ))
        fig.add_trace(go.Scatter(
            x=mo, y=[demand[i] for i in range(TH)],
            name='수요선', mode='lines+markers',
            line=dict(color='#fff', width=2, dash='dot'),
            marker=dict(size=6, color='#fff')
        ))
        fig.update_layout(**CHART_LAYOUT, barmode='overlay', height=320)
        fig.update_layout(yaxis_title='수량 (개)')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">총 공급 구성</div>',
                    unsafe_allow_html=True)
        total_prod = sum(P[t] for t in T_range)
        total_sub  = sum(C[t] for t in T_range)
        total_dem  = sum(demand)
        fig2 = go.Figure(go.Pie(
            labels=['자체생산', '하청', '초기재고활용'],
            values=[total_prod, total_sub,
                    max(0, total_dem - total_prod - total_sub)],
            hole=0.55,
            marker_colors=[COLORS['green'], COLORS['orange'], COLORS['cyan']],
            textfont=dict(color='#fff', size=11),
        ))
        fig2.update_layout(**CHART_LAYOUT, height=320, showlegend=True)
        fig2.update_layout(legend=dict(orientation='h', y=-0.1))
        st.plotly_chart(fig2, use_container_width=True)

    # 초과근무
    st.markdown('<div class="section-header">초과근무 시간</div>', unsafe_allow_html=True)
    max_ot_list = [params['max_ot'] * n(W[t]) for t in T_range]
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=mo, y=[n(O[t]) for t in T_range],
        name='실제 초과근무', marker_color=COLORS['yellow'], opacity=0.85
    ))
    fig3.add_trace(go.Scatter(
        x=mo, y=max_ot_list, name='초과근무 한도',
        mode='lines', line=dict(color=COLORS['red'], width=2, dash='dash')
    ))
    fig3.update_layout(**CHART_LAYOUT, height=240)
    fig3.update_layout(yaxis_title='시간 (Hr/월)')
    st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# TAB 2 — 인력 계획
# ═══════════════════════════════════════════════════════════
with tab2:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-header">월별 종업원 수 추이</div>',
                    unsafe_allow_html=True)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(
            x=mo, y=[n(W[t]) for t in T_range],
            name='종업원 수', mode='lines+markers',
            line=dict(color=COLORS['blue'], width=3),
            marker=dict(size=8, symbol='circle', color=COLORS['blue'])
        ), secondary_y=False)
        fig.add_trace(go.Bar(
            x=mo, y=[n(H[t]) for t in T_range],
            name='신규 고용', marker_color=COLORS['green'], opacity=0.7
        ), secondary_y=True)
        fig.add_trace(go.Bar(
            x=mo, y=[-n(L[t]) for t in T_range],
            name='해고', marker_color=COLORS['red'], opacity=0.7
        ), secondary_y=True)
        fig.update_layout(**CHART_LAYOUT, height=320, barmode='overlay')
        fig.update_yaxes(title_text='종업원 수 (명)', secondary_y=False,
                         gridcolor='#2e2e2e', color='#525252')
        fig.update_yaxes(title_text='고용/해고 (명)', secondary_y=True, color='#525252')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">인력 변동 분석</div>',
                    unsafe_allow_html=True)
        net_change = [n(H[t]) - n(L[t]) for t in T_range]
        colors_bar = [COLORS['green'] if v >= 0 else COLORS['red'] for v in net_change]
        fig2 = go.Figure(go.Bar(
            x=mo, y=net_change,
            marker_color=colors_bar, opacity=0.85, name='순변동'
        ))
        fig2.add_hline(y=0, line_color='#525252', line_width=1)
        fig2.update_layout(**CHART_LAYOUT, height=320)
        fig2.update_layout(yaxis_title='순 인력 변동 (명)')
        st.plotly_chart(fig2, use_container_width=True)

    # 인력 용량 가동률
    st.markdown('<div class="section-header">생산 가동률 (capacity utilization)</div>',
                unsafe_allow_html=True)
    prod_per_w = params['work_days'] * params['work_hours'] / params['std_time']
    max_cap = [prod_per_w * W[t] + params['max_ot'] * W[t] / params['std_time']
               for t in T_range]
    reg_cap = [prod_per_w * n(W[t]) for t in T_range]
    util_reg = [P[t] / reg_cap[i] * 100 if reg_cap[i] > 0 else 0
                for i, t in enumerate(T_range)]

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=mo, y=util_reg, name='정규시간 가동률(%)',
        marker_color=COLORS['cyan'], opacity=0.8
    ))
    fig3.add_hline(y=100, line_color=COLORS['yellow'],
                   line_dash='dash', annotation_text='정규시간 100%')
    fig3.update_layout(**CHART_LAYOUT, height=240)
    fig3.update_layout(yaxis_title='가동률 (%)')
    st.plotly_chart(fig3, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# TAB 3 — 재고 현황
# ═══════════════════════════════════════════════════════════
with tab3:
    c1, c2 = st.columns([3, 2])

    with c1:
        st.markdown('<div class="section-header">재고 & 부족재고 추이</div>',
                    unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=['초기'] + mo, y=I,
            name='재고', mode='lines+markers',
            line=dict(color=COLORS['green'], width=3),
            fill='tozeroy', fillcolor='rgba(66,190,101,0.1)',
            marker=dict(size=7)
        ))
        fig.add_trace(go.Scatter(
            x=['초기'] + mo, y=S,
            name='부족재고(backlog)', mode='lines+markers',
            line=dict(color=COLORS['red'], width=2, dash='dash'),
            marker=dict(size=7, symbol='diamond')
        ))
        fig.add_hline(y=params['final_inv'], line_color=COLORS['yellow'],
                      line_dash='dot',
                      annotation_text=f"최종목표 {params['final_inv']}개")
        fig.update_layout(**CHART_LAYOUT, height=340)
        fig.update_layout(yaxis_title='수량 (개)')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">월말 재고 수준</div>',
                    unsafe_allow_html=True)
        inv_colors = []
        for t in T_range:
            if S[t] > 0:
                inv_colors.append(COLORS['red'])
            elif I[t] < params['final_inv'] * 0.5:
                inv_colors.append(COLORS['yellow'])
            else:
                inv_colors.append(COLORS['green'])

        fig2 = go.Figure(go.Bar(
            x=mo, y=[I[t] for t in T_range],
            marker_color=inv_colors, opacity=0.85, name='월말재고'
        ))
        fig2.update_layout(**CHART_LAYOUT, height=340)
        fig2.update_layout(yaxis_title='재고 (개)')
        st.plotly_chart(fig2, use_container_width=True)

    # 재고 상태 요약
    st.markdown('<div class="section-header">재고 상태 요약</div>', unsafe_allow_html=True)
    inv_data = []
    for i, t in enumerate(T_range):
        inv_level = I[t]
        shortage  = S[t]
        if shortage > 0:
            badge = '<span class="badge badge-err">부재고</span>'
        elif inv_level < params['final_inv'] * 0.5:
            badge = '<span class="badge badge-warn">낮음</span>'
        else:
            badge = '<span class="badge badge-ok">정상</span>'
        inv_data.append((mo[i], f"{inv_level:,.0f}", f"{shortage:,.0f}", badge))

    rows = "".join(
        f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>"
        for r in inv_data
    )
    st.markdown(f"""
    <table class="styled-table">
      <thead><tr>
        <th>월</th><th>월말재고(개)</th><th>부족재고(개)</th><th>상태</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB 4 — 비용 분석
# ═══════════════════════════════════════════════════════════
with tab4:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="section-header">비용 구성 (월별 누적)</div>',
                    unsafe_allow_html=True)
        cost_labels = ['정규임금', '초과근무', '고용비', '해고비',
                       '재고유지', '부재고비', '재료비', '하청비']
        cost_total_each = [
            sum(cost_reg), sum(cost_ot), sum(cost_hire), sum(cost_fire),
            sum(cost_inv), sum(cost_back), sum(cost_mat), sum(cost_sub)
        ]
        cost_colors = [COLORS['blue'], COLORS['cyan'], COLORS['green'], COLORS['red'],
                       COLORS['teal'], COLORS['orange'], COLORS['yellow'], COLORS['purple']]
        fig = go.Figure(go.Pie(
            labels=cost_labels, values=cost_total_each,
            marker_colors=cost_colors, hole=0.5,
            textfont=dict(color='#fff', size=10)
        ))
        fig.update_layout(**CHART_LAYOUT, height=340)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown('<div class="section-header">월별 비용 스택</div>',
                    unsafe_allow_html=True)
        fig2 = go.Figure()
        cost_series = [cost_reg, cost_ot, cost_hire, cost_fire,
                       cost_inv, cost_back, cost_mat, cost_sub]
        for lbl, series, col in zip(cost_labels, cost_series, cost_colors):
            fig2.add_trace(go.Bar(
                x=mo, y=series, name=lbl,
                marker_color=col, opacity=0.85
            ))
        fig2.update_layout(**CHART_LAYOUT, barmode='stack', height=340)
        fig2.update_layout(yaxis_title='비용 (천원)')
        st.plotly_chart(fig2, use_container_width=True)

    # 비용 비율 표
    st.markdown('<div class="section-header">비용 항목별 상세</div>',
                unsafe_allow_html=True)
    rows2 = ""
    for lbl, val in zip(cost_labels, cost_total_each):
        pct = val / total_cost * 100 if total_cost > 0 else 0
        bar_w = int(pct * 2)
        rows2 += f"""<tr>
          <td>{lbl}</td>
          <td class="highlight">{val:,.0f}</td>
          <td>{pct:.1f}%
            <span style="display:inline-block;width:{bar_w}px;height:6px;
            background:var(--primary);border-radius:2px;margin-left:6px;vertical-align:middle;"></span>
          </td>
        </tr>"""
    st.markdown(f"""
    <table class="styled-table">
      <thead><tr><th>비용 항목</th><th>합계 (천원)</th><th>비율</th></tr></thead>
      <tbody>{rows2}
      <tr style="border-top:2px solid var(--border)">
        <td><strong>합계</strong></td>
        <td class="highlight"><strong>{total_cost:,.0f}</strong></td>
        <td>100%</td>
      </tr>
      </tbody>
    </table>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB 5 — 상세 결과표
# ═══════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">월별 최적화 결과 요약</div>',
                unsafe_allow_html=True)

    header = "<tr><th>월</th><th>수요</th><th>종업원</th><th>고용</th><th>해고</th><th>생산</th><th>하청</th><th>잔업(Hr)</th><th>재고</th><th>부재고</th></tr>"
    rows3 = ""
    for i, t in enumerate(T_range):
        s_class = ' class="alert"' if S[t] > 0 else ''
        rows3 += f"""<tr>
          <td>{mo[i]}</td>
          <td>{demand[i]:,.0f}</td>
          <td>{n(W[t]):.1f}</td>
          <td class="highlight">{n(H[t]):.1f}</td>
          <td class="alert">{n(L[t]):.1f}</td>
          <td>{n(P[t]):,.1f}</td>
          <td>{n(C[t]):,.1f}</td>
          <td>{n(O[t]):,.1f}</td>
          <td>{n(I[t]):,.1f}</td>
          <td{s_class}>{n(S[t]):,.1f}</td>
        </tr>"""

    st.markdown(f"""
    <table class="styled-table">
      <thead>{header}</thead>
      <tbody>{rows3}</tbody>
    </table>
    """, unsafe_allow_html=True)

    # CSV 다운로드
    df_export = pd.DataFrame({
        '월': mo,
        '수요': [demand[i] for i in range(TH)],
        '종업원수': [n(W[t]) for t in T_range],
        '고용': [n(H[t]) for t in T_range],
        '해고': [n(L[t]) for t in T_range],
        '생산량': [n(P[t]) for t in T_range],
        '하청': [n(C[t]) for t in T_range],
        '잔업시간': [n(O[t]) for t in T_range],
        '재고': [I[t] for t in T_range],
        '부재고': [S[t] for t in T_range],
        '총비용': [sum([cost_reg[i], cost_ot[i], cost_hire[i], cost_fire[i],
                       cost_inv[i], cost_back[i], cost_mat[i], cost_sub[i]])
                  for i in range(TH)],
    })
    st.markdown("")
    st.download_button(
        label="📥 결과 CSV 다운로드",
        data=df_export.to_csv(index=False, encoding='utf-8-sig'),
        file_name="총괄생산계획_결과.csv",
        mime="text/csv",
    )

    # 파라미터 요약
    st.markdown('<div class="section-header">사용된 파라미터</div>',
                unsafe_allow_html=True)
    param_rows = "".join(
        f"<tr><td>{k}</td><td class='highlight'>{v}</td></tr>"
        for k, v in params.items()
    )
    st.markdown(f"""
    <table class="styled-table">
      <thead><tr><th>파라미터</th><th>값</th></tr></thead>
      <tbody>{param_rows}</tbody>
    </table>
    """, unsafe_allow_html=True)
