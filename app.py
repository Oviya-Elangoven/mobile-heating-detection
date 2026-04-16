import streamlit as st
import plotly.graph_objects as go
import numpy as np

# -----------------------------
# SENSORS
# -----------------------------
from cpu_sensor import get_cpu_usage
from charging_sensor import get_charging_intensity
from temp_sensor import get_cpu_temp

# -----------------------------
# AI SYSTEMS
# -----------------------------
from fuzzy_logic import compute_risk, generate_surface
from ml_model import predict_risk

# -----------------------------
# DATABASE + ALERTS
# -----------------------------
from database import log_data, get_history
from alert_system import check_alert


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI Thermal Analytics",
    page_icon="🔥",
    layout="wide"
)

# -------------------------------------------------
# FULL DARK UI CSS
# -------------------------------------------------
st.markdown("""
<style>

/* Remove white header */
header {visibility: hidden;}
[data-testid="stHeader"] {background: transparent;}

.block-container {padding-top: 0rem;}

/* Background */
html, body, .stApp {
    background: linear-gradient(135deg,#020617,#0f172a,#1e293b);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Hover glow */
div[data-testid="column"] > div:hover {
    transform: scale(1.02);
    transition: 0.3s;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("AI Thermal Risk Analytics Dashboard")
st.caption("Real-Time Fuzzy + Machine Learning Thermal Monitoring")

# -------------------------------------------------
# SENSOR DATA
# -------------------------------------------------
cpu = get_cpu_usage()
temp = get_cpu_temp()
charging = get_charging_intensity()

# -------------------------------------------------
# AI COMPUTATION
# -------------------------------------------------
fuzzy_risk = compute_risk(cpu, temp, charging)
ml_risk = predict_risk(cpu, temp, charging)

# -------------------------------------------------
# DATABASE LOGGING
# -------------------------------------------------
log_data(cpu, temp, charging, fuzzy_risk, ml_risk)

# -------------------------------------------------
# ALERT SYSTEM
# -------------------------------------------------
check_alert(fuzzy_risk)

# -------------------------------------------------
# RISK STATUS
# -------------------------------------------------
if fuzzy_risk < 35:
    status = "SAFE"
elif fuzzy_risk < 65:
    status = "WARNING"
else:
    status = "DANGEROUS"

st.subheader(f"System Risk Status: {status}")

# -------------------------------------------------
# EQUAL SIZE KPI CARD FUNCTION
# -------------------------------------------------
def bright_card(title, value, glow):

    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg,#0f172a,#1e293b);
        padding:25px;
        border-radius:18px;
        text-align:center;
        border:1px solid {glow};
        box-shadow:0 0 20px {glow}55;
        height:170px;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
    ">
        <h4 style='color:#94a3b8;margin-bottom:10px'>{title}</h4>
        <h1 style='color:{glow};margin:0'>{value}</h1>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# KPI ROW
# -------------------------------------------------
k1, k2, k3, k4, k5 = st.columns(5, gap="large")

with k1:
    bright_card("CPU Usage (%)", f"{cpu:.1f}", "#22c55e")

with k2:
    bright_card("Temperature (°C)", f"{temp:.1f}", "#38bdf8")

with k3:
    bright_card("Charging (%)", f"{charging:.0f}", "#f59e0b")

with k4:
    bright_card("Fuzzy Risk", f"{fuzzy_risk:.1f}", "#ef4444")

with k5:
    bright_card("ML Risk", f"{ml_risk:.1f}", "#a855f7")

# -------------------------------------------------
# GAUGE + RADAR
# -------------------------------------------------
col1, col2 = st.columns(2, gap="large")

with col1:

    st.subheader("Heating Risk Gauge")

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=fuzzy_risk,
        title={'text': ""},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#ef4444"},
            'steps': [
                {'range': [0, 35], 'color': "#22c55e"},
                {'range': [35, 65], 'color': "#f59e0b"},
                {'range': [65, 100], 'color': "#ef4444"}
            ],
        }
    ))

    gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(gauge, use_container_width=True)

with col2:

    st.subheader("Thermal Parameter Radar")

    radar = go.Figure()

    radar.add_trace(go.Scatterpolar(
        r=[cpu, temp, charging, fuzzy_risk],
        theta=["CPU","Temp","Charging","Risk"],
        fill='toself',
        line=dict(color="#60a5fa")
    ))

    radar.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)"),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(radar, use_container_width=True)

# -------------------------------------------------
# ML vs FUZZY COMPARISON
# -------------------------------------------------
st.subheader("AI Risk Model Comparison")

fig = go.Figure()

fig.add_trace(go.Bar(
    x=["Fuzzy Logic", "Machine Learning"],
    y=[fuzzy_risk, ml_risk],
    marker_color=["#ef4444", "#a855f7"]
))

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# TREND + 3D SURFACE
# -------------------------------------------------
col3, col4 = st.columns(2, gap="large")

with col3:

    st.subheader("Temperature Trend Analysis")

    trend = np.random.normal(temp, 1.3, 40)
    st.line_chart(trend)

with col4:

    st.subheader("3D Fuzzy Surface")

    X, Y, Z = generate_surface()

    surface = go.Figure(data=[go.Surface(x=X, y=Y, z=Z)])

    surface.update_layout(
        scene=dict(
            xaxis_title="CPU Usage",
            yaxis_title="Temperature",
            zaxis_title="Risk"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=420
    )

    st.plotly_chart(surface, use_container_width=True)

# -------------------------------------------------
# DATABASE HISTORY
# -------------------------------------------------
st.subheader("Thermal History Log")

data = get_history()

if data:
    temps = [d[2] for d in data]
    st.line_chart(temps)

# -------------------------------------------------
# COOLING RECOMMENDATIONS
# -------------------------------------------------
st.subheader("Cooling Recommendations")

recs = []

if cpu > 70:
    recs.append("Close heavy background applications")

if temp > 60:
    recs.append("Move device to cooler environment")

if charging > 70:
    recs.append("Disable fast charging temporarily")

if fuzzy_risk > 65:
    recs.append("Enable power saver mode")
    recs.append("Reduce display brightness")

if not recs:
    recs.append("System thermal condition is optimal")

for r in recs:
    st.info(f"👉 {r}")
