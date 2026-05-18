import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Cricket Tagging Simulator", layout="wide")

st.title("🏏 Cricket Match Tagging Simulator")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = []

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# --- INPUT SECTION ---
st.header("🎯 Tag a Ball")

col1, col2, col3, col4 = st.columns(4)

with col1:
    over = st.text_input("Over (e.g., 2.3)")

with col2:
    delivery = st.selectbox("Delivery Type", ["Yorker","Full","Good Length","Short"])

with col3:
    shot = st.selectbox("Shot Type", ["Defensive","Drive","Pull","Cut","Sweep"])

with col4:
    outcome = st.selectbox("Outcome", ["0","1","2","3","4","6","Wicket"])

# --- TAG BUTTON ---
if st.button("✅ Tag Ball"):
    time_taken = round(time.time() - st.session_state.start_time, 2)

    st.session_state.data.append({
        "Over": over,
        "Delivery": delivery,
        "Shot": shot,
        "Outcome": outcome,
        "Time (s)": time_taken
    })

    # Reset timer
    st.session_state.start_time = time.time()

# --- DISPLAY DATA ---
df = pd.DataFrame(st.session_state.data)

st.header("📋 Tagged Data")
st.dataframe(df, use_container_width=True)

# --- ANALYTICS ---
if not df.empty:
    st.header("📊 Analytics")

    df_numeric = df.copy()
    df_numeric["Outcome"] = pd.to_numeric(df_numeric["Outcome"], errors="coerce")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Runs per Over")
        st.bar_chart(df_numeric.groupby("Over")["Outcome"].sum())

    with col2:
        st.subheader("Shot Distribution")
        st.bar_chart(df["Shot"].value_counts())

    # Speed indicator
    st.subheader("⚡ Tagging Speed")
    avg_time = df["Time (s)"].mean()
    st.metric("Average Time per Ball (seconds)", round(avg_time, 2))

    # Speed feedback
    if avg_time < 6:
        st.success("🔥 Great speed! Ready for live tagging")
    else:
        st.warning("⚠️ Try to tag faster (target < 6 sec)")