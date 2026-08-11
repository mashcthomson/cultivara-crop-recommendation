# app.py

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import joblib
import random
import json
from PIL import Image
from streamlit_autorefresh import st_autorefresh

# Resolve all asset paths relative to this file so the app works from any cwd
# (and regardless of the OS the project was originally developed on).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_model(region):
    """
    Load the machine learning model based on the region.
    """
    model_path = os.path.join(BASE_DIR, 'models', f'crop_recommendation_{region.lower()}.pkl')
    try:
        model = joblib.load(model_path)
        st.sidebar.success(f"All Models loaded successfully.")
        return model
    except Exception as e:
        st.sidebar.error(f"Error loading model for {region}: {e}")
        return None

def load_label_encoder(region):
    """
    Load the label encoder for soil type based on the region.
    """
    encoder_path = os.path.join(BASE_DIR, 'models', f'label_encoder_soil_{region.lower()}.pkl')
    try:
        le_soil = joblib.load(encoder_path)
        return le_soil
    except Exception as e:
        st.error(f"Error loading label encoder for {region}: {e}")
        return None

def load_welcome_messages():
    """
    Load welcome messages from welcome_messages.txt.
    """
    try:
        with open(os.path.join(BASE_DIR, 'static', 'messages', 'welcome_messages.txt'), 'r') as f:
            messages = [line.strip().strip('"') for line in f if line.strip()]
        return messages
    except Exception as e:
        st.error(f"Error loading welcome messages: {e}")
        return ["Welcome to Cultivara!"]

def load_top_messages():
    """
    Load top messages from topmessage.txt.
    """
    try:
        with open(os.path.join(BASE_DIR, 'static', 'messages', 'topmessage.txt'), 'r') as f:
            messages = [line.strip().strip('"') for line in f if line.strip()]
        return messages
    except Exception as e:
        st.error(f"Error loading top messages: {e}")
        return ["Welcome to Cultivara!"]

def load_cards(region):
    """
    Load crop/farming practice cards from a JSON file based on the region.
    """
    try:
        with open(os.path.join(BASE_DIR, 'data', f'{region.lower()}_cards.json'), 'r') as f:
            cards = json.load(f)
        return cards
    except Exception as e:
        st.error(f"Error loading cards for {region}: {e}")
        return []

