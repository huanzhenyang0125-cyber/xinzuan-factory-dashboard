from pathlib import Path
import base64
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="工厂经营管理工作台", layout="wide", initial_sidebar_state="expanded")

DATA = [
    (2020, None, 70042, 43122.86, None),
    (2021, None, 200207, 112340, None),
    (2022, 28598629.76, 189679, 142478, None),
    (2023, 26171504.06, 216858, 61600, None),
    (2024, 23910255.3510725, 212299, 13740, 1908),
    (2025, 22755388.7497971, 151659.5, None, 40678),
    (2026, 22630283.7135, 197555.5, None, 31400),
]

def cash(value):
    return "未记录" if value is None else f"{value / 10000:,.2f} 万元"

def proportion(numerator, denominator):
    return "无法计算" if denominator is None or denominator == 0 else f"{numerator / denominator:.2%}"

def total(row):
    return sum(value for value in row[2:] if value is not None)

for key, value in {'page':'经营概览','sales_adjust':0,'cost_adjust':0}.items():
    st.session_state.setdefault(key,value)
st.session_state.setdefault('menu_collapsed',False)

def toggle_menu():
    st.session_state.menu_collapsed=not st.session_state.menu_collapsed

def navigate(page):
    st.session_state.page=page

def remember(control,business):
    st.session_state[business]=st.session_state[control]

def reset_model():
    for key in ['sales_adjust','cost_adjust','sales_slider','cost_slider','sales_number','cost_number']:
        st.session_state[key]=0

@st.cache_data
def company_font():
    return base64.b64encode((Path(__file__).parent/'assets'/'company.woff').read_bytes()).decode()

st.html('<style>@font-face{font-family:CompanyText;src:url(data:font/woff;base64,'+company_font()+') format("woff");font-display:swap;}'+'''
html,body,.stApp{font-family:CompanyText,sans-serif;color:#10131a}
.stApp{background:radial-gradient(ellipse at 96% 0%,rgba(39,133,255,.23) 0,transparent 43%),radial-gradient(ellipse at 12% 100%,rgba(97,184,255,.15) 0,transparent 40%),#fbfdff}
[data-testid="stHeader"]{background:transparent}[data-testid="stToolbar"]{display:none}
[data-testid="stSidebar"]{position:fixed!important;left:0!important;top:0!important;bottom:0!important;transform:none!important;visibility:visible!important;z-index:100!important;background:rgba(255,255,255,.54)!important;border-right:1px solid rgba(255,255,255,.94);backdrop-filter:blur(22px) saturate(140%)}
[data-testid="stSidebarCollapseButton"],[data-testid="stSidebarCollapsedControl"]{display:none!important}
[data-testid="stSidebarUserContent"]{padding:24px 14px!important}
.block-container{padding:36px 34px 50px!important;max-width:1500px}
h1{font-family:CompanyText!important;font-size:27px!important;font-weight:600!important;letter-spacing:.03em!important;color:#10131a!important;margin-bottom:20px!important}
h3{font-family:CompanyText!important;font-size:16px!important;font-weight:600!important;color:#131720!important}
p,label,button,input,[data-testid="stMetricValue"],[data-testid="stMetricLabel"]{font-family:CompanyText!important}
.brand{font-size:24px;letter-spacing:.18em;color:#075ef0;margin:8px 0 28px;font-weight:600}.brand-sub{display:none}
[data-testid="stSidebar"] button{justify-content:flex-start;min-height:44px;border-radius:9px;border:0!important;box-shadow:none!important;transition:transform .25s cubic-bezier(.16,1.4,.3,1),background .2s}
[data-testid="stSidebar"] button[kind="primary"]{background:#0866ff!important;color:#fff!important}
[data-testid="stSidebar"] button[kind="secondary"]{background:transparent;color:#242a35}
[data-testid="stSidebar"] button:hover{background:#e5f0ff!important}[data-testid="stSidebar"] button:active{transform:scale(.97)}
.st-key-glass_sim,.st-key-glass_history,.st-key-glass_ring,.st-key-glass_data,.st-key-glass_forecast{background:linear-gradient(135deg,rgba(255,255,255,.66),rgba(255,255,255,.31))!important;border:1px solid rgba(255,255,255,.96)!important;border-radius:18px!important;padding:24px!important;backdrop-filter:blur(22px) saturate(145%)!important;box-shadow:0 14px 38px rgba(21,91,174,.08),inset 0 2px 2px rgba(255,255,255,.98),inset 0 -1px 1px rgba(82,159,249,.10)!important}
.st-key-glass_sim{margin:18px 0}.st-key-glass_history,.st-key-glass_ring{margin:10px 0}
[data-testid="stMetric"]{padding:10px 0 20px!important;min-height:0;background:none!important;border:0!important;box-shadow:none!important}
[data-testid="stMetricLabel"] p{font-size:13px!important;color:#3d4652!important;font-weight:400!important}
[data-testid="stMetricValue"]{font-size:31px!important;color:#10131a;font-weight:500;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
[data-testid="stMetricValue"]>div{overflow:visible!important;white-space:normal!important;text-overflow:clip!important}
.ring-wrap{display:flex;justify-content:center;padding:16px 0 24px}.glass-ring{width:185px;height:185px;border-radius:50%;padding:20px;box-shadow:inset 0 2px 5px #ffffff88,0 8px 20px #65859a18}.ring-core{height:100%;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(255,255,255,.88);backdrop-filter:blur(16px)}.ring-core b{font-size:29px;font-weight:500;color:#111725}.ring-core small{font-size:12px;color:#45515f;margin-top:6px}.legend-row{display:flex;justify-content:space-between;padding:8px 0;font-size:13px;color:#252e3b}.legend-row i{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:8px}.legend-row b{font-weight:500}
.st-key-side_toggle button{min-height:32px!important;color:#667f90!important}.model-panel{padding:25px 0}.model-panel h2{font-size:22px}.model-panel p,.chips{display:none}.model-pill{font-size:13px;color:#6c7d88}.model-ring{display:none}
@media(max-width:1100px){.block-container{padding:28px 22px!important}[data-testid="stMetricValue"]{font-size:24px!important}.st-key-glass_sim,.st-key-glass_history,.st-key-glass_ring{padding:18px!important}}
@media(max-width:600px){.block-container{padding:22px 12px!important}[data-testid="stMetricValue"]{font-size:21px!important}}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}

[data-testid="stSidebar"] button[kind="primary"] p{color:#fff!important}
[data-testid="stSidebar"] button[kind="primary"]:hover{background:#0055df!important}
.st-key-reset_model button{border:1px solid rgba(8,102,255,.2)!important;background:rgba(255,255,255,.6)!important;border-radius:12px;color:#0758d1;box-shadow:inset 0 1px 1px white;min-height:40px}
.st-key-reset_model button:hover{background:#0866ff!important;color:white!important}
.st-key-reset_model button:hover p{color:white!important}
[data-testid="stNumberInput"] input{color:#111725!important;background:rgba(255,255,255,.54)!important;font-variant-numeric:tabular-nums}
[data-testid="stSlider"] p{color:#202733!important}
[data-testid="stSlider"] [data-testid="stTickBar"]{color:#465364}
button:focus-visible,input:focus-visible{outline:2px solid #0866ff!important;outline-offset:3px}
.glass-ring{box-shadow:inset 0 2px 5px rgba(255,255,255,.7),0 10px 25px rgba(8,102,255,.16)}
.ring-core{background:linear-gradient(145deg,rgba(255,255,255,.96),rgba(242,249,255,.73));box-shadow:inset 0 2px 10px rgba(8,102,255,.035),0 1px 5px rgba(255,255,255,.9)}
::selection{background:#c6e1ff;color:#10131a}
</style>''')

