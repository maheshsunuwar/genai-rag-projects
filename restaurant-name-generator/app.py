import streamlit as st
import langchain_helper

st.title("Restaurant Name Generator")

# save a value in `cuisine` variable after it gets selected
cuisine = st.sidebar.selectbox(
    "Pick a Cuisine", ("Nepali", "Italian", "Indian", "Mexican", "Chinese")
)

if cuisine:
    response = langchain_helper.generate_restaurant_name_and_items(cuisine)

    st.header(response['restaurant_name'])
    menu_items = response['menu_items'].split(",")

    st.write("There are menu items")
    for item in menu_items:
        st.write("-", item)
