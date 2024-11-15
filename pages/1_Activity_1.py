import streamlit as st
from openai import OpenAI

st.title("Activity 1: Difficult Conversations")


if "level" not in st.session_state:
    st.session_state["level"] = ""

if "diffchanged" not in st.session_state:
    st.session_state["diffchanged"] = False

# Select GPT model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Initialise response counter
if "response_counter" not in st.session_state:
    st.session_state.response_counter = 0

# Initialise chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Set up OpenAI API client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "part_1_done" not in st.session_state:
    st.session_state["part_1_done"] = False

###############
def diffchange():
    st.session_state["diffchanged"] = True

option = st.selectbox(label="Select a difficulty level for the conversation:", 
                        options=("Level 1", "Level 2", "Level 3"),
                        index=None,
                        placeholder="Choose a difficulty level",
                        disabled=st.session_state["diffchanged"],
                        on_change=diffchange)

if option:
    st.session_state["level"] = option

###############

if not st.session_state["diffchanged"]:
    exit()

# Read system prompt and level
with open("./prompts/teacherpeerprompt.txt", "r") as file:
    systemprompt = file.read()

if st.session_state["level"] == "Level 1":
    with open("./prompts/level1.txt", "r") as file:
        levelprompt = file.read()
elif st.session_state["level"] == "Level 2":
    with open("./prompts/level2.txt", "r") as file:
        levelprompt = file.read()
else:
    with open("./prompts/level3.txt", "r") as file:
        levelprompt = file.read()

systemprompt = f"{systemprompt} \n\n {levelprompt}"

###############

# Write greeting & chat history
with st.chat_message("assistant"):
    st.markdown("Welcome! Don’t worry, this is a safe space for practicing your skills. Things might get heated but just remember its not personal and I’m not real!")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat logic
if prompt := st.chat_input("Write a response here", disabled = st.session_state.response_counter >= 10):

    st.session_state["part_1_done"] = True

    st.session_state.chat_history.append({"role": "user", "content": prompt})

    if st.session_state.response_counter < 10:
    
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            messages_with_system_prompt = [{"role": "system", "content": systemprompt}] + [
                {"role": m["role"], "content": m["content"]}
            for m in st.session_state.chat_history
            ]

            stream = client.chat.completions.create(
                model = st.session_state["openai_model"],
                messages = messages_with_system_prompt,
                stream = True,
            )
            response = st.write_stream(stream)

        st.session_state.response_counter += 1
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    else:
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            st.markdown("That was intense. I hope you feel like you are really prepared to go have a difficult conversation with a real person! You nailed it!")
        
        st.session_state.chat_history.append({"role": "assistant", "content": "That was intense. I hope you feel like you are really prepared to go have a difficult conversation with a real person! You nailed it!"})