with st.sidebar:
    st.button('' if st.session_state.menu_collapsed else '收起菜单',icon=':material/chevron_right:' if st.session_state.menu_collapsed else ':material/chevron_left:',key='side_toggle',help='展开菜单' if st.session_state.menu_collapsed else '收起菜单',on_click=toggle_menu,width='stretch')
    st.html('<div class="brand">新钻</div><div class="brand-sub">工厂管理工作台</div>')
    for title,key,icon in [('经营概览','overview',':material/dashboard:'),('采购分析','trend',':material/bar_chart:'),('预算测算','model',':material/tune:'),('质量预测','forecast',':material/model_training:'),('年度台账','data',':material/table_chart:')]:
        st.button('' if st.session_state.menu_collapsed else title,help=title,icon=icon,key='nav_'+key,type='primary' if st.session_state.page==title else 'secondary',width='stretch',on_click=navigate,args=(title,))
    st.write("")
    year = st.selectbox("年度", [2026, 2025, 2024, 2023, 2022, 2021, 2020], index=1, format_func=lambda v: f"{v} 年")

width=76 if st.session_state.menu_collapsed else 200
st.html(f'<style>[data-testid="stSidebar"]{{width:{width}px!important;min-width:{width}px!important;max-width:{width}px!important}}[data-testid="stMain"]{{margin-left:{width}px!important;width:calc(100% - {width}px)!important}}'+('[data-testid="stSidebar"] [data-testid="stSelectbox"]{display:none}.brand{display:none}' if st.session_state.menu_collapsed else '')+'</style>')
page=st.session_state.page

row = next(item for item in DATA if item[0] == year)
amount = total(row)
st.title(page)

def metrics():
    cols = st.columns(3, gap="medium")
    cols[0].metric("销售额", cash(row[1]))
    cols[1].metric("采购金额", cash(amount), help="仅汇总已录入项目")
    cols[2].metric("采购销售比", proportion(amount, row[1]))
    if year == 2026:
        st.caption("2026 年统计范围待确认")

