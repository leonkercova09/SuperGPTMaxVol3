import os
import openai
import streamlit as st
import blog_posts
import google_serp
import tokens_count
import prompts

# Load configurations from environment variables or use default values
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
TOP_P = float(os.getenv('TOP_P', '1.0'))
MODEL = os.getenv('MODEL', 'text-davinci-003')
SHOW_TOKEN_COST = os.getenv('SHOW_TOKEN_COST', 'True') == 'True'

# Set OpenAI API Key
openai.api_key = OPENAI_API_KEY

# Initialize Streamlit UI components
st.title("ChatGPT Max 3.0 🚀")

# Sidebar settings for Streamlit UI
st.sidebar.header("Settings")
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=TEMPERATURE)
top_p = st.sidebar.slider("Top P", min_value=0.0, max_value=1.0, value=TOP_P)
model_selection = st.sidebar.selectbox("Model", ["gpt-3.5-turbo", "gpt-4", "text-davinci-003"], index=2)

# Handling chat input and responses
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What do you want to do?", key="chat_input")

if prompt:
    if prompt.lower() == "/reset":
        st.session_state.messages = []
    else:
        # Processing the chat input based on specific commands
        # This is a simplified example; you'll need to expand it based on your actual functionalities.
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Example of handling a summarization request
        if prompt.lower().startswith("/summarize "):
            blog_url = prompt[11:]
            summary_prompt = blog_posts.get_blog_summary_prompt(blog_url)
            # Note: Implement get_blog_summary_prompt function in blog_posts.py as per your requirement
            
            # OpenAI GPT call for summarization
            response = openai.Completion.create(
                engine=MODEL,
                prompt=summary_prompt,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                max_tokens=150  # Adjust as per your requirement
            )
            summary = response.choices[0].text.strip()
            st.session_state.messages.append({"role": "assistant", "content": summary})
        
        # Add more elif blocks for other functionalities like /rewrite, /google, etc.
        
        # Example for generic response
        else:
            response = openai.Completion.create(
                engine=model_selection,
                prompt=prompt,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                max_tokens=150
            )
            reply = response.choices[0].text.strip()
            st.session_state.messages.append({"role": "assistant", "content": reply})
        
        # Optionally, display token usage and costs if SHOW_TOKEN_COST is True
        if SHOW_TOKEN_COST:
            token_usage = tokens_count.count_tokens(prompt + reply, MODEL)  # Implement count_tokens in tokens_count.py as needed
            cost = tokens_count.estimate_input_cost_optimized(MODEL, token_usage)  # Implement estimate_input_cost_optimized as needed
            st.sidebar.markdown(f"**Estimated Token Usage:** {token_usage} tokens")
            st.sidebar.markdown(f"**Estimated Cost:** ${cost:.6f}")
