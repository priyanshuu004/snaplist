import streamlit as st
from PIL import Image
from google import genai

# Page ki setting aur title
st.set_page_config(page_title="SnapList AI", layout="centered")
st.title("SnapList AI")
st.write("Apne item ki ek photo upload karein aur turant marketplace listing banayein.")

# Streamlit Secrets se Gemini API key padhein
api_key = st.secrets.get("GEMINI_API_KEY")

# Sidebar mein marketplace aur currency chunne ke options
with st.sidebar:
    st.header("Listing Preferences")
    platform = st.selectbox(
        "Target Marketplace",
        ["OLX", "Facebook Marketplace", "eBay", "Poshmark"]
    )
    currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)"])
    notes = st.text_input(
        "Optional Notes (brand, size, flaws)",
        placeholder="jaise: Size M, bilkul nayi jaisi condition"
    )

# Photo upload karne ka box
uploaded_file = st.file_uploader("Item ki photo upload karein", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Item", use_container_width=True)

    if st.button("Generate Listing", type="primary"):
        if not api_key:
            st.error("API Key nahi mili! Kripya Streamlit Secrets mein GEMINI_API_KEY add karein.")
        else:
            with st.spinner("Photo analyze ho rahi hai aur listing ban rahi hai..."):
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = (
                        f"Analyze this item photo and write a ready-to-post listing for {platform}. "
                        f"Seller notes: '{notes or 'None'}'. Include: 1) Catchy Title, "
                        f"2) Competitive Resale Price Range in {currency}, 3) Condition Assessment, "
                        f"4) Key Specifications, and 5) Platform-Tailored Sales Description."
                    )

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=
                    )

                    st.subheader("Aapki Marketplace Listing Taiyar Hai")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
