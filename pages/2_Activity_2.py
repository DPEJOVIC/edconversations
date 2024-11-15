import streamlit as st
from openai import OpenAI

st.title("Activity 2: Debrief")

if "part_1_done" not in st.session_state:
    st.session_state["part_1_done"] = False

if not st.session_state["part_1_done"]:
    st.write("Please complete Activity 1 first.")
    exit()

# Initialise response counter
if "response_counter_2" not in st.session_state:
    st.session_state.response_counter_2 = 0

# Select GPT model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialise chat history
if "chat_history_2" not in st.session_state:
    st.session_state.chat_history_2 = []

# Set up OpenAI API client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

###############

# Read system prompt
with open("./prompts/debrief.txt", "r") as file:
    systemprompt = file.read()

a1_messages = st.session_state["chat_history"]
formatted_messages = "\n".join([f"{message['role'].capitalize()}: {message['content']}" for message in a1_messages])

systemprompt = f"{systemprompt} \n\n {formatted_messages}"

###############

# Write greeting & chat history
with st.chat_message("assistant"):
    st.markdown("Welcome! Reflection on our practice is essential. It is great you have come here for some feedback. Feedback can be difficult to accept, but it is useful information to help us grow.")

for message in st.session_state.chat_history_2:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat logic
if prompt := st.chat_input("Write a response here", disabled = st.session_state.response_counter_2 >= 10):

    st.session_state["part_1_done"] = True
    
    st.session_state.chat_history_2.append({"role": "user", "content": prompt})

    if st.session_state.response_counter_2 < 10:
    
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            messages_with_system_prompt = [{"role": "system", "content": systemprompt}] + [
                {"role": m["role"], "content": m["content"]}
            for m in st.session_state.chat_history_2
            ]

            stream = client.chat.completions.create(
                model = st.session_state["openai_model"],
                messages = messages_with_system_prompt,
                stream = True,
            )
            response = st.write_stream(stream)

        st.session_state.response_counter_2 += 1
        st.session_state.chat_history_2.append({"role": "assistant", "content": response})
    
    else:
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            st.markdown("Well done. Engaging with the feedback will help you improve. Keep up with your practice.")
        
        st.session_state.chat_history_2.append({"role": "assistant", "content": "Well done. Engaging with the feedback will help you improve. Keep up with your practice."})
