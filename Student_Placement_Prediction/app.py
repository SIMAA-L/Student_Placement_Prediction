import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import plotly.graph_objects as go
from database_functions import save_prediction, get_history

# ================= CONFIG =================
st.set_page_config(
    page_title="Placement Predictor V9 Pro",
    page_icon="🎓",
    layout="wide"
)

# ================= LOAD =================
df = pd.read_csv("data/placement_dataset.csv")
model = joblib.load("models/placement_model.pkl")

# ================= SIDEBAR =================
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Dashboard", "Prediction", "History"]
)

# ================= HOME =================
if page == "Home":
    st.title("🎓 Placement Prediction V9 PRO")
    st.success("System Running Successfully 🚀")

    st.markdown("""
    ### Features
    - 📊 Dashboard Analytics  
    - 🤖 ML Prediction  
    - 📜 History Tracking  
    - 📈 Visual Insights  
    """)

# ================= DASHBOARD =================
elif page == "Dashboard":
    st.title("📊 Placement Analytics Dashboard")

    total = len(df)
    placed = len(df[df["status"] == "Placed"])
    not_placed = len(df[df["status"] == "Not Placed"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", total)
    col2.metric("Placed", placed)
    col3.metric("Not Placed", not_placed)

    st.markdown("---")

    # ================= PIE CHART =================
    st.subheader("📌 Placement Distribution")

    fig1 = px.pie(
        names=["Placed", "Not Placed"],
        values=[placed, not_placed],
        hole=0.4
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ================= GENDER =================
    st.subheader("👨‍🎓 Gender vs Placement")

    fig2 = px.histogram(
        df,
        x="gender",
        color="status",
        barmode="group"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # ================= SSC =================
    st.subheader("📘 SSC % vs Placement")

    fig3 = px.box(
        df,
        x="status",
        y="ssc_p",
        color="status"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # ================= DEGREE =================
    st.subheader("🎓 Degree % vs Placement")

    fig4 = px.box(
        df,
        x="status",
        y="degree_p",
        color="status"
    )
    st.plotly_chart(fig4, use_container_width=True)

    # ================= MBA =================
    st.subheader("💼 MBA % Distribution")

    fig5 = px.violin(
        df,
        x="status",
        y="mba_p",
        color="status",
        box=True
    )
    st.plotly_chart(fig5, use_container_width=True)

# ================= PREDICTION =================
elif page == "Prediction":
    st.title("🎯 Prediction System")

    gender = st.selectbox("Gender", ["Male", "Female"])
    ssc_p = st.number_input("SSC %")
    ssc_b = st.selectbox("SSC Board", ["Central", "Others"])
    hsc_p = st.number_input("HSC %")
    hsc_b = st.selectbox("HSC Board", ["Central", "Others"])
    hsc_s = st.selectbox("Stream", ["Science", "Commerce", "Arts"])
    degree_p = st.number_input("Degree %")
    degree_t = st.selectbox("Degree Type", ["Sci&Tech", "Comm&Mgmt", "Others"])
    workex = st.selectbox("Work Experience", ["Yes", "No"])
    etest_p = st.number_input("Test %")
    specialisation = st.selectbox("MBA Specialisation", ["Mkt&Fin", "Mkt&HR"])
    mba_p = st.number_input("MBA %")

    if st.button("Predict"):

        # ================= ENCODING =================
        gender = 1 if gender == "Male" else 0
        ssc_b = 1 if ssc_b == "Others" else 0
        hsc_b = 1 if hsc_b == "Others" else 0
        workex = 1 if workex == "Yes" else 0

        hsc_s = {"Science": 2, "Commerce": 1, "Arts": 0}[hsc_s]
        degree_t = {"Sci&Tech": 2, "Comm&Mgmt": 1, "Others": 0}[degree_t]
        specialisation = {"Mkt&Fin": 0, "Mkt&HR": 1}[specialisation]

        # ⚠️ MUST MATCH TRAINING EXACTLY (12 FEATURES)
        input_data = [[
            gender,
            ssc_p,
            ssc_b,
            hsc_p,
            hsc_b,
            hsc_s,
            degree_p,
            degree_t,
            workex,
            etest_p,
            specialisation,
            mba_p
        ]]

        prediction = model.predict(input_data)[0]
        prob = model.predict_proba(input_data)[0][1] * 100

        result = "Placed" if prediction == 1 else "Not Placed"

        save_prediction(gender, ssc_p, hsc_p, degree_p, mba_p, result, prob)

        st.success(result)
        st.metric("Probability", f"{prob:.2f}%")

        # Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob,
            title={"text": "Placement Probability"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "blue"},
                "steps": [
                    {"range": [0, 50], "color": "#ffcccc"},
                    {"range": [50, 80], "color": "#fff3cd"},
                    {"range": [80, 100], "color": "#d4edda"}
                ]
            }
        ))

        st.plotly_chart(fig, use_container_width=True)

# ================= HISTORY =================
elif page == "History":
    st.title("📜 History")

    data = get_history()

    if data is None or data.empty:
        st.info("No history found")
    else:
        st.dataframe(data, use_container_width=True)

        st.download_button(
            "Download CSV",
            data.to_csv(index=False).encode(),
            "history.csv",
            "text/csv"
        )