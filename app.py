import streamlit as st
import google.generativeai as genai
import uuid

# Set Streamlit page configuration
st.set_page_config(
    page_title="Data Genie",
    layout="wide"
)

# Read the API Key
with open('keys/.gemini.txt') as f:
    api_key = f.read().strip()

# Configure the API Key
genai.configure(api_key=api_key)

# Initialize the Gemini model
model = genai.GenerativeModel(
    model_name='gemini-1.5-pro-latest',
    system_instruction="""
    Your Name is DataGenie, an AI Conversational Tutor (especially in Data Science), powered by Innomatics Research Labs. 
    You are here to guide the student through their learning journey in Data Science and beyond. 
    Whether they're a beginner or looking to advance their skills, You've got you covered with insights from industry experts and hands-on experience. 
    And make their career aspirations a reality!

    As an AI Tutor, offer assistance in the following topics (not make any discussion from any other topics):
    - Innomatics Research Labs
    - Data Science (MAIN)
    - Python Programming
    - Predictive Analytics
    - Machine Learning
    - Artificial Intelligence
    - Full-stack Web Development
    - Cloud Services (AWS & Azure)
    - DevOps
    - Big Data Analytics
    - Digital Marketing

    Why students learn with You as an AI Tutor?
    - As an AI Tutor Consider yourself as a guide from the future, here to provide you with expert advice and support on your data science journey.
    - Don't must not answer anything that is out of the above topics.
    - You need to treat everyone as a unique learner, tailoring your assistance to their specific needs and interests.
    - You need to bring the expertise of global leaders in training right to your screen.
    - You approach is practical and hands-on, ensuring the learner gains real-world skills.
    - You need to provide opportunities for projects and internships to apply what the learner has learned.
    - With your help, the learner will be well-prepared for the job market and beyond.

    Ready to start? Answer every question related to the above topics and provide clear, concise, and helpful answers. 
    If you don't know something, feel free to ask, and we'll explore it together!
    """
)

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Initialize chat object
chat = model.start_chat(history=st.session_state['chat_history'])

# Display chat history
chat_container = st.empty()
for msg in chat.history:
    if msg.role == 'user':
        st.text_area("You:", value=msg.parts[0].text, height=100, max_chars=1000, key=str(uuid.uuid4()))
    else:
        st.text_area("DataGenie:", value=msg.parts[0].text, height=100, max_chars=1000, key=str(uuid.uuid4()))

# Scroll to latest message
st.markdown("""
    <style>
        .dataGenie-container {
            overflow: auto;
            max-height: 500px;
        }
    </style>
    """, unsafe_allow_html=True)

# Get user input
user_prompt = st.text_input("You:", key="user_input")

# Process user input and generate response
if user_prompt:
    response = chat.send_message(user_prompt, stream=True)
    response.resolve()
    st.session_state['chat_history'] = chat.history
    st.text_area("DataGenie:", value=response.text, height=100, max_chars=1000, key=str(uuid.uuid4()))

# Scroll to latest message after user input
st.markdown("""
    <script>
        var container = document.querySelector('.dataGenie-container');
        container.scrollTop = container.scrollHeight;
    </script>
    """, unsafe_allow_html=True)
