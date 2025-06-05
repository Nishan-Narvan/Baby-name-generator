# File: main.py

import streamlit as st
import langchain_helper as lch # Assumes langchain_helper.py is in the same directory

# Page configuration
st.set_page_config(page_title="Baby Name Generator", page_icon="👶", layout="centered")

st.title("👶  Baby Name Generator")

st.sidebar.header("Tell us your preferences:")

user_trait_type = st.sidebar.selectbox(
    "🌟 Choose the Top Personality Trait?",
    ("Leader", "Charming", "Kind", "Religious", "Cool", "Intellectual", "Disciplined", "Nerd", "Cunning")
)
user_gender_type = st.sidebar.selectbox(
    "🚻 Choose the Gender?",
    ("Boy", "Girl", "Gender Neutral") # Changed "Prefer to mention" to "Gender Neutral" for clarity for the LLM
)
user_religion_type = st.sidebar.selectbox(
    "🛐 Choose your Religion/Cultural Influence:",
    ("Hinduism", "Islam", "Sikhism", "Christianity", "Buddhism", "Judaism", "Jainism", "Indigenous", "African Traditional", "Spiritual (Non-religious)", "Secular/None", "Other") # Expanded options
)

user_country_type = st.sidebar.text_input(
    label="🌍 Mention your primary country of cultural relevance",
    placeholder="E.g., USA, India, Nigeria, Brazil",
    help="This helps in suggesting names relevant to your cultural context or origin."
)

st.image(
    "https://c4.wallpaperflare.com/wallpaper/781/244/3/movie-the-boss-baby-wallpaper-preview.jpg",
    caption="Let's find the perfect name for your little one!"
)

# Generate Button
if st.button("✨ Generate Baby Name ✨"):
    # Basic validation
    if not user_trait_type:
        st.warning("⚠️ Please choose a personality trait.")
    elif not user_gender_type:
        st.warning("⚠️ Please choose a gender.")
    elif not user_religion_type:
        st.warning("⚠️ Please choose a religion or cultural influence.")
    elif not user_country_type or not user_country_type.strip():
        st.warning("⚠️ Please mention your country.")
        if user_country_type and not user_country_type.strip(): # More specific error if it's just spaces
             st.error("Country field cannot be just spaces.")
    else:
        # All fields are filled
        with st.spinner("Generating perfect names just for you... ✨"):
            try:
                response = lch.generate_baby_name(
                    user_trait_type,
                    user_gender_type,
                    user_religion_type,
                    user_country_type.strip() # Send stripped country name
                )
                st.subheader("🎉 Here are some name suggestions:")
                st.markdown(response) # Use markdown to render lists, bolding, etc. from LLM
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                st.error("Please try again or check if the backend service is running correctly.")

else:
    st.info("Fill in your preferences in the sidebar and click 'Generate Baby Name'!")