# https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# UI start
st.title("ChatGPT-like clone")

st.session_state.notion_url = st.text_input("notion url", value="", placeholder="notion url")

if "output" in st.session_state:
    st.text_area("output", value=st.session_state.output, disabled=True)

if st.button("Submit"):
    st.session_state.output = 'こんにちは、Streamlit！'
    stream = client.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )
    response = st.write_stream(stream)
