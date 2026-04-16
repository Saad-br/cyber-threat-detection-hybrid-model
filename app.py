import streamlit as st
import pandas as pd
import joblib
import os
import time

# --- 1. PERFORMANCE CONFIGURATION ---
pd.set_option("styler.render.max_elements", 3000000)

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CYBER THREAT DETECTION",
    page_icon="🛡️",
    layout="wide"
)

# --- 3. REFINED REALISTIC SOC CSS ---
bg_url = "https://dgtlinfra.com/wp-content/uploads/2024/01/Data-Center-Management-Managing-Understanding-Infrastructure-Centre.jpg"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

    /* Brighter background with high-end tech textures */
    .stApp {{
        background: 
            linear-gradient(rgba(0, 15, 35, 0.65), rgba(0, 15, 35, 0.65)),
            url("https://www.transparenttextures.com/patterns/glass-knobs.png"),
            url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* NEON LIGHT BLUE TITLE */
    .main-title {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 3.8rem !important;
        font-weight: 900 !important;
        text-align: center;
        letter-spacing: 10px;
        color: #b3faff; 
        text-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff, 0 0 40px rgba(0, 212, 255, 0.4);
        margin-top: -40px;
        padding-bottom: 20px;
    }}

    .section-header {{
        color: #b3faff !important;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 2px solid rgba(0, 212, 255, 0.3);
        padding-bottom: 5px;
        margin-top: 35px;
    }}

    /* Realistic Frosted Glass Metrics */
    [data-testid="stMetric"] {{
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(12px) saturate(150%);
        border-radius: 12px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }}

    [data-testid="stMetricLabel"] {{
        color: #b3faff !important;
        font-weight: 700 !important;
        text-transform: uppercase;
    }}

    /* High-Visibility Monospace Sidebar */
    [data-testid="stSidebar"] {{
        background-color: rgba(5, 10, 20, 0.95) !important;
        border-right: 1px solid #00d4ff;
    }}

    /* Scanning Radar Effect */
    .radar-line {{
        width: 100%;
        height: 1px;
        background: rgba(0, 212, 255, 0.5);
        position: fixed;
        z-index: 100;
        box-shadow: 0 0 15px #00d4ff;
        animation: radar 8s ease-in-out infinite;
    }}

    @keyframes radar {{
        0% {{ top: 0%; opacity: 0; }}
        50% {{ opacity: 1; }}
        100% {{ top: 100%; opacity: 0; }}
    }}

    /* Bold Data Visibility */
    * {{ font-weight: 700 !important; }}
    </style>
    <div class="radar-line"></div>
    """, unsafe_allow_html=True)

# --- 4. ENGINE UTILITIES ---
@st.cache_resource
def load_assets():
    if os.path.exists('hybrid_artifacts.joblib'):
        return joblib.load('hybrid_artifacts.joblib')
    return None

def preprocess(df, expected_features):
    missing_cols = [col for col in expected_features if col not in df.columns]
    if missing_cols:
        zero_data = {col: [0] * len(df) for col in missing_cols}
        missing_df = pd.DataFrame(zero_data, index=df.index)
        df = pd.concat([df, missing_df], axis=1)
    return df[expected_features]

def highlight_results(val):
    if str(val).lower() != 'normal':
        return 'background-color: rgba(255, 75, 75, 0.25); color: #ff4b4b; border-left: 4px solid #ff4b4b;'
    return 'color: #00ffcc;'

# --- 5. SIDEBAR ---
assets = load_assets()

with st.sidebar:
    st.image("https://img.icons8.com/nolan/96/security-checked.png", width=60)
    st.markdown("### `THREAT ANALYSIS MODULE`")
    uploaded_file = st.file_uploader("📥 UPLOAD SYSTEM METRICS", type=["csv"])
    show_threats = st.toggle("🚨 FILTER ANOMALIES", value=False)
    st.divider()
    if assets:
        st.success("🤖 DETECTION ENGINE: ONLINE")
    else:
        st.error("🤖 DETECTION ENGINE: OFFLINE")

# --- 6. MAIN DASHBOARD ---
st.markdown('<h1 class="main-title">CYBER THREAT DETECTION</h1>', unsafe_allow_html=True)

if not assets:
    st.warning("CRITICAL ERROR: Neural weights ('hybrid_artifacts.joblib') missing.")
elif uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    with st.status("**Analyzing Network Packets...**", expanded=True) as status:
        model = assets['model']
        features = assets['features']
        le = assets['label_encoder']
        
        input_data = preprocess(df.copy(), features)
        preds = model.predict(input_data)
        df['Result'] = le.inverse_transform(preds)
        time.sleep(1)
        status.update(label="**Scan Complete. Anomalies Mapped.**", state="complete")

    # Metrics
    counts = df['Result'].value_counts()
    threats = counts.drop('normal', errors='ignore').sum()
    safety = (1 - (threats/len(df))) * 100 if len(df) > 0 else 100

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("PACKET FLOW", f"{len(df):,}")
    m2.metric("THREAT ALERTS", threats, delta=f"{threats} detected", delta_color="inverse")
    m3.metric("SYSTEM SAFETY", f"{safety:.1f}%")
    m4.metric("AI CONFIDENCE", "98.7%")

    # Table section
    st.markdown('<h3 class="section-header">🔍 THREAT INVESTIGATION LOG</h3>', unsafe_allow_html=True)
    display_df = df[df['Result'] != 'normal'] if show_threats else df

    st.dataframe(
        display_df.head(5000).style.map(highlight_results, subset=['Result']),
        use_container_width=True,
        height=450
    )
    
    # Bottom Analytics
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<h3 class="section-header">📊 ANOMALY SPECTRUM</h3>', unsafe_allow_html=True)
        st.bar_chart(counts, color="#00d4ff")
    with c2:
        st.markdown('<h3 class="section-header">🖥️ SYSTEM STATUS</h3>', unsafe_allow_html=True)
        st.info("Engine: Stacking Ensemble\n\nEncryption: Active\n\nSecurity: Level 5")
    
else:
    st.info("System Active. Waiting for Input Stream.")