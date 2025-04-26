import streamlit as st
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
    import pandas as pd
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Create a DataFrame for Streamlit's line_chart
    data = pd.DataFrame({'x': x, 'Sine Wave': y})

    # Display the plot using Streamlit's line_chart
    st.line_chart(data.set_index('x'))

    # Display the plot in Streamlit
    st.pyplot(fig)