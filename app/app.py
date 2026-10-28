import os
import sys

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from src.prediction import predict_stress
from src.recommendations import generate_recommendations


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LUMINA AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main application */

    .stApp {
        background-color: #090a0d;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 45px;
        padding-bottom: 50px;
    }


    /* Sidebar */

    section[data-testid="stSidebar"] {
        background-color: #111216;
        border-right: 1px solid #292c33;
    }


    /* Main title */

    .main-title {
        font-size: 44px;
        font-weight: 800;
        letter-spacing: -1.5px;
        line-height: 1.1;
        margin-bottom: 10px;
    }

    .main-subtitle {
        font-size: 16px;
        color: #9a9faa;
        line-height: 1.6;
        margin-bottom: 35px;
    }


    /* Section title */

    .section-heading {
        font-size: 26px;
        font-weight: 750;
        margin-top: 30px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #858a96;
        font-size: 14px;
        margin-bottom: 20px;
    }


    /* Logo */

    .logo {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }

    .logo-line {
        width: 55px;
        height: 3px;
        background-color: #ff3b4d;
        margin-bottom: 35px;
    }


    /* Button */

    .stButton > button {
        border-radius: 9px;
        font-weight: 700;
        min-height: 46px;
    }


    /* Divider */

    .divider {
        height: 1px;
        background-color: #292c33;
        margin-top: 35px;
        margin-bottom: 35px;
    }


    /* Footer */

    .footer-text {
        color: #656a75;
        font-size: 12px;
        line-height: 1.6;
        margin-top: 40px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="logo">✦ LUMINA</div>
        <div class="logo-line"></div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Your profile")

    age = st.slider(
        "Age",
        min_value=18,
        max_value=28,
        value=21
    )

    skin_type = st.selectbox(
        "Skin type",
        [
            "Dry",
            "Normal",
            "Oily",
            "Combination"
        ]
    )

    activity_level = st.selectbox(
        "Outdoor activity",
        [
            "Low",
            "Moderate",
            "High"
        ]
    )

    st.caption(
        "Your profile is used only to personalize this session."
    )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">Understand your skin\'s climate stress</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-subtitle">
        See how today's environment may affect your skin
        and get a simple preventive strategy.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ENVIRONMENT SECTION
# ============================================================

st.markdown(
    '<div class="section-heading">Today\'s environment</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">Adjust the conditions around you.</div>',
    unsafe_allow_html=True
)


# ============================================================
# ENVIRONMENT INPUTS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    uv_index = st.slider(
        "UV Index",
        min_value=0.0,
        max_value=12.0,
        value=6.0,
        step=0.1
    )


with col2:

    pm25 = st.slider(
        "Air pollution (PM2.5)",
        min_value=0.0,
        max_value=300.0,
        value=50.0,
        step=1.0
    )


with col3:

    outdoor_hours = st.slider(
        "Outdoor time (hours)",
        min_value=0.0,
        max_value=10.0,
        value=3.0,
        step=0.5
    )


col4, col5 = st.columns(2)

with col4:

    temperature = st.slider(
        "Temperature (°C)",
        min_value=15.0,
        max_value=45.0,
        value=30.0,
        step=0.5
    )


with col5:

    humidity = st.slider(
        "Humidity (%)",
        min_value=20.0,
        max_value=95.0,
        value=65.0,
        step=1.0
    )


st.write("")


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze = st.button(
    "Analyze my skin environment",
    type="primary"
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze:

    with st.spinner("Analyzing your environment..."):

        try:

            # ------------------------------------------------
            # MODEL
            # ------------------------------------------------

            result = predict_stress(
                uv_index=uv_index,
                pm25=pm25,
                temperature=temperature,
                humidity=humidity,
                outdoor_hours=outdoor_hours,
                age=age,
                skin_type=skin_type,
                activity_level=activity_level
            )

            score = result["score"]
            category = result["category"]


            # ------------------------------------------------
            # RESULT MESSAGE
            # ------------------------------------------------

            if category == "Very Low":

                message = (
                    "Environmental conditions are relatively mild "
                    "for your current profile."
                )

            elif category == "Low":

                message = (
                    "Environmental stress is relatively low today. "
                    "Maintain your regular preventive routine."
                )

            elif category == "Moderate":

                message = (
                    "Some environmental factors may increase "
                    "skin stress today."
                )

            elif category == "High":

                message = (
                    "Several environmental factors may contribute "
                    "to higher skin stress today."
                )

            else:

                message = (
                    "Environmental conditions are strongly elevated. "
                    "Prioritize a consistent preventive routine."
                )


            # =================================================
            # RESULT
            # =================================================

            st.markdown(
                '<div class="divider"></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="section-heading">Your result</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="section-description">A simple estimate based on the conditions you entered.</div>',
                unsafe_allow_html=True
            )


            # ------------------------------------------------
            # SCORE
            # ------------------------------------------------

            result_col1, result_col2 = st.columns(
                [1, 2]
            )


            with result_col1:

                st.metric(
                    label="Climate skin stress",
                    value=f"{score:.1f}/100"
                )


            with result_col2:

                st.metric(
                    label="Environmental level",
                    value=category
                )


            # ------------------------------------------------
            # PROGRESS
            # ------------------------------------------------

            st.progress(
                min(max(score / 100, 0.0), 1.0)
            )

            st.caption(
                message
            )


            # =================================================
            # ENVIRONMENT SUMMARY
            # =================================================

            st.markdown(
                '<div class="section-heading">Your environment</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="section-description">Conditions used to calculate your result.</div>',
                unsafe_allow_html=True
            )


            f1, f2, f3, f4, f5 = st.columns(5)


            with f1:

                st.metric(
                    "UV",
                    f"{uv_index:.1f}"
                )


            with f2:

                st.metric(
                    "PM2.5",
                    f"{pm25:.0f}"
                )


            with f3:

                st.metric(
                    "Temperature",
                    f"{temperature:.1f}°C"
                )


            with f4:

                st.metric(
                    "Humidity",
                    f"{humidity:.0f}%"
                )


            with f5:

                st.metric(
                    "Outdoor",
                    f"{outdoor_hours:.1f}h"
                )


            # =================================================
            # RECOMMENDATIONS
            # =================================================

            st.markdown(
                '<div class="section-heading">What to do today</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="section-description">Simple preventive actions based on your environment.</div>',
                unsafe_allow_html=True
            )


            recommendations = generate_recommendations(
                uv_index=uv_index,
                pm25=pm25,
                temperature=temperature,
                humidity=humidity,
                outdoor_hours=outdoor_hours,
                stress_score=score
            )


            # ------------------------------------------------
            # RECOMMENDATION CARDS
            # ------------------------------------------------

            for recommendation in recommendations:

                title = recommendation.get(
                    "title",
                    "Recommendation"
                )

                text = recommendation.get(
                    "text",
                    ""
                )

                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"**{title}**"
                    )

                    st.write(
                        text
                    )


            # =================================================
            # DISCLAIMER
            # =================================================

            st.markdown(
                '<div class="footer-text">LUMINA AI is a competition prototype. '
                'The score is an environmental-risk estimate and is not a medical '
                'diagnosis or clinical assessment.</div>',
                unsafe_allow_html=True
            )


        except Exception as e:

            st.error(
                "Unable to generate the result."
            )

            st.error(
                str(e)
            )