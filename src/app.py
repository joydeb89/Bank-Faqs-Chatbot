import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

port = int(os.getenv("PORT", 8501))

# Load the FAQ dataset
faq_data = pd.read_csv("BankFAQs.csv")


questions = faq_data["Question"].tolist()
answers = faq_data["Answer"].tolist()

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(questions)

# Streamlit UI Styling
st.markdown(
    """
    <style>
    body {
        background-color: #e5ddd5;
    }
    .main {
        background-color: #e5ddd5;
    }
    .chat-container {
        max-width: 500px;
        margin: auto;
        padding: 10px;
        font-family: Arial, sans-serif;
    }
    .chat-bubble {
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
        display: inline-block;
        max-width: 80%;
    }
    .user-message {
        background-color: #dcf8c6;
        align-self: flex-end;
        text-align: right;
    }
    .bot-message {
        background-color: #ffffff;
        align-self: flex-start;
    }
    .message-container {
        display: flex;
        flex-direction: column;
    }
    .clear-btn {
        position: absolute;
        top: 10px;
        right: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and Clear Chat Button
col1, col2 = st.columns([4, 1])
col1.title("💬 Bank FAQs Chatbot")
if col2.button("🗑️"):
    st.session_state.chat_history = []

if __name__ == "__main__":
    import subprocess
    subprocess.run(["streamlit", "run", "app.py", "--server.port", str(port), "--server.enableCORS", "false"])

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_query = st.text_input("Type your message...")

if user_query:
    # Transform user query into a vector
    user_vector = vectorizer.transform([user_query])

    # Compute similarity
    similarity = cosine_similarity(user_vector, question_vectors)
    best_match_idx = similarity.argmax()

    # Get response
    if similarity[0, best_match_idx] > 0.2:  # Confidence threshold
        bot_response = answers[best_match_idx]
    else:
        bot_response = "I'm sorry, I couldn't find an answer to your question."

    # Append messages to chat history
    st.session_state.chat_history.append(("user", user_query))
    st.session_state.chat_history.append(("bot", bot_response))

# Display chat history in WhatsApp style
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for sender, message in st.session_state.chat_history:
    if sender == "user":
        st.markdown(
            f'<div class="message-container"><div class="chat-bubble user-message">{message}</div></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="message-container"><div class="chat-bubble bot-message">{message}</div></div>',
            unsafe_allow_html=True,
        )
st.markdown("</div>", unsafe_allow_html=True)
