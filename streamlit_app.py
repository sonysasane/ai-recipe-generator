import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(page_title="Recipe Generator", page_icon="🍳")


def get_api_key():
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "google_api_key"):
        value = os.getenv(name)
        if value:
            return value
    return st.secrets.get("GEMINI_API_KEY")


@st.cache_resource
def get_client():
    api_key = get_api_key()
    if not api_key:
        st.error("No API key found. Set GEMINI_API_KEY in your .env file or Streamlit secrets.")
        st.stop()
    return genai.Client(api_key=api_key)


def give_recipe(ingredients, cuisine, diet_type):
    prompt = f'''Generate a recipe based on given ingredients: {", ".join(ingredients)}
    The recipe should not be more than 100 words, it should be concise and clear.
    You can use any cuisine like Indian, Mexican, American etc. cuisine: {cuisine}
    Diet_type can be non vegetarian, vegetarian, vegan and other possible diets etc. diet_type: {diet_type}
    '''
    client = get_client()
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )
    return response.text


st.title("🍳 Recipe Generator")
st.caption("Tell me what you have, and I'll cook up a recipe for you.")

ingredients_input = st.text_input(
    "Ingredients (comma separated)",
    placeholder="e.g. potatoes, chicken, wheat flour",
)

col1, col2 = st.columns(2)
with col1:
    cuisine = st.selectbox(
        "Cuisine",
        ["Any", "Indian", "American", "Mexican", "Italian", "Chinese", "Thai", "Mediterranean"],
    )
with col2:
    diet_type = st.selectbox(
        "Diet type",
        ["Any", "Vegetarian", "Non-vegetarian", "Vegan", "Keto", "Gluten-free"],
    )

if st.button("Generate Recipe", type="primary"):
    ingredients = [i.strip() for i in ingredients_input.split(",") if i.strip()]
    if not ingredients:
        st.warning("Please enter at least one ingredient.")
    else:
        with st.spinner("Cooking up your recipe..."):
            try:
                recipe = give_recipe(ingredients, cuisine, diet_type)
                st.markdown(recipe)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
