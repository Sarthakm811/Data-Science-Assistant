import streamlit as st

st.set_page_config(
    page_title="AI Data Science Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Data Science Research Assistant")
st.write("Welcome to the AI Data Science Assistant!")

# Simple tabs
tab1, tab2, tab3 = st.tabs(["Home", "Upload", "Analysis"])

with tab1:
    st.header("Welcome")
    st.write("This is a simple test version")

with tab2:
    st.header("Upload Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        st.success("File uploaded!")

with tab3:
    st.header("Analysis")
    st.write("Analysis features coming soon")