def bar_chart():
    choice = st.segmented_control("查看指标", ["销售额", "采购金额"], default="采购金额", label_visibility="collapsed", key="chart_choice")
    vals = [(r[1] if choice == "销售额" else total(r)) for r in DATA]
    fig = go.Figure(go.Bar(x=[str(r[0]) for r in DATA], y=[None if v is None else v/10000 for v in vals],
                           marker_color=["#0866ff" if r[0] == year else "#9acaff" for r in DATA],
                           text=["未记录" if v is None else f"{v/10000:,.1f}" for v in vals], textposition="outside",
                           hovertemplate="%{x} 年<br>%{y:,.2f} 万元<extra></extra>"))
    fig.update_layout(height=330, margin=dict(l=0,r=12,t=25,b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family='CompanyText',color='#263442'), showlegend=False, yaxis=dict(title="万元", showgrid=True, gridcolor="#e7f0f6", zeroline=False), xaxis=dict(showgrid=False, tickmode="linear"), bargap=.57)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar":False}, key="bar")

def donut_chart():
    labels = ["油漆采购", "兴源", "油墨采购"]
    colors=['#0866ff','#4da7ff','#b8e4ff']
    stops=[]
    acc=0
    for i,value in enumerate(row[2:]):
        if value is not None:
            nxt=acc+value/amount*100
            stops.append(f'{colors[i]} {acc}% {nxt}%')
            acc=nxt
    st.html(f'<div class="ring-wrap"><div class="glass-ring" style="background:conic-gradient({",".join(stops)})"><div class="ring-core"><b>{amount/10000:,.2f}</b><small>万元</small></div></div></div>')
    for label,color,value in zip(labels,colors,row[2:]):
        text='未记录' if value is None else f'{value:,.2f} 元'
        st.html(f'<div class="legend-row"><span><i style="background:{color}"></i>{label}</span><b>{text}</b></div>')

def simulation():
    with st.container(key='glass_sim'):
        heading,reset_col=st.columns([5,1],vertical_alignment='center')
        heading.subheader('预算测算')
        reset_col.button('恢复原值',key='reset_model',on_click=reset_model,width='stretch')
        a,b=st.columns(2,gap='large')
        for col,label,business,slider,number in [(a,'销售增减','sales_adjust','sales_slider','sales_number'),(b,'采购增减','cost_adjust','cost_slider','cost_number')]:
            with col:
                st.session_state[slider]=st.session_state[business]
                st.session_state[number]=st.session_state[business]
                left,right=st.columns([4,1])
                left.slider(label,-50,50,key=slider,format='%d%%',on_change=remember,args=(slider,business))
                right.number_input(label+'（%）',-50,50,key=number,label_visibility='hidden',on_change=remember,args=(number,business))
                base=row[1] if business=='sales_adjust' else amount
                adjusted=None if base is None else base*(1+st.session_state[business]/100)
                chart=go.Figure(go.Bar(x=['原值','测算值'],y=[None if v is None else v/10000 for v in [base,adjusted]],marker_color=['#b9d9ff','#0866ff'],text=['未记录' if v is None else f'{v/10000:,.2f}' for v in [base,adjusted]],textposition='outside',hovertemplate='%{x}<br>%{y:,.2f} 万元<extra></extra>'))
                chart.update_layout(height=230,margin=dict(l=0,r=12,t=28,b=0),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font=dict(family='CompanyText',color='#263442',size=12),bargap=.57,yaxis=dict(title='万元',gridcolor='#eaf0f4',zeroline=False),xaxis=dict(fixedrange=True),showlegend=False)
                st.plotly_chart(chart,width='stretch',key='budget_'+business,config={'displayModeBar':False},alt=label+'测算柱状图')
        assumed_sales=None if row[1] is None else row[1]*(1+st.session_state.sales_adjust/100)
        assumed_purchase=amount*(1+st.session_state.cost_adjust/100)
        st.caption('测算采购销售比　'+proportion(assumed_purchase,assumed_sales))
        

if page == "经营概览":
    metrics()
    simulation()
    left,right=st.columns([1.4,1],gap="medium")
    with left:
        with st.container(key='glass_history'):
            st.subheader("年度趋势")
            bar_chart()
    with right:
        with st.container(key='glass_ring'):
            st.subheader("采购构成")
            donut_chart()
elif page == "采购分析":
    metrics()
    with st.container(key='glass_history'):
        st.subheader("年度趋势")
        bar_chart()
    
elif page == "预算测算":
    metrics()
    simulation()
elif page == "质量预测":
    with st.container(key='glass_forecast'):
        st.caption('生产数据待接入')
else:
    rows=[]
    for r in reversed(DATA):
        def fmt(v): return "未记录" if v is None else f"{v:,.2f}"
        rows.append({"年份":str(r[0]),"销售额（元）":fmt(r[1]),"油漆（元）":fmt(r[2]),"兴源（元）":fmt(r[3]),"油墨（元）":fmt(r[4]),"已记录合计（元）":fmt(total(r)),"占销售额":proportion(total(r),r[1])})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch", alt="年度经营台账")
