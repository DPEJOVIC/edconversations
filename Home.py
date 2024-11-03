import streamlit as st

# Select GPT model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

st.title("Home")
st.subheader("Preparing and practicing for difficult conversations")
st.write("In Activity One, you will have the chance to prepare for a difficult conversation by interacting with a chatbot. You can choose the level of difficulty to help you practice having conversations with people who might be a little difficult and avoidant or defensive, or increasing in difficulty where the person is highly defensive and attacks back and finally at the hardest level, where the person is extremely disengaged to the point where the chatbot might just leave!")
st.write("\nIn Activity Two, you get the chance to debrief your interaction. You will work with a ‘supervisor’, who takes a coaching role and helps you unpack the conversation you have just had. In this conversation the supervisor unpacks where you went well and makes some suggestions for where you could grow and develop.")