def load_additional_info(region, crop):
    """
    Load additional information for the recommended crop.
    """
    try:
        with open(os.path.join(BASE_DIR, 'data', f'{region.lower()}_crop_info.json'), 'r') as f:
            crop_info = json.load(f)
        return crop_info.get(crop, {})
    except Exception as e:
        st.error(f"Error loading additional info for {crop} in {region}: {e}")
        return {}

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Cultivara - Crop Recommendation System",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Auto-refresh every 15 seconds to update dynamic messages
    st_autorefresh(interval=15000, limit=None, key="dynamic_message_refresh")

    # Load messages
    welcome_messages = load_welcome_messages()
    top_messages = load_top_messages()

    # Sidebar information
    st.sidebar.title("Cultivara")
    st.sidebar.markdown("""
    **About:**
    Cultivara provides crop recommendations based on soil and climate data tailored to your region.
    """)

    # Welcome Overlay
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = True

    if st.session_state.show_welcome:
        current_welcome_message = random.choice(welcome_messages)
        st.markdown(f"""
            <div id="welcome-overlay" style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(40, 167, 69, 0.95);
                color: white;
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 1000;
                transition: opacity 2s ease;
                text-align: center;
                padding: 170px;
            ">
                <h2>{current_welcome_message}</h2>
            </div>
        """, unsafe_allow_html=True)

        # JavaScript to hide the overlay after 4 seconds
        st.markdown("""
            <script>
                setTimeout(function(){
                    var overlay = document.getElementById('welcome-overlay');
                    if (overlay) {
                        overlay.style.opacity = '1';
                        setTimeout(function(){
                            overlay.style.display = 'none';
                        }, 2000); // Duration of the fade-out transition
                    }
                }, 4000); // Display the welcome message for 4 seconds before starting the fade-out
            </script>
        """, unsafe_allow_html=True)

        st.session_state.show_welcome = False

        # Header Section
    st.markdown("<div class='header'><h1>Welcome to Cultivara</h1><p>Cultivating with Climate</p></div>", unsafe_allow_html=True)

    # Dynamic Message above Select Region
    if top_messages:
        if 'current_top_message' not in st.session_state:
            st.session_state.current_top_message = random.choice(top_messages)
            st.session_state.last_update_top = datetime.datetime.now()
        else:
            # Check if it's time to update the message
            if datetime.datetime.now() - st.session_state.last_update_top > pd.Timedelta(seconds=15):
                st.session_state.current_top_message = random.choice(top_messages)
                st.session_state.last_update_top = datetime.datetime.now()

        st.markdown(f"<div style='background-color:#d1ecf1; color:#0c5460; padding:15px; text-align:center; font-size:1.1rem; border-radius:5px; margin-bottom:20px;'>{st.session_state.current_top_message}</div>", unsafe_allow_html=True)

    

    # Main Content
    st.markdown("<div class='container'>", unsafe_allow_html=True)

    # Region Selection
    st.subheader("Select Your Region")
    regions = ['Wheatbelt', 'Kimberley', 'Southwest']
    selected_region = st.selectbox("Choose your region:", regions)

    # Load the appropriate model and label encoder
    model = load_model(selected_region)
    le_soil = load_label_encoder(selected_region)

    # Model Availability Check
    if model is None:
        st.warning("Crop recommendations are currently unavailable. Please train the model to enable this feature.")

    # Load cards based on selected region
    cards = load_cards(selected_region)

    # Display Crop Cards
    if cards:
        st.subheader(f"Recommended Crops and Practices in {selected_region}")
        st.markdown("<div class='row'>", unsafe_allow_html=True)
        cols = st.columns(3)
        for idx, card in enumerate(cards):
            with cols[idx % 3]:
                # Load and display image
                image_path = os.path.join(BASE_DIR, 'static', 'images', selected_region.lower(), card['image'])
                try:
                    image = Image.open(image_path)
                    st.image(image, width='stretch')
                except Exception as e:
                    st.error(f"Image not found: {image_path} - {e}")

                # Card title
                st.markdown(f"### {card['title']}")

                # Expandable section for more details
                with st.expander("View Details"):
                    st.markdown(f"**Suitable Methods:**")
                    for method in card['methods']:
                        st.markdown(f"- {method}")
                    st.markdown(f"**Optimal Planting Months:** {card['planting_months']}")
                    st.markdown(f"**Why:** {card['why']}")
                    st.markdown(f"**Reasons/Benefits:**")
                    for reason in card['reasons']:
                        st.markdown(f"- {reason}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Crop Recommendation Form
    st.subheader("Enter Your Farm Details for Crop Recommendation")
    with st.form("recommend_form"):
        # Inputs
        region_input = selected_region

        # Location selection
        if region_input == 'Wheatbelt':
            locations = ['Merredin']
        elif region_input == 'Kimberley':
            locations = ['Kununurra']
        else:
            locations = ['Manjimup']
        location_input = st.selectbox("Select Location", locations)

        # Date input
        date_input = st.date_input("Select Date", datetime.date.today())

        # Soil types for each region based on your data
        # Soil lists mirror each region's entries in data/Soil_Parameters.csv,
        # so every option can be encoded by that region's label encoder.
        if region_input == 'Wheatbelt':
            soil_types = ['Sandy Loam', 'Clay Loam', 'Loamy Sand']
        elif region_input == 'Kimberley':
            soil_types = ['Clay', 'Silt Loam', 'Loam']
        else:
            soil_types = ['Loamy Clay', 'Sandy Clay', 'Clay Loam']

        soil_input = st.selectbox("Soil Type", soil_types)

        # Optional Inputs with "I don't know" checkbox
        def optional_number_input(label, key, min_value=None, max_value=None, step=None):
            col1, col2 = st.columns([3, 1])
            with col1:
                value = st.number_input(label, min_value=min_value, max_value=max_value, step=step, key=key)
            with col2:
                optional = st.checkbox("I don't know", key=f"{key}_unknown")
            return None if optional else value

        temperature_input = optional_number_input("Average Temperature (°C)", "temperature", min_value=-50.0, max_value=60.0, step=0.1)
        rainfall_input = optional_number_input("Monthly Rainfall (mm)", "rainfall", min_value=0.0, step=1.0)
        pH_input = optional_number_input("Soil pH", "pH", min_value=0.0, max_value=14.0, step=0.01)
        n_input = optional_number_input("Nitrogen (%)", "nitrogen", min_value=0.0, step=0.001)
        p_input = optional_number_input("Phosphorus (%)", "phosphorus", min_value=0.0, step=0.001)
        k_input = optional_number_input("Potassium (%)", "potassium", min_value=0.0, step=0.001)

        # Submit button
        submitted = st.form_submit_button("Get Recommendation")

    if submitted:
        if model is not None and le_soil is not None:
            # Handle missing inputs by replacing them with average values or model defaults
            # For simplicity, we'll use fixed default values here
            default_temperature = 20.0
            default_rainfall = 50.0
            default_pH = 6.5
            default_n = 0.1
            default_p = 0.05
            default_k = 0.1

            temperature = temperature_input if temperature_input is not None else default_temperature
            rainfall = rainfall_input if rainfall_input is not None else default_rainfall
            pH = pH_input if pH_input is not None else default_pH
            n = n_input if n_input is not None else default_n
            p = p_input if p_input is not None else default_p
            k = k_input if k_input is not None else default_k

            # Encode soil type
            try:
                soil_encoded = le_soil.transform([soil_input])[0]
            except Exception as e:
                st.error(f"Error encoding soil type: {e}")
                soil_encoded = 0  # Handle appropriately

            # Prepare features for prediction
            features = np.array([[temperature, rainfall, pH, n, p, k, soil_encoded]])

            # Make prediction
            try:
                prediction = model.predict(features)
                recommended_crop = prediction[0]
                # st.toast is the only native Streamlit primitive with a duration
                # argument, so it is the clean way to auto-dismiss this message
                # instead of leaving a full-width success banner on screen
                # indefinitely. It renders top-right rather than full-width, but
                # the crop name stays visible in the detail section below.
                st.toast(f"Recommended crop for {region_input}: {recommended_crop}", icon="✅", duration=2)

                # Load additional info for the recommended crop
                additional_info = load_additional_info(region_input, recommended_crop)

                if additional_info:
                    st.markdown(f"**Why is {recommended_crop} recommended?**")
                    st.markdown(f"{additional_info.get('why', 'No information available.')}")

                    st.markdown(f"**Recommended Irrigation System:** {additional_info.get('irrigation_system', 'No information available.')}")
                    st.markdown(f"**Recommended Farming Methods:**")
                    methods = additional_info.get('farming_methods', [])
                    for method in methods:
                        st.markdown(f"- {method}")

                    st.markdown(f"**Grazing Recommendations:** {additional_info.get('grazing', 'No information available.')}")
                    st.markdown(f"**Suitability for Viticulture or Horticulture:** {additional_info.get('suitability', 'No information available.')}")

                    # Include date-based recommendations
                    planting_months = additional_info.get('optimal_planting_months', '')
                    if planting_months:
                        # Parse the planting months and compare with the selected date
                        current_month = date_input.month
                        suitable_months = parse_months(planting_months)
                        if current_month in suitable_months:
                            st.markdown(f"**Timing:** The selected date is within the optimal planting months for {recommended_crop}.")
                        else:
                            next_suitable_months = [month for month in suitable_months if month > current_month]
                            if next_suitable_months:
                                next_month = min(next_suitable_months)
                            else:
                                next_month = min(suitable_months)  # Next year's months
                            month_name = datetime.date(1900, next_month, 1).strftime('%B')
                            st.markdown(f"**Timing:** The next optimal planting month for {recommended_crop} is {month_name}.")
                    else:
                        st.markdown("**Timing:** No specific planting months information available.")

                else:
                    st.info("Additional information for the recommended crop is not available.")

            except Exception as e:
                st.error(f"Error making prediction: {e}")
        else:
            st.error("Crop recommendation model or label encoder is not available for the selected region.")

def parse_months(month_str):
    """
    Parse a string of months into a list of month numbers.
    Example input: "May - July"
    Output: [5, 6, 7]
    """
    months = []
    month_ranges = month_str.split(',')
    for mr in month_ranges:
        mr = mr.strip()
        if '-' in mr:
            start_month_str, end_month_str = mr.split('-')
            start_month = datetime.datetime.strptime(start_month_str.strip(), '%B').month
            end_month = datetime.datetime.strptime(end_month_str.strip(), '%B').month
            if start_month <= end_month:
                months.extend(range(start_month, end_month + 1))
            else:  # Handles year wrap-around
                months.extend(list(range(start_month, 13)) + list(range(1, end_month + 1)))
        else:
            month = datetime.datetime.strptime(mr.strip(), '%B').month
            months.append(month)
    return months

if __name__ == "__main__":
    main()
