# app_streamlit_fixed.py
import streamlit as st
import pandas as pd
import base64
import requests
import json
import hashlib
import os

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Agri-Tech ML Hub", page_icon="🌾", layout="wide")

# ---------------------------
# BACKGROUND IMAGE
# ---------------------------
BG_CANDIDATES = [
    "/mnt/data/A_high-resolution_digital_photograph_captures_a_ru.png",
    "/mnt/data/img2.jpg",
    "img2.jpg"
]

def get_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

def set_background():
    # Set the main app background
    main_bg_b64 = None
    for p in BG_CANDIDATES:
        b = get_base64(p)
        if b:
            main_bg_b64 = b
            break
    
    css = ""
    if main_bg_b64:
        css += f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{main_bg_b64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            /* Changed to BLACK for maximum readability */
            color: #000000; 
        }}
        </style>
        """

    css += """
    <style>
    /* Login/Dashboard Card */
    .card {
        background: rgba(255,255,255,0.92);
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.20);
        height: 100%;
    }
    /* Secondary Card */
    .semi-card {
        background: rgba(255,255,255,0.90);
        border-radius: 10px;
        padding: 14px;
    }
    
    /* BUTTON STYLING: Smaller, mobile-friendly, animated buttons */
    .stButton > button {
        /* Increased radius for rounded corners/pill shape */
        border-radius: 15px; 
        border: 1px solid #2E8B57; /* Sea Green border */
        color: #2E8B57; /* Sea Green text */
        background-color: #F0FFF0; /* Lightest green background */
        font-weight: 600;
        /* Further reduced vertical padding and font size for smallest size */
        padding: 0.15rem 0.5rem; 
        font-size: 0.8rem; /* Smaller font size */
        transition: all 0.2s ease-in-out;
        white-space: nowrap; /* Prevents text wrapping on very small screens */
    }
    .stButton > button:hover {
        background-color: #2E8B57; /* Darker green on hover */
        color: white;
        /* Subtle animation */
        transform: scale(1.05); 
    }
    
    /* CSS for making Recommended Crop and Metric output BOLDER and BIGGER */
    /* Targeting Streamlit metric value text for larger display (N, P, K values) */
    div[data-testid="stMetricValue"] {
        font-size: 2.0rem !important; /* Increase NPK metric value size */
        font-weight: 900 !important;
        color: #2E8B57 !important; /* Ensure metric value is also a dark color */
    }
    
    /* Targeting the final recommended crop text */
    .recommended-crop-output {
        font-size: 1.8em;
        font-weight: 900;
        color: #1E8449; /* Darker green for contrast */
    }
    
    /* Ensure input labels and placeholders are black on the card */
    .stTextInput label, .stSelectbox label, .stNumberInput label {
        color: #000000 !important;
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
            
set_background()
# Make results appear in white for visibility
st.markdown("""
<style>
/* NPK Metric values */
div[data-testid="stMetricValue"] {
    color: #FFFFFF !important;  /* White */
}

/* Recommended Crop output */
.recommended-crop-output {
    color: #FFFFFF !important;  /* White */
}

/* General text inside semi-card for better contrast if needed */
.semi-card, .card {
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)

# Make Recommended Crop and NPK metrics white and larger
st.markdown("""
<style>
/* NPK Metric values */
div[data-testid="stMetricValue"] {
    font-size: 2.2rem !important;  /* Larger font size */
    font-weight: 900 !important;   /* Bold */
    color: #FFFFFF !important;     /* White */
}

/* Recommended Crop output label */
.recommended-crop-output {
    font-size: 2.0rem !important;  /* Larger font size */
    font-weight: 900 !important;   /* Bold */
    color: #FFFFFF !important;     /* White */
}

/* Label "Recommended Crop Grown:" preceding the crop name */
div span[style*="font-weight:700"] {
    color: #FFFFFF !important;     /* White */
    font-size: 1.6rem !important;  /* Slightly larger */
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# CUSTOM STYLING FOR MESSAGES AND METRICS
# ---------------------------
st.markdown("""
<style>
/* Login/Signup/Reset success or error messages */
.stAlert {
    color: #FFFFFF !important;      /* White text for alerts */
    font-weight: 700 !important;    /* Bold */
    font-size: 1.2rem !important;   /* Slightly larger */
}

/* NPK Metric values on Fertilizer page */
div[data-testid="stMetricValue"] {
    font-size: 2.4rem !important;   /* Larger font size */
    font-weight: 900 !important;    /* Bold */
    color: #FFFFFF !important;      /* White */
}

/* Recommended Crop output label */
.recommended-crop-output {
    font-size: 2.2rem !important;   /* Larger font size */
    font-weight: 900 !important;    /* Bold */
    color: #FFFFFF !important;      /* White */
}

/* Label "Recommended Crop Grown:" preceding the crop name */
div span[style*="font-weight:700"] {
    color: #FFFFFF !important;      /* White */
    font-size: 1.8rem !important;   /* Slightly larger */
    font-weight: 900 !important;    /* Bold */
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# TRANSLATIONS (offline)
# ---------------------------
# UI Element Translations

TRANSLATIONS = {
    "en": {
        "Login":"Login","Username":"Username","Password":"Password","Enter username":"Enter username",
        "Enter password":"Enter password","Create New Account":"Create New Account","Cancel":"Cancel",
        "Forgot Password?":"Forgot Password?","Create Account":"Create Account","Choose Username":"Choose Username",
        "Choose Password":"Choose Password","Confirm Password":"Confirm Password","Sign Up":"Sign Up",
        "Reset Password":"Reset Password","Crop Recommendation":"Crop Recommendation",
        "Fertilizer Recommendation":"Fertilizer Recommendation","Predict Crop":"Predict Crop",
        "Recommended Crop Grown":"Recommended Crop Grown","Select Crop":"Select Crop",
        "Get Fertilizer Recommendation":"Get Fertilizer Recommendation","Menu":"Menu","Logout":"Logout",
        "Invalid username or password":"Invalid username or password","Login successful":"Login successful",
        "Account created. Please login.":"Account created. Please login.","Password reset successful":"Password reset successful",
        "User does not exist":"User does not exist", 
        "Nitrogen":"Nitrogen","Phosphorus":"Phosphorus","Potassium":"Potassium",
        "Temperature":"Temperature","Humidity":"Humidity","pH":"pH","Rainfall":"Rainfall","Soil Type":"Soil Type",
        "N":"N","P":"P","K":"K",
        "Enter Nitrogen":"Enter Nitrogen","Enter Phosphorus":"Enter Phosphorus","Enter Potassium":"Enter Potassium",
        "Enter Temperature":"Enter Temperature","Enter Humidity":"Enter Humidity","Enter pH":"Enter pH","Enter Rainfall":"Enter Rainfall",
        "Welcome to Agri Tech ML Hub":"🌾Welcome to Agri Tech ML Hub"
    },
    "hi": {
        "Login":"लॉगिन","Username":"उपयोगकर्ता नाम","Password":"पासवर्ड","Enter username":"उपयोगकर्ता नाम दर्ज करें",
        "Enter password":"पासवर्ड दर्ज करें","Create New Account":"नया खाता बनाएँ","Cancel":"रद्द करें",
        "Forgot Password?":"पासवर्ड भूल गए?","Create Account":"खाता बनाएँ","Choose Username":"उपयोगकर्ता नाम चुनें",
        "Choose Password":"पासवर्ड चुनें","Confirm Password":"पासवर्ड की पुष्टि करें","Sign Up":"साइन अप",
        "Reset Password":"पासवर्ड रीसेट करें","Crop Recommendation":"फ़सल सिफारिश",
        "Fertilizer Recommendation":"उर्वरक सिफारिश","Predict Crop":"फ़सल की भविष्यवाणी करें",
        "Recommended Crop Grown":"अनुशंसित फ़सल","Select Crop":"फ़सल चुनें",
        "Get Fertilizer Recommendation":"उर्वरक सुझाव प्राप्त करें","Menu":"मेन्यू","Logout":"लॉगआउट",
        "Invalid username or password":"अमान्य उपयोगकर्ता नाम या पासवर्ड","Login successful":"लॉगिन सफल",
        "Account created. Please login.":"खाता बना लिया गया। कृपया लॉगिन करें।","Password reset successful":"पासवर्ड सफलतापूर्वक रीसेट हुआ",
        "User does not exist":"उपयोगकर्ता मौजूद नहीं है",
        "Nitrogen":"नाइट्रोजन","Phosphorus":"फॉस्फोरस","Potassium":"पोटाशियम",
        "Temperature":"तापमान","Humidity":"आर्द्रता","pH":"पीएच","Rainfall":"वर्षा","Soil Type":"मिट्टी का प्रकार",
        "N":"एन","P":"पी","K":"के",
        "Enter Nitrogen":"नाइट्रोजन दर्ज करें","Enter Phosphorus":"फॉस्फोरस दर्ज करें","Enter Potassium":"पोटाशियम दर्ज करें",
        "Enter Temperature":"तापमान दर्ज करें","Enter Humidity":"आर्द्रता दर्ज करें","Enter pH":"पीएच दर्ज करें","Enter Rainfall":"वर्षा दर्ज करें",
        "Welcome to Agri Tech ML Hub":"🌾 एग्री टेक एमएल हब में आपका स्वागत है"
    },
    "kn": {
        "Login":"ಲಾಗಿನ್","Username":"ಬಳಕೆದಾರ ಹೆಸರು","Password":"ಪಾಸ್ವರ್ಡ್","Enter username":"ಬಳಕೆದಾರರ ಹೆಸರನ್ನು ನಮೂದಿಸಿ",
        "Enter password":"ಪಾಸ್ವರ್ಡ್ ನಮೂದಿಸಿ","Create New Account":"ಹೊಸ ಖಾತೆ ರಚಿಸಿ","Cancel":"ರದ್ದುಮಾಡಿ",
        "Forgot Password?":"ಪಾಸ್ವರ್ಡ್ ಮರೆತಿರಾ?","Create Account":"ಖಾತೆ ರಚಿಸಿ","Choose Username":"ಬಳಕೆದಾರ ಹೆಸರು ಆಯ್ಕೆಮಾಡಿ",
        "Choose Password":"ಪಾಸ್ವರ್ಡ್ ಆಯ್ಕೆಮಾಡಿ","Confirm Password":"ಪಾಸ್ವರ್ಡ್ ದೃಢೀಕರಿಸಿ","Sign Up":"ಸೈನ್ ಅಪ್",
        "Reset Password":"ಪಾಸ್ವರ್ಡ್ ಮರುಹೊಂದಿಸಿ","Crop Recommendation":"ಬೆಳೆ ಶಿಫಾರಸು",
        "Fertilizer Recommendation":"ರಸಗೊಬ್ಬರ ಶಿಫಾರಸು","Predict Crop":"ಬೆಳೆ ಊಹಿಸಿ",
        "Recommended Crop Grown":"ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆ","Select Crop":"ಬೆಳೆ ಆಯ್ಕೆಮಾಡಿ",
        "Get Fertilizer Recommendation":"ರಸಗೊಬ್ಬರ ಶಿಫಾರಸು ಪಡೆಯಿರಿ","Menu":"ಮೆನು","Logout":"ಲಾಗ್ಔಟ್",
        "Invalid username or password":"ಅಮಾನ್ಯ ಬಳಕೆದಾರ ಹೆಸರು ಅಥವಾ ಪಾಸ್ವರ್ಡ್","Login successful":"ಲಾಗಿನ್ ಯಶಸ್ವಿ",
        "Account created. Please login.":"ಖಾತೆ ರಚಿಸಲಾಗಿದೆ. ದಯವಿಟ್ಟು ಲಾಗಿನ್ ಮಾಡಿ.","Password reset successful":"ಪಾಸ್ವರ್ಡ್ ಯಶಸ್ವಿಯಾಗಿ ಮರುಹೊಂದಿಸಲಾಗಿದೆ",
        "User does not exist":"ಬಳಕೆದಾರರು ಸಿಗಲಿಲ್ಲ",
        "Nitrogen":"ನೈಟ್ರೋಜನ್","Phosphorus":"ಫಾಸ್ಫರಸ್","Potassium":"ಪೊಟ್ಯಾಸಿಯಮ್",
        "Temperature":"ತಾಪಮಾನ","Humidity":"ಆರ್ಡ್ರತೆ","pH":"ಪಿಎಚ್","Rainfall":"ವರ್ಷಾಪಾತ","Soil Type":"ಮಣ್ಣು ಪ್ರಕಾರ",
        "N":"ಎನ್","P":"ಪಿ","K":"ಕೆ",
        "Enter Nitrogen":"ನೈಟ್ರೋಜನ್ ನಮೂದಿಸಿ","Enter Phosphorus":"ಫಾಸ್ಫರಸ್ ನಮೂದಿಸಿ","Enter Potassium":"ಪೊಟ್ಯಾಸಿಯಮ್ ನಮೂದಿಸಿ",
        "Enter Temperature":"ತಾಪಮಾನ ನಮೂದಿಸಿ","Enter Humidity":"ಆರ್ಡ್ರತೆ ನಮೂದಿಸಿ","Enter pH":"ಪಿಎಚ್ ನಮೂದಿಸಿ","Enter Rainfall":"ವರ್ಷಾಪಾತ ನಮೂದಿಸಿ",
        "Welcome to Agri Tech ML Hub":"🌾 ಅಗ್ರಿ ಟೆಕ್ ಎಂಎಲ್ ಹಬ್‌ಗೆ ಸ್ವಾಗತ"
    }
}

# Crop Names Translations
CROP_NAMES_TRANSLATIONS = {
    "en": {
        "rice": "Rice", "maize": "Maize", "chickpea": "Chickpea", "kidneybeans": "Kidney Beans",
        "pigeonpeas": "Pigeon Peas", "mothbeans": "Moth Beans", "mungbean": "Mung Bean",
        "blackgram": "Black Gram", "lentil": "Lentil", "pomegranate": "Pomegranate",
        "banana": "Banana", "mango": "Mango", "grapes": "Grapes", "watermelon": "Watermelon",
        "muskmelon": "Muskmelon", "apple": "Apple", "orange": "Orange", "papaya": "Papaya",
        "coconut": "Coconut", "cotton": "Cotton", "jute": "Jute", "coffee": "Coffee"
    },
    "hi": {
        "rice": "चावल", "maize": "मक्का", "chickpea": "चना", "kidneybeans": "राजमा",
        "pigeonpeas": "अरहर", "mothbeans": "मोठ", "mungbean": "मूंग",
        "blackgram": "उड़द", "lentil": "मसूर", "pomegranate": "अनार",
        "banana": "केला", "mango": "आम", "grapes": "अंगूर", "watermelon": "तरबूज",
        "muskmelon": "खरबूजा", "apple": "सेब", "orange": "संतरा", "papaya": "पपीता",
        "coconut": "नारियल", "cotton": "कपास", "jute": "जूट", "coffee": "कॉफ़ी"
    },
    "kn": {
        "rice": "ಭತ್ತ", "maize": "ಮೆಕ್ಕೆ ಜೋಳ", "chickpea": "ಕಡಲೆ", "kidneybeans": "ರಾಜ್ಮಾ",
        "pigeonpeas": "ತೊಗರಿ ಬೇಳೆ", "mothbeans": "ಮೋಥ್ ಬೇಳೆ", "mungbean": "ಹೆಸರು ಬೇಳೆ",
        "blackgram": "ಉದ್ದಿನ ಬೇಳೆ", "lentil": "ಮಸೂರ್ ಬೇಳೆ", "pomegranate": "ದಾಳಿಂಬೆ",
        "banana": "ಬಾಳೆಹಣ್ಣು", "mango": "ಮಾವು", "grapes": "ದ್ರಾಕ್ಷಿ", "watermelon": "ಕಲ್ಲಂಗಡಿ",
        "muskmelon": "ಕಸ್ತೂರಿ ಕಲ್ಲಂಗಡಿ", "apple": "ಸೇಬು", "orange": "ಕಿತ್ತಳೆ", "papaya": "ಪಪ್ಪಾಯಿ",
        "coconut": "ತೆಂಗಿನಕಾಯಿ", "cotton": "ಹತ್ತಿ", "jute": "ಸೆಣಬು", "coffee": "ಕಾಫಿ"
    }
}

# Soil Types Translations
SOIL_TYPES_TRANSLATIONS = {
    "en": {
        "Alluvial": "Alluvial", "Loamy": "Loamy", "Loamy (Light Soil)": "Loamy (Light Soil)",
        "Sandy Loam": "Sandy Loam", "Black Soil (Regur)": "Black Soil (Regur)", "Laterite": "Laterite"
    },
    "hi": {
        "Alluvial": "जलोढ़ मिट्टी", "Loamy": "दोमट मिट्टी", "Loamy (Light Soil)": "दोमट (हल्की मिट्टी)",
        "Sandy Loam": "बलुई दोमट", "Black Soil (Regur)": "काली मिट्टी (रेगुर)", "Laterite": "लेटराइट मिट्टी"
    },
    "kn": {
        "Alluvial": "ಮೆಕ್ಕಲು ಮಣ್ಣು", "Loamy": "ಗೋಡು ಮಣ್ಣು", "Loamy (Light Soil)": "ಗೋಡು (ತಿಳಿಯಾದ ಮಣ್ಣು)",
        "Sandy Loam": "ಮರಳು ಮಿಶ್ರಿತ ಗೋಡು", "Black Soil (Regur)": "ಕಪ್ಪು ಮಣ್ಣು (ರೆಗೂರ್)", "Laterite": "ಲ್ಯಾಟರೈಟ್ ಮಣ್ಣು"
    }
}

#
def t(key):
    lang = st.session_state.get("lang", "en")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

# Functions for data value translations
def t_crop(key):
    lang = st.session_state.get("lang", "en")
    return CROP_NAMES_TRANSLATIONS.get(lang, CROP_NAMES_TRANSLATIONS["en"]).get(key.lower(), key)

def t_soil(key):
    lang = st.session_state.get("lang", "en")
    return SOIL_TYPES_TRANSLATIONS.get(lang, SOIL_TYPES_TRANSLATIONS["en"]).get(key, key)

# ---------------------------
# LANGUAGE SELECTOR
# ---------------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "en"

st.sidebar.title("🌐 Language")
st.session_state["lang"] = st.sidebar.selectbox("Choose language", ["en","hi","kn"],
                                               index=["en","hi","kn"].index(st.session_state["lang"]),
                                               format_func=lambda x: {"en":"English","hi":"Hindi","kn":"Kannada"}[x])

# ---------------------------
# USER SYSTEM
# ---------------------------
USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {"users": {}}
    try:
        return json.load(open(USER_FILE, "r"))
    except:
        return {"users": {}}

def save_users(data):
    json.dump(data, open(USER_FILE, "w"), indent=4)

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

# ---------------------------
# API endpoints
# ---------------------------
BASE_API = "http://127.0.0.1:5000"
CROP_PREDICT_URL = f"{BASE_API}/predict"
FERT_PREDICT_URL = f"{BASE_API}/fertilizer_recommendation"

# ---------------------------
# Load dataset
# ---------------------------
DATASET_PATH = "Crop_recommendation_with_soil.csv"
@st.cache_data
def load_data():
    if os.path.exists(DATASET_PATH):
        try:
            df = pd.read_csv(DATASET_PATH)
        except:
            # Fallback to empty DataFrame if file read fails
            df = pd.DataFrame(columns=["N","P","K","temperature","humidity","ph","rainfall","soil_type","label"])
    else:
        # Fallback to empty DataFrame if file does not exist
        df = pd.DataFrame(columns=["N","P","K","temperature","humidity","ph","rainfall","soil_type","label"])
    
    # Extract unique values, using fallbacks if columns are missing
    soils = sorted(df['soil_type'].dropna().unique().tolist()) if 'soil_type' in df.columns and not df.empty else ["Loamy","Sandy","Clayey"]
    crops = sorted(df['label'].dropna().unique().tolist()) if 'label' in df.columns and not df.empty else ["Wheat","Rice","Maize"]
    
    return df, soils, crops

# ---------------------------
# API CALLERS
# ---------------------------
def get_crop_recommendation(payload):
    try:
        r = requests.post(CROP_PREDICT_URL, json=payload, timeout=12)
        if r.ok:
            js = r.json()
            return js.get("recommended_crop"), js.get("error")
        else:
            return None, r.text
    except Exception as e:
        return None, str(e)

def get_fertilizer_recommendation(crop_name):
    try:
        r = requests.post(FERT_PREDICT_URL, json={"crop": crop_name}, timeout=12)
        if r.ok:
            js = r.json()
            return js.get("recommended_ratio"), js.get("error")
        else:
            return None, r.text
    except Exception as e:
        return None, str(e)

# ---------------------------
# DASHBOARD HEADER
# ---------------------------
def dashboard_header():
    st.markdown(
        f"<div style='text-align:center; margin-top:20px; margin-bottom:20px;'>"
        f"<h1 style='color:#FFFFFF; margin:0;'>{t('Welcome to Agri Tech ML Hub')}</h1>"
        "</div>", 
        unsafe_allow_html=True
    )

# ---------------------------
# CENTERED CARD HELPER 
# ---------------------------
def centered_card(inner_fn, width=400):
    st.markdown(f"<div style='display:flex; justify-content:center; margin-top:50px;'><div class='card' style='width:{width}px;'>", unsafe_allow_html=True)
    inner_fn()
    st.markdown("</div></div>", unsafe_allow_html=True)

# ---------------------------
# LOGIN / SIGNUP / RESET
# ---------------------------
def page_login():
    dashboard_header()
    def content():
        st.markdown(f"<h3 style='text-align:center; margin:6px 0; color:#2E8B57;'>{t('Login')}</h3>", unsafe_allow_html=True)
        uname = st.text_input(t("Username"), placeholder=t("Enter username"))
        pwd = st.text_input(t("Password"), type="password", placeholder=t("Enter password"))
        
        # Login and Cancel buttons on the same line
        c1, c2 = st.columns([1,1])
        with c1:
            if st.button(t("Login"), use_container_width=True):
                users = load_users()
                if uname in users.get("users", {}) and users["users"][uname]==hash_password(pwd):
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = uname
                    st.success(t("Login successful"))
                else:
                    st.error(t("Invalid username or password"))
        with c2:
            if st.button(t("Cancel"), use_container_width=True):
                st.experimental_rerun()
        
        # Add a small separator/spacer
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

        # Forgot Password and Create New Account buttons on a new line, aligned
        c3, c4 = st.columns([1, 1])
        with c3:
            if st.button(t("Forgot Password?"), use_container_width=True):
                st.session_state["page"]="ForgotPassword"
        with c4:
            if st.button(t("Create New Account"), use_container_width=True):
                st.session_state["page"]="Signup"

    centered_card(content, width=400)

def page_signup():
    dashboard_header()
    def content():
        st.markdown(f"<h3 style='text-align:center; margin:6px 0;'>{t('Create Account')}</h3>", unsafe_allow_html=True)
        u = st.text_input(t("Choose Username"))
        p = st.text_input(t("Choose Password"), type="password")
        c = st.text_input(t("Confirm Password"), type="password")
        if st.button(t("Sign Up")):
            users = load_users()
            if u in users.get("users", {}):
                st.error("Username already exists")
            elif p != c:
                st.error("Passwords do not match")
            else:
                users.setdefault("users", {})[u]=hash_password(p)
                save_users(users)
                st.success("Account created. Please login.")
                st.session_state["page"]="Login"
        if st.button(t("Cancel")):
            st.session_state["page"]="Login"
    centered_card(content, width=400)

def page_reset():
    dashboard_header()
    def content():
        st.markdown(f"<h3 style='text-align:center; margin:6px 0;'>{t('Reset Password')}</h3>", unsafe_allow_html=True)
        u = st.text_input(t("Enter username"))
        npw = st.text_input(t("New Password"), type="password")
        cpw = st.text_input(t("Confirm Password"), type="password")
        if st.button(t("Reset Password")):
            users = load_users()
            if u not in users.get("users", {}):
                st.error(t("User does not exist"))
            elif npw != cpw:
                st.error("Passwords do not match")
            else:
                users["users"][u]=hash_password(npw)
                save_users(users)
                st.success(t("Password reset successful"))
                st.session_state["page"]="Login"
        if st.button(t("Cancel")):
            st.session_state["page"]="Login"
    centered_card(content, width=400)

# ---------------------------
# CROP / FERTILIZER PAGES
# ---------------------------
def page_crop(soils):
    st.markdown("<div class='semi-card'>", unsafe_allow_html=True)
    st.header(t("Crop Recommendation"))
    
    with st.form("crop_form"):
        c1, c2 = st.columns(2)
        
        with c1:
            n = st.number_input(f"{t('Nitrogen')} ({t('N')})", value=90.0, help=t("Enter Nitrogen"))
            p = st.number_input(f"{t('Phosphorus')} ({t('P')})", value=42.0, help=t("Enter Phosphorus"))
            k = st.number_input(f"{t('Potassium')} ({t('K')})", value=43.0, help=t("Enter Potassium"))
            soil = st.selectbox(t("Soil Type"), soils, format_func=t_soil)

        with c2:
            temp = st.number_input(t("Temperature"), value=25.0, help=t("Enter Temperature"))
            hum = st.number_input(t("Humidity"), value=75.0, help=t("Enter Humidity"))
            ph_val = st.number_input(t("pH"), value=6.5, help=t("Enter pH"))
            rain = st.number_input(t("Rainfall"), value=150.0, help=t("Enter Rainfall"))
        
        submitted = st.form_submit_button(t("Predict Crop"))

    if submitted:
        payload = {"N": n, "P": p, "K": k, "temperature": temp, "humidity": hum, "ph": ph_val, "rainfall": rain, "soil_type": soil}
        crop, err = get_crop_recommendation(payload)
        if crop:
            st.session_state["last_crop"] = str(crop)
            translated_crop_name = t_crop(str(crop))
            st.success(f"**{t('Recommended Crop Grown')}: {translated_crop_name.upper()}**")
            st.session_state["page"] = "Fertilizer Recommendation"
        else:
            st.error(err or "Prediction error")
    
    st.markdown("</div>", unsafe_allow_html=True)

def page_fertilizer(crops):
    st.markdown("<div class='semi-card'>", unsafe_allow_html=True)
    st.header(t("Fertilizer Recommendation"))

    # Use format_func to display translated crop name
    crop = st.selectbox(t("Select Crop"), crops, format_func=t_crop)

    if st.button(t("Get Fertilizer Recommendation")):
        ratio, err = get_fertilizer_recommendation(crop)
        if ratio:
            # Display N,P,K metrics bigger and white
            c1, c2, c3 = st.columns(3)
            c1.metric(label=f"{t('N')}", value=f"{ratio.get('N')}", delta=None)
            c2.metric(label=f"{t('P')}", value=f"{ratio.get('P')}", delta=None)
            c3.metric(label=f"{t('K')}", value=f"{ratio.get('K')}", delta=None)
        else:
            st.error(err or "No fertilizer data")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# MAIN
# ---------------------------
def main():
    df, soils, crops = load_data()

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = "Login"

    if st.session_state["logged_in"]:
        st.sidebar.markdown(f"**👤 {st.session_state.get('user','')}**")
        if st.sidebar.button(t("Logout")):
            st.session_state["logged_in"] = False
            st.session_state["page"] = "Login"

        menu = [t("Crop Recommendation"), t("Fertilizer Recommendation")]
        choice = st.sidebar.selectbox(t("Menu"), menu)

        dashboard_header()  # Dashboard header for logged-in pages

        if choice == t("Crop Recommendation"):
            page_crop(soils)
            # Show Recommended Crop only on Crop Recommendation page
            if "last_crop" in st.session_state:
                translated_last_crop = t_crop(st.session_state['last_crop'])
                st.markdown(
                    f"<div style='text-align:center; margin-top:18px;'>"
                    f"<span style='font-weight:700; font-size:20px; color:white;'>{t('Recommended Crop Grown')}:</span>"
                    f"<span class='recommended-crop-output' style='color:white; font-size:20px;'>{translated_last_crop.upper()}</span>"
                    "</div>", unsafe_allow_html=True
                )

        else:
            page_fertilizer(crops)  # Fertilizer page does NOT show Recommended Crop

    else:
        page = st.session_state.get("page", "Login")
        if page == "Login":
            page_login()
        elif page == "Signup":
            page_signup()
        elif page == "ForgotPassword":
            page_reset()
        else:
            page_login()


if __name__ == "__main__":
    main()
