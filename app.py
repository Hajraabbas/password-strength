import streamlit as st
import re
import random
import string

# Custom CSS for styles & animations
st.markdown("""
    <style>
    /* Title Styling */
    .title {
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        color: white;
        animation: fadeIn 1s ease-in-out;
    }

    /* Password Label - Bigger & Bolder */
    .password-label {
        font-size: 1.8em;
        font-weight: bold;
        color: white;
        margin-bottom: 5px;
    }

    /* Styled Input Box */
    .stTextInput input {
        background-color: #222;
        color: white;
        border-radius: 8px;
        border: 1px solid #555;
        padding: 12px;
        width: 100%;
        transition: 0.3s;
        font-size: 1.3em;
    }

    /* Input Animation on Click */
    .stTextInput input:focus {
        background-color: white !important;
        color: black !important;
        border: 2px solid white;
        transform: scale(1.05);
    }

    /* Strength Display Box */
    .strength-box {
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-top: 10px;
        font-size: 1.3em;
        font-weight: bold;
        cursor: pointer;
        animation: fadeIn 0.8s ease-in-out;
    }

    /* Sidebar Styling - Larger Title */
    .sidebar-title {
        font-size: 1.8em !important;
        font-weight: bold;
        text-align: center;
        color: white;
        margin-bottom: 10px;
    }

    /* Password History Items */
    .history-item {
        font-size: 1.4em !important;
        font-weight: bold;
        color: white;
        margin-bottom: 10px;
        background-color: #444;
        padding: 10px;
        border-radius: 8px;
        cursor: pointer;
        transition: 0.3s;
    }

    /* Hover Effect for Strength & History */
    .history-item:hover, .strength-box:hover {
        background-color: #666;
        transform: scale(1.05);
    }

    /* Press Enter Animation */
    .press-enter {
        font-size: 1.3em;
        font-weight: bold;
        color: white;
        opacity: 0;
        animation: fadeIn 0.5s ease-in-out forwards;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for Password History
st.sidebar.markdown('<p class="sidebar-title">📜 Password History</p>', unsafe_allow_html=True)
if "password_history" not in st.session_state:
    st.session_state.password_history = []

# Function to check password strength
def check_password_strength(password):
    score = 0
    checks = [r".{8,}", r"[A-Z]", r"[a-z]", r"\d", r"[!@#$%^&*(),.?\":{}|<>]"]
    
    for check in checks:
        if re.search(check, password):
            score += 1
    
    strength_levels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    return strength_levels[score]

# Function to generate a strong password
def generate_strong_password():
    length = 12
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    return ''.join(random.choice(characters) for _ in range(length))

# UI
st.markdown('<h1 class="title">🔐 PASSWORD STRENGTH METER</h1>', unsafe_allow_html=True)

# Password Input Box
st.markdown('<p class="password-label">Enter Password:</p>', unsafe_allow_html=True)
password = st.text_input("", type="password")  

# Generate Strong Password Button
if st.button("🔄 Generate Strong Password"):
    strong_password = generate_strong_password()
    st.success(f"🔑 Strong Password: **{strong_password}**")

# Show "Press Enter" only when typing starts
if password:
    st.markdown('<p class="press-enter">Press Enter</p>', unsafe_allow_html=True)

if password:
    strength = check_password_strength(password)
    
    # Save to history
    if password not in st.session_state.password_history:
        st.session_state.password_history.insert(0, password)

    # Define color for each strength level
    color_dict = {
        "Very Weak": "#FF4B4B",
        "Weak": "#FF914D",
        "Moderate": "#FFD700",
        "Strong": "#5CD65C",
        "Very Strong": "#4CAF50"
    }
    
    # Strength Display Box
    st.markdown(f'<div class="strength-box" style="background-color:{color_dict[strength]}; color: black;">'
                f'🔒 <strong>Password Strength:</strong> {strength}</div>', unsafe_allow_html=True)

    # Additional Feedback
    if strength == "Very Weak":
        st.error("❌ Too weak! Try using a longer password with symbols and numbers.")
    elif strength == "Weak":
        st.warning("⚠️ Weak password! Add uppercase letters and special characters.")
    elif strength == "Moderate":
        st.info("ℹ️ Decent, but can be improved with more complexity.")
    elif strength == "Strong":
        st.success("✅ Strong password! Well done.")
    else:
        st.balloons()
        st.success("🎉 Excellent! Your password is very strong!")

# Show password history in the sidebar
for past_password in st.session_state.password_history[:5]:  
    st.sidebar.markdown(f'<p class="history-item">🔑 {past_password}</p>', unsafe_allow_html=True)
