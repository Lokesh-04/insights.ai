from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
import random 


# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def get_gemini_response(prompt):
    # Start a chat session and send the prompt
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)

    # Extract the main text from the response
    candidates = response._result.candidates
    main_text = candidates[0].content.parts[0].text
    return main_text

insights = []

def get_prompt():
    x = random.choice(insights)
    prompt = "hey i want you to act as habit coach, i am gonna give you a insight" + x + ".So make the given insight in to an actionable insight, so that i can easily apply that into my life."
    return prompt


# Streamlit app
st.title("Get ahead with actionable insights")

# prompt = st.text_input("Enter your prompt:")

# Insights Section
st.subheader("Add Insights")
insight = st.text_area("Enter your insight here:")
if st.button("Save Insight"):
    if insight.strip():
        # You can implement saving functionality here, e.g., saving to a file or database
        st.session_state.insights.append(insight)
        st.success("Insight saved!")
    else:
        st.error("Please enter an insight.")

# Display saved insights
st.subheader("Saved Insights")
if 'insights' not in st.session_state:
    st.session_state.insights = []

for i, saved_insight in enumerate(st.session_state.insights, start=1):
    st.write(f"{i}. {saved_insight}")
    insights.append(saved_insight)


if st.button("Get an actionable insight"):
    prompt = get_prompt()
    if prompt.strip():
        response_text = get_gemini_response(prompt)
        st.text_area("Generated Content:", response_text, height=400)
    else:
        st.error("Please enter a prompt.")


# Run the app with: streamlit run streamlit_app.py

# create an actionable insight