import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fuzzywuzzy import process

# Function to load FAQ data
@st.cache_data
def load_faq_data(file):
    df = pd.read_csv(file)
    return df["Question"].tolist(), df["Answer"].tolist()

# Sidebar for uploading a custom FAQ CSV
st.sidebar.title("📂 Upload FAQ CSV")
uploaded_file = st.sidebar.file_uploader("Upload your FAQ CSV", type=["csv"])

# Load default or uploaded FAQs
if uploaded_file is not None:
    questions, answers = load_faq_data(uploaded_file)
    st.sidebar.success("✅ FAQ file uploaded successfully!")
else:
    default_faq = "E:/GUVI/faqs/flipkart_faqs_cleaned.csv"
    questions, answers = load_faq_data(default_faq)

# Function to find the best matching answer
def get_best_match(user_query):
    best_match, score = process.extractOne(user_query, questions)
    if score > 60:
        return answers[questions.index(best_match)]
    return "Sorry, I couldn't find an answer. Please contact support."

# Dictionary to store FAQ counts (Tracking most-asked questions)
faq_counter = {}

# Streamlit UI
st.title("🛍 Flipkart Seller FAQ Chatbot")
st.write("Ask any question related to Flipkart seller policies!")

# Chat Input
user_query = st.text_input("💬 Ask a question:")

if user_query:
    response = get_best_match(user_query)
    st.write(f"🤖 **Chatbot:** {response}")

    # Update FAQ counter
    faq_counter[user_query] = faq_counter.get(user_query, 0) + 1

# Show Most-Asked Questions
if st.sidebar.checkbox("📊 Show Most-Asked Questions"):
    st.sidebar.subheader("📈 Most Popular Questions:")
    sorted_faqs = sorted(faq_counter.items(), key=lambda x: x[1], reverse=True)

    for question, count in sorted_faqs[:5]:  # Show top 5
        st.sidebar.write(f"🔹 {question} ({count} times)")

    # Display chart
    st.sidebar.subheader("📊 FAQ Popularity Chart")
    fig, ax = plt.subplots()
    ax.barh([q for q, _ in sorted_faqs[:5]], [c for _, c in sorted_faqs[:5]])
    st.sidebar.pyplot(fig)
