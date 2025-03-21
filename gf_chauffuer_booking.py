import streamlit as st
import datetime
import pandas as pd
import os
from PIL import Image

# Set page config
st.set_page_config(
    page_title="GF Airport Chauffeur Service",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
    }
    .vehicle-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        background-color: white;
    }
    .vehicle-header {
        font-size: 1.5rem;
        font-weight: 600;
    }
    .vehicle-subheader {
        font-size: 1rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .vehicle-price {
        font-size: 1.25rem;
        font-weight: 600;
        margin: 1rem 0;
    }
    .feature-list {
        margin: 1rem 0;
    }
    .best-deal-tag {
        background-color: #28a745;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin-left: 1rem;
    }
    .popular-tag {
        background-color: #ff7700;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        margin-left: 0.5rem;
    }
    .footnote {
        font-size: 0.8rem;
        color: #666;
        font-style: italic;
        margin-top: 1rem;
    }
    .button-container {
        display: flex;
        justify-content: center;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2rem 0 1.5rem 0;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 0.5rem;
    }
    .premium-fleet {
        margin-top: 3rem;
    }
    .premium-fleet-header {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 2rem;
        text-align: center;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem;
        color: #666;
        font-size: 0.9rem;
        background-color: #f8f9fa;
        border-radius: 5px;
    }
    .feature-item {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    .feature-icon {
        color: #28a745;
        margin-right: 0.5rem;
    }
    .form-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .car-image {
        width: 100%;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .fleet-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        height: 100%;
    }
    .fleet-detail {
        display: flex;
        align-items: center;
        margin: 0.5rem 0;
    }
    .fleet-icon {
        width: 20px;
        margin-right: 10px;
    }
    .confirmation-container {
        background-color: #e8f4f8;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }
    .confirmation-header {
        font-size: 1.8rem;
        color: #28a745;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .confirmation-detail {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .detail-header {
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #444;
    }
</style>
""", unsafe_allow_html=True)

# Ensure the img directory exists
if not os.path.exists("img"):
    st.warning("The 'img' directory does not exist. Creating it now...")
    os.makedirs("img")
    st.info("Please place vf8.png and vf9.png in the newly created 'img' folder and restart the application.")

# Initialize session state variables
if 'show_vehicles' not in st.session_state:
    st.session_state.show_vehicles = False
if 'selected_vehicle' not in st.session_state:
    st.session_state.selected_vehicle = None
if 'booking_confirmed' not in st.session_state:
    st.session_state.booking_confirmed = False

# Header
st.markdown("<h1 class='main-header'>Book Your Airport Transfer</h1>", unsafe_allow_html=True)


# Define functions for selecting vehicles
def select_vf8():
    st.session_state.selected_vehicle = "VF8"
    st.session_state.vehicle_price = "1,200,000 VND"
    st.session_state.vehicle_type = "Premium 5-Seater SUV"


def select_vf9():
    st.session_state.selected_vehicle = "VF9"
    st.session_state.vehicle_price = "1,800,000 VND"
    st.session_state.vehicle_type = "Luxury 7-Seater SUV"


def confirm_booking():
    st.session_state.booking_confirmed = True


# Main application flow
if st.session_state.booking_confirmed:
    # Booking confirmation page
    st.markdown("<div class='confirmation-container'>", unsafe_allow_html=True)
    st.markdown("<h2 class='confirmation-header'>🎉 Booking Confirmed!</h2>", unsafe_allow_html=True)

    # Booking details
    st.markdown("<div class='confirmation-detail'>", unsafe_allow_html=True)
    st.markdown("<p class='detail-header'>Trip Details:</p>", unsafe_allow_html=True)
    st.markdown(f"**From:** {st.session_state.pickup_location}", unsafe_allow_html=True)
    st.markdown(f"**To:** {st.session_state.dropoff_location}", unsafe_allow_html=True)
    st.markdown(f"**Date:** {st.session_state.pickup_date.strftime('%B %d, %Y')}", unsafe_allow_html=True)
    st.markdown(f"**Time:** {st.session_state.pickup_time}", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Vehicle details
    st.markdown("<div class='confirmation-detail'>", unsafe_allow_html=True)
    st.markdown("<p class='detail-header'>Vehicle:</p>", unsafe_allow_html=True)
    st.markdown(f"**Model:** VinFast {st.session_state.selected_vehicle}", unsafe_allow_html=True)
    st.markdown(f"**Type:** {st.session_state.vehicle_type}", unsafe_allow_html=True)
    st.markdown(f"**Price:** {st.session_state.vehicle_price}", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Next steps
    st.markdown("<div class='confirmation-detail'>", unsafe_allow_html=True)
    st.markdown("<p class='detail-header'>Next Steps:</p>", unsafe_allow_html=True)
    st.markdown("""
    1. You will receive a confirmation email with your booking details
    2. Your driver will track your flight and meet you at the arrival hall
    3. Driver will wait up to 60 minutes after your flight lands at no extra charge
    4. For any changes, please contact our customer service at least 24 hours before pickup
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Support info
    st.markdown("<div class='confirmation-detail'>", unsafe_allow_html=True)
    st.markdown("<p class='detail-header'>Customer Support:</p>", unsafe_allow_html=True)
    st.markdown("**Email:** support@gfairporttransfer.com", unsafe_allow_html=True)
    st.markdown("**Phone:** +84 123 456 789", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Option to make another booking
    if st.button("Make Another Booking"):
        st.session_state.booking_confirmed = False
        st.session_state.selected_vehicle = None
        st.session_state.show_vehicles = False
        st.rerun()

elif st.session_state.selected_vehicle:
    # Passenger details and booking confirmation page
    st.markdown("<h2 class='section-header'>Passenger Details</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        passenger_name = st.text_input("Full Name", placeholder="Enter your full name")
        passenger_email = st.text_input("Email", placeholder="Enter your email address")

    with col2:
        passenger_phone = st.text_input("Phone Number", placeholder="Enter your phone number")
        flight_number = st.text_input("Flight Number (optional)", placeholder="e.g., VN123")

    st.markdown("<h2 class='section-header'>Booking Summary</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='confirmation-detail'>", unsafe_allow_html=True)
        st.markdown("<p class='detail-header'>Trip Details:</p>", unsafe_allow_html=True)
        st.markdown(f"**From:** {st.session_state.pickup_location}", unsafe_allow_html=True)
        st.markdown(f"**To:** {st.session_state.dropoff_location}", unsafe_allow_html=True)
        st.markdown(f"**Date:** {st.session_state.pickup_date.strftime('%B %d, %Y')}", unsafe_allow_html=True)
        st.markdown(f"**Time:** {st.session_state.pickup_time}", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='confirmation-detail'>", unsafe_allow_html=True)
        st.markdown("<p class='detail-header'>Vehicle Details:</p>", unsafe_allow_html=True)
        st.markdown(f"**Vehicle:** VinFast {st.session_state.selected_vehicle}", unsafe_allow_html=True)
        st.markdown(f"**Type:** {st.session_state.vehicle_type}", unsafe_allow_html=True)
        st.markdown(f"**Price:** {st.session_state.vehicle_price}", unsafe_allow_html=True)

        # Additional services
        st.markdown("<p class='detail-header' style='margin-top: 1rem;'>Included Services:</p>", unsafe_allow_html=True)
        st.markdown("- ✓ Professional English-speaking driver", unsafe_allow_html=True)
        st.markdown("- ✓ Flight tracking and 60-min wait time", unsafe_allow_html=True)
        st.markdown("- ✓ Free cancellation up to 24h before pickup", unsafe_allow_html=True)
        st.markdown("- ✓ Free bottled water and Wi-Fi", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Payment method
    st.markdown("<h2 class='section-header'>Payment Method</h2>", unsafe_allow_html=True)
    payment_method = st.radio(
        "Select payment method",
        ["Credit/Debit Card", "PayPal", "Pay Cash to Driver"],
        horizontal=True
    )

    if payment_method in ["Credit/Debit Card", "PayPal"]:
        st.info("In a real application, a secure payment form would be integrated here.")

    # Terms and conditions
    st.checkbox("I agree to the terms and conditions", key="terms_agreed")

    # Confirm booking button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Confirm Booking", type="primary", disabled=not st.session_state.get("terms_agreed", False)):
            # Save all form inputs to session state
            st.session_state.passenger_name = passenger_name
            st.session_state.passenger_email = passenger_email
            st.session_state.passenger_phone = passenger_phone
            st.session_state.flight_number = flight_number
            st.session_state.payment_method = payment_method

            # Set booking as confirmed
            confirm_booking()
            st.rerun()

    # Back button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Back to Vehicle Selection"):
            st.session_state.selected_vehicle = None
            st.rerun()

elif not st.session_state.show_vehicles:
    # Initial booking form
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pickup Location")
        pickup_location = st.selectbox(
            "Select pickup location",
            ["DAD - Da Nang International Airport", "HAN - Hanoi International Airport",
             "SGN - Ho Chi Minh City Airport"],
            label_visibility="collapsed"
        )

        st.subheader("Pickup Date")
        pickup_date = st.date_input(
            "Select date",
            datetime.date.today() + datetime.timedelta(days=1),
            label_visibility="collapsed"
        )

    with col2:
        st.subheader("Dropoff Location")

        # Create a container for dropoff location with the "Popular Choice" tag
        dropoff_container = st.container()
        with dropoff_container:
            col_drop, col_tag = st.columns([4, 1])
            with col_drop:
                dropoff_location = st.selectbox(
                    "Select dropoff location",
                    ["Hoi An", "Da Nang City Center", "Ba Na Hills", "My Khe Beach"],
                    label_visibility="collapsed"
                )
            with col_tag:
                if dropoff_location == "Hoi An":
                    st.markdown("<div class='popular-tag'>Popular Choice</div>", unsafe_allow_html=True)

        st.subheader("Pickup Time")
        pickup_time = st.selectbox(
            "Select time",
            ["00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00",
             "05:30", "06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00"],
            index=2,
            label_visibility="collapsed"
        )

    # Check Availability button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Check Availability", type="primary"):
            # Save form data to session state
            st.session_state.pickup_location = pickup_location
            st.session_state.dropoff_location = dropoff_location
            st.session_state.pickup_date = pickup_date
            st.session_state.pickup_time = pickup_time

            # Set session state to show vehicles
            st.session_state.show_vehicles = True
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Premium Fleet Section
    st.markdown("<div class='premium-fleet'>", unsafe_allow_html=True)
    st.markdown("<h2 class='premium-fleet-header'>Our Premium Fleet</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='fleet-card'>", unsafe_allow_html=True)

        # Load VF8 image from img folder
        try:
            vf8_image = Image.open("img/vf8.png")
            st.image(vf8_image, caption="", use_container_width=True)
        except FileNotFoundError:
            st.warning("VF8 image not found. Please place vf8.png in the img folder.")
            st.image("https://via.placeholder.com/600x400", caption="VF8 image placeholder", use_container_width=True)

        st.markdown("<h3>VinFast VF8</h3>", unsafe_allow_html=True)
        st.markdown("<p>Luxury 5-seater electric SUV with premium comfort</p>", unsafe_allow_html=True)

        st.markdown("<div class='fleet-detail'><span class='fleet-icon'>👥</span>5 Seats</div>", unsafe_allow_html=True)
        st.markdown("<div class='fleet-detail'><span class='fleet-icon'>✨</span>Premium Interior</div>",
                    unsafe_allow_html=True)
        st.markdown("<div class='fleet-detail'><span class='fleet-icon'>🔋</span>Up to 400km Range</div>",
                    unsafe_allow_html=True)
        st.markdown("<div class='fleet-detail'><span class='fleet-icon'>🧳</span>Spacious Luggage Space</div>",
                    unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='fleet-card'>", unsafe_allow_html=True)

        # Load VF9 image from img folder
        try:
            vf9_image = Image.open("img/vf9.png")
            st.image(vf9_image, caption="", use_container_width=True)
        except FileNotFoundError:
            st.warning("VF9 image not found. Please place vf9.png in the img folder.")
            st.image("https://via.placeholder.com/600x400", caption="VF9 image placeholder", use_container_width=True)

        st.markdown("<h3>VinFast VF9</h3>", unsafe_allow_html=True)
        st.markdown("<p>Premium 7-seater electric SUV for larger groups</p>", unsafe_allow_html=True)

        st.markdown("<div class='fleet-detail'><span class='fleet-icon'>👥</span>7 Seats</div>", unsafe_allow_html=True)
        st.markdown("<div class='fleet-detail'><span class='fleet-icon'>✨</span>Premium Interior</div>",
                    unsafe_allow_html=True)
        st.markdown("<div class='fleet-detail'><span class='fleet-icon'>🔋</span>Up to 450km Range</div>",
                    unsafe_allow_html=True)
        st.markdown("<div class='fleet-detail'><span class='fleet-icon'>🧳</span>Extra Luggage Space</div>",
                    unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Vehicle selection section
    st.markdown("<h2 class='section-header'>Select Your Vehicle</h2>", unsafe_allow_html=True)

    # Display trip details
    st.markdown(
        f"**From:** {st.session_state.pickup_location} • **To:** {st.session_state.dropoff_location} • **Date:** {st.session_state.pickup_date.strftime('%B %d, %Y')} • **Time:** {st.session_state.pickup_time}")

    # Vehicle data
    vf8_features = ["Professional Driver", "Free WiFi", "Luggage Assistance", "Free Bottled Water", "Flight Tracking",
                    "60-min Free Waiting"]
    vf9_features = ["Professional Driver", "Free WiFi", "Luggage Assistance", "Extra Luggage Space",
                    "Free Bottled Water", "Flight Tracking", "60-min Free Waiting", "Perfect for Groups"]

    # Display vehicle cards in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='vehicle-card'>", unsafe_allow_html=True)

        # Vehicle image - load from img folder
        try:
            vf8_image = Image.open("img/vf8.png")
            st.image(vf8_image, caption="VinFast VF8", use_container_width=True)
        except FileNotFoundError:
            st.warning("VF8 image not found. Please place vf8.png in the img folder.")
            st.image("https://via.placeholder.com/400x300", caption="VinFast VF8", use_container_width=True)

        st.markdown("""
            <div style='display: flex; align-items: center;'>
                <span class='vehicle-header'>VinFast VF8</span>
                <span class='best-deal-tag'>Best Deal</span>
            </div>
            <p class='vehicle-subheader'>Premium 5-Seater SUV</p>
            <p class='vehicle-price'>1,200,000 VND</p>
            <div class='feature-list'>
        """, unsafe_allow_html=True)

        for feature in vf8_features:
            st.markdown(f"<p class='feature-item'><span class='feature-icon'>✓</span> {feature}</p>",
                        unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Select VF8", key="select_vf8", use_container_width=True):
            select_vf8()
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='vehicle-card'>", unsafe_allow_html=True)

        # Vehicle image - load from img folder
        try:
            vf9_image = Image.open("img/vf9.png")
            st.image(vf9_image, caption="VinFast VF9", use_container_width=True)
        except FileNotFoundError:
            st.warning("VF9 image not found. Please place vf9.png in the img folder.")
            st.image("https://via.placeholder.com/400x300", caption="VinFast VF9", use_container_width=True)

        st.markdown("""
            <div style='display: flex; align-items: center;'>
                <span class='vehicle-header'>VinFast VF9</span>
            </div>
            <p class='vehicle-subheader'>Luxury 7-Seater SUV</p>
            <p class='vehicle-price'>1,800,000 VND</p>
            <div class='feature-list'>
        """, unsafe_allow_html=True)

        for feature in vf9_features:
            st.markdown(f"<p class='feature-item'><span class='feature-icon'>✓</span> {feature}</p>",
                        unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("Select VF9", key="select_vf9", use_container_width=True):
            select_vf9()
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # Pricing footnote
    st.markdown(
        "<p class='footnote'>* Prices are in Vietnamese Dong (VND). Additional charges may apply for waiting time or extra distance.</p>",
        unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>© 2025 GF Airport Chauffeur Service. All rights reserved.</div>",
            unsafe_allow_html=True)