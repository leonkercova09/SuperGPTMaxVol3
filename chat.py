import streamlit as st
import openai
import blog_posts
import tokens_count

# Load the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai_api_key"]

st.title("ChatGPT Max 3.0 🚀")

# Sidebar settings for Streamlit UI
st.sidebar.header("Settings")
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
top_p = st.sidebar.slider("Top P", min_value=0.0, max_value=1.0, value=1.0)
model_selection = st.sidebar.selectbox("Model", ["gpt-3.5-turbo", "gpt-4", "text-davinci-003"], index=2)

# Initialize or clear chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("What do you want to do?", key="chat_input")

if prompt:
    if prompt.lower() == "/reset":
        st.session_state.messages = []
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Example: Summarize a blog post
        if prompt.lower().startswith("/summarize "):
            blog_url = prompt[11:]
            summary_prompt = blog_posts.get_blog_summary_prompt(blog_url)  # Assume implementation in blog_posts.py
            
            response = openai.Completion.create(
                engine=model_selection,
                prompt=summary_prompt,
                temperature=temperature,
                top_p=top_p,
                max_tokens=150
            )
            summary = response.choices[0].text.strip()
            st.session_state.messages.append({"role": "assistant", "content": summary})
        
        # Generic response for other prompts
        else:
            response = openai.Completion.create(
                engine=model_selection,
                prompt=prompt,
                temperature=temperature,
                top_p=top_p,
                max_tokens=150
            )
            reply = response.choices[0].text.strip()
            st.session_state.messages.append({"role": "assistant", "content": reply})
        
        # Display token usage and cost (implementation needed in tokens_count.py)
        if st.sidebar.checkbox("Show token cost"):
            token_usage = tokens_count.count_tokens(prompt + reply)  # Implement this function in tokens_count.py
            cost = tokens_count.estimate_cost(token_usage)  # Implement this function in tokens_count.py
            st.sidebar.markdown(f"**Token Usage:** {token_usage} tokens")
            st.sidebar.markdown(f"**Estimated Cost:** ${cost:.6f}")
