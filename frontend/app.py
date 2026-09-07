import os

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(

    page_title="Karachi AQI Forecast",

    page_icon="🌍",

    layout="wide",

    initial_sidebar_state="collapsed"

)


# ============================================================
# API CONFIGURATION
# ============================================================

API_URL = os.getenv(

    "API_URL",

    "http://localhost:8000"

)

# ============================================================
# SESSION STATE
# ============================================================

if "prediction_data" not in st.session_state:

    st.session_state.prediction_data = None


if "explanation_data" not in st.session_state:

    st.session_state.explanation_data = None


if "backend_connected" not in st.session_state:

    st.session_state.backend_connected = False


if "shap_error" not in st.session_state:

    st.session_state.shap_error = None


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(

    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    div[data-testid="stMetric"] {
        background-color: #1f2937;
        border: 1px solid #374151;
        padding: 20px;
        border-radius: 12px;
    }

    </style>
    """,

    unsafe_allow_html=True

)


# ============================================================
# AQI INFORMATION FUNCTION
# ============================================================

def get_aqi_information(aqi):


    if aqi <= 50:

        return {

            "category": "Good",

            "emoji": "😊",

            "message": (

                "Air quality is satisfactory. "
                "Outdoor activities are safe for everyone."

            )

        }


    elif aqi <= 100:

        return {

            "category": "Moderate",

            "emoji": "🙂",

            "message": (

                "Air quality is acceptable. "
                "Most people can continue normal outdoor activities."

            )

        }


    elif aqi <= 150:

        return {

            "category": (
                "Unhealthy for Sensitive Groups"
            ),

            "emoji": "😷",

            "message": (

                "Sensitive individuals should consider reducing "
                "prolonged or heavy outdoor activities."

            )

        }


    elif aqi <= 200:

        return {

            "category": "Unhealthy",

            "emoji": "😷",

            "message": (

                "Everyone may begin experiencing health effects. "
                "Sensitive groups may experience more serious effects."

            )

        }


    elif aqi <= 300:

        return {

            "category": "Very Unhealthy",

            "emoji": "⚠️",

            "message": (

                "Health alert. Everyone may experience "
                "more serious health effects."

            )

        }


    else:

        return {

            "category": "Hazardous",

            "emoji": "🚨",

            "message": (

                "Health warning. Everyone should avoid outdoor "
                "activities whenever possible."

            )

        }


# ============================================================
# API REQUEST FUNCTION
# ============================================================

def make_api_request(endpoint, timeout=30):


    url = f"{API_URL}{endpoint}"


    try:


        response = requests.get(

            url,

            timeout=timeout

        )


        return response


    except requests.exceptions.RequestException:


        return None


# ============================================================
# HEADER
# ============================================================

st.title(

    "🌍 Karachi AQI Forecasting"

)


st.caption(

    "AI-powered next-day Air Quality Index forecasting system "
    "for Karachi, Pakistan."

)


st.divider()


# ============================================================
# SYSTEM STATUS
# ============================================================

st.subheader(

    "System Status"

)


try:


    health_response = requests.get(

        f"{API_URL}/health",

        timeout=5

    )


    if health_response.status_code == 200:

        st.session_state.backend_connected = True


    else:

        st.session_state.backend_connected = False


except requests.exceptions.RequestException:

    st.session_state.backend_connected = False


status_col1, status_col2, status_col3 = st.columns(

    3

)


with status_col1:


    if st.session_state.backend_connected:

        st.success(

            "🟢 Backend Connected"

        )


    else:

        st.error(

            "🔴 Backend Offline"

        )


with status_col2:


    if st.session_state.backend_connected:

        st.success(

            "🤖 ML Model Ready"

        )


    else:

        st.warning(

            "🤖 Model Status Unknown"

        )


with status_col3:


    if st.session_state.backend_connected:

        st.success(

            "🗄️ Feature Pipeline Ready"

        )


    else:

        st.warning(

            "🗄️ Pipeline Status Unknown"

        )


st.divider()


# ============================================================
# AQI PREDICTION
# ============================================================

st.subheader(

    "Next-Day AQI Prediction"

)


st.write(

    "Generate a machine learning prediction for the "
    "next-day Air Quality Index in Karachi."

)


if st.button(

    "🔮 Generate AQI Prediction",

    use_container_width=True,

    type="primary"

):


    # ========================================================
    # RESET OLD DATA
    # ========================================================

    st.session_state.prediction_data = None

    st.session_state.explanation_data = None

    st.session_state.shap_error = None


    # ========================================================
    # CHECK BACKEND
    # ========================================================

    if not st.session_state.backend_connected:


        st.error(

            "Backend is not connected. "
            "Please start the FastAPI server first."

        )


    else:


        try:


            # ====================================================
            # GET PREDICTION
            # ====================================================

            with st.spinner(

                "Generating prediction using the ML model..."

            ):


                prediction_response = requests.get(

                    f"{API_URL}/predict",

                    timeout=60

                )


            # ====================================================
            # CHECK PREDICTION RESPONSE
            # ====================================================

            if prediction_response.status_code == 200:


                prediction_data = (

                    prediction_response.json()

                )


                st.session_state.prediction_data = (

                    prediction_data

                )


                # =================================================
                # GET SHAP EXPLANATION
                # =================================================

                try:


                    with st.spinner(

                        "Analyzing feature impact using SHAP..."

                    ):


                        explain_response = requests.get(

                            f"{API_URL}/explain",

                            timeout=60

                        )


                    # =============================================
                    # SUCCESSFUL SHAP RESPONSE
                    # =============================================

                    if explain_response.status_code == 200:


                        explain_data = (

                            explain_response.json()

                        )


                        explanations = (

                            explain_data.get(

                                "explanation",

                                []

                            )

                        )


                        # =========================================
                        # VERIFY SHAP DATA
                        # =========================================

                        if len(explanations) > 0:


                            st.session_state.explanation_data = (

                                explain_data

                            )


                            st.session_state.shap_error = None


                        else:


                            st.session_state.explanation_data = None


                            st.session_state.shap_error = (

                                "The SHAP API returned successfully, "
                                "but no feature explanations were found."

                            )


                    # =============================================
                    # FAILED SHAP RESPONSE
                    # =============================================

                    else:


                        st.session_state.explanation_data = None


                        try:


                            error_data = (

                                explain_response.json()

                            )


                            st.session_state.shap_error = (

                                f"Explain API returned status code "
                                f"{explain_response.status_code}: "
                                f"{error_data}"

                            )


                        except Exception:


                            st.session_state.shap_error = (

                                f"Explain API returned status code "
                                f"{explain_response.status_code}"

                            )


                # =================================================
                # SHAP CONNECTION ERROR
                # =================================================

                except requests.exceptions.RequestException as error:


                    st.session_state.explanation_data = None


                    st.session_state.shap_error = (

                        f"Could not connect to SHAP explanation API: "
                        f"{error}"

                    )


            # ====================================================
            # PREDICTION FAILED
            # ====================================================

            else:


                st.error(

                    f"Prediction request failed. "
                    f"Status code: "
                    f"{prediction_response.status_code}"

                )


                try:


                    error_detail = (

                        prediction_response.json()

                    )


                    st.caption(

                        f"API Response: {error_detail}"

                    )


                except Exception:

                    pass


        # ========================================================
        # PREDICTION CONNECTION ERROR
        # ========================================================

        except requests.exceptions.RequestException as error:


            st.error(

                "Unable to connect to prediction service."

            )


            st.caption(

                f"Error details: {error}"

            )


# ============================================================
# DISPLAY PREDICTION
# ============================================================

if st.session_state.prediction_data is not None:


    prediction_data = (

        st.session_state.prediction_data

    )


    # ========================================================
    # EXTRACT DATA
    # ========================================================

    predicted_aqi = float(

        prediction_data[
            "predicted_aqi"
        ]

    )


    prediction_for = prediction_data.get(

        "prediction_for",

        "Next Day"

    )


    # ========================================================
    # AQI INFORMATION
    # ========================================================

    aqi_info = get_aqi_information(

        predicted_aqi

    )


    st.divider()


    # ========================================================
    # MAIN RESULT
    # ========================================================

    st.subheader(

        "Prediction Result"

    )


    result_col1, result_col2 = st.columns(

        [1, 2]

    )


    with result_col1:


        st.metric(

            "Predicted AQI",

            f"{predicted_aqi:.2f}"

        )


    with result_col2:


        if predicted_aqi <= 50:


            st.success(

                f"{aqi_info['emoji']} "
                f"AQI Category: "
                f"{aqi_info['category']}"

            )


        elif predicted_aqi <= 100:


            st.warning(

                f"{aqi_info['emoji']} "
                f"AQI Category: "
                f"{aqi_info['category']}"

            )


        else:


            st.error(

                f"{aqi_info['emoji']} "
                f"AQI Category: "
                f"{aqi_info['category']}"

            )


    # ========================================================
    # PREDICTION DETAILS
    # ========================================================

    st.subheader(

        "Prediction Details"

    )


    detail_col1, detail_col2, detail_col3 = st.columns(

        3

    )


    with detail_col1:


        st.metric(

            "📊 Predicted AQI",

            f"{predicted_aqi:.2f}"

        )


    with detail_col2:


        st.metric(

            "🌡️ AQI Category",

            aqi_info["category"]

        )


    with detail_col3:


        st.metric(

            "📅 Prediction For",

            prediction_for

        )


    # ========================================================
    # HEALTH RECOMMENDATION
    # ========================================================

    st.divider()


    st.subheader(

        "Health Recommendation"

    )


    st.info(

        f"{aqi_info['emoji']} "
        f"**Air Quality Guidance**\n\n"
        f"{aqi_info['message']}"

    )


    # ========================================================
    # AQI SCALE
    # ========================================================

    st.divider()


    st.subheader(

        "AQI Scale"

    )


    scale_col1, scale_col2, scale_col3 = st.columns(

        3

    )


    with scale_col1:


        st.success(

            "0 – 50\n\n"
            "**Good**"

        )


        st.warning(

            "51 – 100\n\n"
            "**Moderate**"

        )


    with scale_col2:


        st.warning(

            "101 – 150\n\n"
            "**Unhealthy for Sensitive Groups**"

        )


        st.error(

            "151 – 200\n\n"
            "**Unhealthy**"

        )


    with scale_col3:


        st.error(

            "201 – 300\n\n"
            "**Very Unhealthy**"

        )


        st.error(

            "301+\n\n"
            "**Hazardous**"

        )


    # ========================================================
    # AI PREDICTION EXPLANATION
    # ========================================================

    st.divider()


    st.subheader(

        "🧠 AI Prediction Explanation"

    )


    st.write(

        "The following features show how the AI model "
        "was influenced when generating this AQI prediction."

    )


    # ========================================================
    # CHECK SHAP DATA
    # ========================================================

    if st.session_state.explanation_data is not None:


        explain_data = (

            st.session_state.explanation_data

        )


        explanations = (

            explain_data.get(

                "explanation",

                []

            )

        )


        # ====================================================
        # VERIFY EXPLANATIONS
        # ====================================================

        if len(explanations) > 0:


            # =================================================
            # CREATE SHAP DATAFRAME
            # =================================================

            shap_df = pd.DataFrame(

                explanations

            )


            # =================================================
            # CONVERT SHAP VALUES
            # =================================================

            if "shap_value" in shap_df.columns:


                shap_df["shap_value"] = (

                    pd.to_numeric(

                        shap_df["shap_value"],

                        errors="coerce"

                    )

                )


            if "feature_value" in shap_df.columns:


                shap_df["feature_value"] = (

                    pd.to_numeric(

                        shap_df["feature_value"],

                        errors="coerce"

                    )

                )


            # =================================================
            # REMOVE INVALID VALUES
            # =================================================

            shap_df = (

                shap_df

                .dropna(

                    subset=["shap_value"]

                )

            )


            # =================================================
            # ADD ABSOLUTE IMPACT
            # =================================================

            shap_df["absolute_impact"] = (

                shap_df["shap_value"].abs()

            )


            # =================================================
            # SORT BY IMPORTANCE
            # =================================================

            shap_df = (

                shap_df

                .sort_values(

                    by="absolute_impact",

                    ascending=False

                )

                .reset_index(

                    drop=True

                )

            )


            # =================================================
            # TOP FEATURES TABLE
            # =================================================

            st.subheader(

                "Top Features Influencing Prediction"

            )


            display_df = (

                shap_df[

                    [

                        "feature",

                        "feature_value",

                        "shap_value",

                        "impact"

                    ]

                ]

                .copy()

            )


            # =================================================
            # ROUND VALUES
            # =================================================

            display_df[

                "feature_value"

            ] = (

                display_df[

                    "feature_value"

                ].round(4)

            )


            display_df[

                "shap_value"

            ] = (

                display_df[

                    "shap_value"

                ].round(4)

            )


            # =================================================
            # RENAME COLUMNS
            # =================================================

            display_df = (

                display_df.rename(

                    columns={

                        "feature":
                            "Feature",

                        "feature_value":
                            "Current Value",

                        "shap_value":
                            "SHAP Impact",

                        "impact":
                            "Effect on AQI"

                    }

                )

            )


            # =================================================
            # DISPLAY TABLE
            # =================================================

            st.dataframe(

                display_df,

                use_container_width=True,

                hide_index=True

            )


            # =================================================
            # FEATURE IMPACT SUMMARY
            # ============================================================

            st.subheader(

                "Feature Impact Summary"

            )


            summary_col1, summary_col2, summary_col3 = (

                st.columns(3)

            )


            top_feature = (

                shap_df.iloc[0]

            )


            positive_features = (

                len(

                    shap_df[

                        shap_df["shap_value"] > 0

                    ]

                )

            )


            negative_features = (

                len(

                    shap_df[

                        shap_df["shap_value"] < 0

                    ]

                )

            )


            with summary_col1:


                st.metric(

                    "Strongest Feature",

                    str(

                        top_feature["feature"]

                    )

                )


            with summary_col2:


                st.metric(

                    "Features Increasing AQI",

                    positive_features

                )


            with summary_col3:


                st.metric(

                    "Features Decreasing AQI",

                    negative_features

                )


            # =================================================
            # FEATURE IMPACT VISUALIZATION
            # =================================================

            st.subheader(

                "Feature Impact Visualization"

            )


            st.caption(

                "Features are ranked by their absolute SHAP "
                "impact. The chart uses a symmetric logarithmic "
                "scale so both large and small feature impacts "
                "remain visible."

            )


            # =================================================
            # PREPARE CHART DATA
            # =================================================

            chart_df = (

                shap_df

                .sort_values(

                    by="absolute_impact",

                    ascending=True

                )

                .copy()

            )


            # =================================================
            # CREATE BAR COLORS
            # =================================================

            bar_colors = [

                "#ef4444"

                if value < 0

                else "#22c55e"

                for value in chart_df["shap_value"]

            ]


            # =================================================
            # CREATE PROFESSIONAL DARK CHART
            # =================================================

            fig, ax = plt.subplots(

                figsize=(11, 7)

            )


            fig.patch.set_facecolor(

                "#0e1117"

            )


            ax.set_facecolor(

                "#0e1117"

            )


            bars = ax.barh(

                chart_df["feature"],

                chart_df["shap_value"],

                color=bar_colors,

                alpha=0.9

            )


            # =================================================
            # ZERO REFERENCE LINE
            # =================================================

            ax.axvline(

                x=0,

                color="#9ca3af",

                linewidth=1.2

            )


            # =================================================
            # SYMMETRIC LOG SCALE
            # =================================================

            max_abs_value = (

                chart_df[

                    "absolute_impact"

                ].max()

            )


            if max_abs_value > 1:


                ax.set_xscale(

                    "symlog",

                    linthresh=0.1

                )


            # =================================================
            # ADD VALUE LABELS
            # =================================================

            for bar, value in zip(

                bars,

                chart_df["shap_value"]

            ):


                y_position = (

                    bar.get_y()

                    +

                    bar.get_height()

                    / 2

                )


                if value >= 0:


                    label_x = (

                        value

                    )


                    horizontal_alignment = (

                        "left"

                    )


                else:


                    label_x = (

                        value

                    )


                    horizontal_alignment = (

                        "right"

                    )


                ax.annotate(

                    f"{value:.3f}",

                    xy=(

                        label_x,

                        y_position

                    ),

                    xytext=(

                        5

                        if value >= 0

                        else -5,

                        0

                    ),

                    textcoords="offset points",

                    va="center",

                    ha=horizontal_alignment,

                    fontsize=9,

                    color="#e5e7eb"

                )


            # =================================================
            # CHART TITLE
            # =================================================

            ax.set_title(

                "SHAP Feature Impact on AQI Prediction",

                fontsize=17,

                fontweight="bold",

                color="#f9fafb",

                pad=18

            )


            # =================================================
            # AXIS LABELS
            # =================================================

            ax.set_xlabel(

                "SHAP Value",

                fontsize=12,

                color="#d1d5db",

                labelpad=12

            )


            ax.set_ylabel(

                "Features",

                fontsize=12,

                color="#d1d5db",

                labelpad=12

            )


            # =================================================
            # TICK COLORS
            # =================================================

            ax.tick_params(

                axis="x",

                colors="#d1d5db"

            )


            ax.tick_params(

                axis="y",

                colors="#d1d5db"

            )


            # =================================================
            # REMOVE UNNECESSARY BORDERS
            # =================================================

            ax.spines[

                "top"

            ].set_visible(False)


            ax.spines[

                "right"

            ].set_visible(False)


            ax.spines[

                "left"

            ].set_color(

                "#4b5563"

            )


            ax.spines[

                "bottom"

            ].set_color(

                "#4b5563"

            )


            # =================================================
            # GRID
            # =================================================

            ax.grid(

                axis="x",

                linestyle="--",

                alpha=0.2

            )


            plt.tight_layout()


            # =================================================
            # DISPLAY CHART
            # =================================================

            st.pyplot(

                fig,

                use_container_width=True

            )


            plt.close(fig)


            # =================================================
            # LEGEND
            # =================================================

            legend_col1, legend_col2 = (

                st.columns(2)

            )


            with legend_col1:


                st.success(

                    "🟢 Positive SHAP Value → "
                    "Feature increased the predicted AQI."

                )


            with legend_col2:


                st.error(

                    "🔴 Negative SHAP Value → "
                    "Feature decreased the predicted AQI."

                )


            # =================================================
            # AI EXPLANATION
            # =================================================

            st.info(

                "📊 **How to interpret this explanation:** "
                "SHAP values show how each environmental feature "
                "influenced the final AQI prediction. Features "
                "with larger absolute SHAP values had a stronger "
                "influence on the machine learning model. "
                "Positive values pushed the prediction higher, "
                "while negative values pushed it lower."

            )


        else:


            st.warning(

                "SHAP explanation was returned, but no "
                "feature explanations were found."

            )


    # ========================================================
    # SHAP ERROR
    # ========================================================

    else:


        st.warning(

            "AQI prediction was generated successfully, "
            "but the AI explanation could not be retrieved."

        )


        if st.session_state.shap_error:


            st.error(

                st.session_state.shap_error

            )


        else:


            st.caption(

                "Make sure the FastAPI server is running and "
                "the /explain endpoint is available."

            )


    # ========================================================
    # SYSTEM INFORMATION
    # ========================================================

    st.divider()


    st.subheader(

        "System Information"

    )


    info_col1, info_col2 = st.columns(

        2

    )


    with info_col1:


        st.info(

            """
            🤖 **Machine Learning Model**

            Random Forest model trained using historical
            Karachi air quality data and engineered
            environmental features.
            """

        )


    with info_col2:


        st.info(

            """
            ⚙️ **Production Pipeline**

            Live Data → Feature Engineering →
            Feast Feature Store →
            Random Forest Model →
            FastAPI → SHAP → Streamlit Dashboard
            """

        )


    # ========================================================
    # SUCCESS MESSAGE
    # ========================================================

    st.success(

        "✅ Prediction generated successfully."

    )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(

    "🌍 Karachi AQI Forecasting System | "
    f"Dashboard loaded: "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

)