"""
Car Price Prediction — Streamlit Frontend
Connects to the FastAPI backend at /predict endpoint.
"""

import streamlit as st
import requests

# ─── Configuration ───────────────────────────────────────────────────────────
API_URL = "https://fastapi-full-stack-1-v47n.onrender.com"
PREDICT_ENDPOINT = f"{API_URL}/predict"
TEST_ENDPOINT = f"{API_URL}/test"

CAR_NAMES = [
    "800", "Activa 3g", "Activa 4g", "alto 800", "alto k10", "amaze",
    "Bajaj Avenger 150", "Bajaj Avenger 150 street", "Bajaj Avenger 220",
    "Bajaj Avenger 220 dtsi", "Bajaj Avenger Street 220", "Bajaj ct 100",
    "Bajaj Discover 100", "Bajaj Discover 125", "Bajaj Dominar 400",
    "Bajaj Pulsar 135 LS", "Bajaj Pulsar 150", "Bajaj Pulsar 220 F",
    "Bajaj Pulsar NS 200", "Bajaj Pulsar RS200", "baleno", "brio", "camry",
    "ciaz", "city", "corolla", "corolla altis", "creta", "dzire", "elantra",
    "eon", "ertiga", "etios cross", "etios g", "etios gd", "etios liva",
    "fortuner", "grand i10", "Hero CBZ Xtreme", "Hero Extreme",
    "Hero Glamour", "Hero Honda CBZ extreme", "Hero Honda Passion Pro",
    "Hero Hunk", "Hero Ignitor Disc", "Hero Passion Pro",
    "Hero Passion X pro", "Hero Splender iSmart", "Hero Splender Plus",
    "Hero Super Splendor", "Honda Activa 125", "Honda Activa 4G",
    "Honda CB Hornet 160R", "Honda CBR 150", "Honda CB Shine",
    "Honda CB Trigger", "Honda CB twister", "Honda CB Unicorn",
    "Honda Dream Yuga", "Honda Karizma", "Hyosung GT250R", "i10", "i20",
    "ignis", "innova", "jazz", "KTM 390 Duke", "KTM RC200", "KTM RC390",
    "land cruiser", "Mahindra Mojo XT300", "omni", "ritz",
    "Royal Enfield Bullet 350", "Royal Enfield Classic 350",
    "Royal Enfield Classic 500", "Royal Enfield Thunder 350",
    "Royal Enfield Thunder 500", "s cross", "Suzuki Access 125", "swift",
    "sx4", "TVS Apache RTR 160", "TVS Apache RTR 180", "TVS Jupyter",
    "TVS Sport", "TVS Wego", "UM Renegade Mojave", "verna", "vitara brezza",
    "wagon r", "xcent", "Yamaha Fazer", "Yamaha FZ 16", "Yamaha FZ S",
    "Yamaha FZ S V 2.0", "Yamaha FZ v 2.0",
]

FUEL_TYPES = ["Petrol", "Diesel", "CNG"]
SELLER_TYPES = ["Dealer", "Individual"]
TRANSMISSION_TYPES = ["Manual", "Automatic"]


# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Header styling */
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
    }
    .main-header h1 {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    .main-header p {
        font-size: 1.05rem;
        opacity: 0.7;
    }

    /* Result card */
    .result-card {
        background: linear-gradient(135deg, #0f9b58 0%, #0d8a4e 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(15, 155, 88, 0.3);
    }
    .result-card .price {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0.5rem 0;
    }
    .result-card .label {
        font-size: 0.95rem;
        opacity: 0.85;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Error card */
    .error-card {
        background: linear-gradient(135deg, #e53935 0%, #c62828 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(229, 57, 53, 0.3);
    }

    /* API status badge */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-online {
        background-color: #e8f5e9;
        color: #2e7d32;
    }
    .status-offline {
        background-color: #ffebee;
        color: #c62828;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem;
        opacity: 0.5;
        font-size: 0.85rem;
    }

    /* Divider */
    .section-divider {
        border: none;
        border-top: 1px solid rgba(128,128,128,0.2);
        margin: 1.5rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ─── Helper Functions ────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def check_api_health() -> bool:
    """Check if the FastAPI backend is reachable."""
    try:
        resp = requests.get(TEST_ENDPOINT, timeout=5)
        return resp.status_code == 200
    except requests.ConnectionError:
        return False


def call_predict_api(payload: dict) -> dict:
    """Send prediction request to FastAPI backend."""
    resp = requests.post(PREDICT_ENDPOINT, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()


# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    api_url_input = st.text_input(
        "API Base URL",
        value=API_URL,
        help="The base URL of your FastAPI backend.",
    )
    if api_url_input != API_URL:
        PREDICT_ENDPOINT = f"{api_url_input}/predict"
        TEST_ENDPOINT = f"{api_url_input}/test"

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # API Health Check
    st.markdown("### 🩺 API Status")
    if st.button("Check Connection", use_container_width=True):
        st.cache_data.clear()

    api_online = check_api_health()
    if api_online:
        st.markdown(
            "<span class='status-badge status-online'>● Online</span>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<span class='status-badge status-offline'>● Offline</span>",
            unsafe_allow_html=True,
        )
        st.warning("API is not reachable. Make sure the FastAPI server is running.")

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown(
        """
        ### 📖 How to use
        1. Select your car details from the form
        2. Click **Predict Price**
        3. View the estimated selling price

        ### 🚀 Run the API
        ```bash
        cd car_price_api
        uvicorn app.main:app --reload
        ```
        """,
    )


# ─── Main Content ────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class='main-header'>
        <h1>🚗 Car Price Predictor</h1>
        <p>Get an instant estimate for your car's selling price</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─── Input Form ──────────────────────────────────────────────────────────────
with st.form("prediction_form"):
    st.markdown("### 📋 Car Details")

    col1, col2 = st.columns(2)

    with col1:
        car_name = st.selectbox(
            "Car Name",
            options=CAR_NAMES,
            index=CAR_NAMES.index("ritz"),
            help="Select the car model.",
        )
        year = st.number_input(
            "Year of Purchase",
            min_value=2000,
            max_value=2026,
            value=2014,
            step=1,
            help="The year the car was bought.",
        )
        present_price = st.number_input(
            "Present Showroom Price (₹ Lakhs)",
            min_value=0.0,
            max_value=100.0,
            value=5.59,
            step=0.01,
            format="%.2f",
            help="Current ex-showroom price in lakhs.",
        )
        kms_driven = st.number_input(
            "Kilometers Driven",
            min_value=0,
            max_value=500000,
            value=27000,
            step=500,
            help="Total distance driven in km.",
        )

    with col2:
        fuel_type = st.selectbox(
            "Fuel Type",
            options=FUEL_TYPES,
            help="Type of fuel the car uses.",
        )
        seller_type = st.selectbox(
            "Seller Type",
            options=SELLER_TYPES,
            help="Whether sold by dealer or individual.",
        )
        transmission = st.selectbox(
            "Transmission",
            options=TRANSMISSION_TYPES,
            help="Type of transmission.",
        )
        owner = st.selectbox(
            "Number of Previous Owners",
            options=[0, 1, 2, 3],
            index=0,
            help="How many people have owned this car before.",
        )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    submitted = st.form_submit_button(
        "🔮  Predict Price",
        use_container_width=True,
        type="primary",
    )


# ─── Prediction Result ───────────────────────────────────────────────────────
if submitted:
    payload = {
        "Car_Name": car_name,
        "year": int(year),
        "Present_price": float(present_price),
        "Kms_Driven": int(kms_driven),
        "Fuel_Type": fuel_type,
        "Seller_Type": seller_type,
        "Transmission": transmission,
        "owner": int(owner),
    }

    with st.spinner("Predicting..."):
        try:
            result = call_predict_api(payload)
            predicted_price = result.get("prediction_price", 0.0)

            st.markdown(
                f"""
                <div class='result-card'>
                    <div class='label'>Estimated Selling Price</div>
                    <div class='price'>₹ {predicted_price:,.2f} Lakhs</div>
                    <div class='label'>{car_name} · {year} · {fuel_type}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Summary table
            with st.expander("📊 Input Summary", expanded=False):
                summary_col1, summary_col2 = st.columns(2)
                with summary_col1:
                    st.metric("Car Name", car_name)
                    st.metric("Year", year)
                    st.metric("Present Price", f"₹ {present_price:.2f} L")
                    st.metric("Kms Driven", f"{kms_driven:,}")
                with summary_col2:
                    st.metric("Fuel Type", fuel_type)
                    st.metric("Seller Type", seller_type)
                    st.metric("Transmission", transmission)
                    st.metric("Owners", owner)

        except requests.ConnectionError:
            st.markdown(
                """
                <div class='error-card'>
                    <h3>⚠️ Connection Error</h3>
                    <p>Cannot reach the API server. Please make sure it is running.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except requests.HTTPError as e:
            st.markdown(
                f"""
                <div class='error-card'>
                    <h3>⚠️ Prediction Error</h3>
                    <p>{e.response.text if e.response else str(e)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.markdown(
                f"""
                <div class='error-card'>
                    <h3>⚠️ Unexpected Error</h3>
                    <p>{str(e)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    "<div class='footer'>Car Price Prediction App · Powered by FastAPI & Streamlit</div>",
    unsafe_allow_html=True,
)
