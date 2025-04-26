import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Graphics"])

# Home Page
if page == "Home":
    st.title("Welcome to the Streamlit App")
    st.write("This is a simple app with multiple pages and some graphics.")
    st.image(
        "https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png",
        width=300,
    )
    st.write("Use the sidebar to navigate between pages.")

# Graphics Page
elif page == "Graphics":
    st.title("Graphics Page")
    st.write("Here is a simple sine wave plot:")

    # Generate data for the plot
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(x, y, label="Sine Wave")
    ax.set_title("Sine Wave")
    ax.set_xlabel("x-axis")
    ax.set_ylabel("y-axis")
    ax.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)