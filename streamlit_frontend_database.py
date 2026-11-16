import streamlit as st
from langgraph_database_backend import ChatBot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid

# --- utility Functions ---

# def generate_thread_id():
#     thread_id = uuid.uuid4()
#     return thread_id

# (Chat gpt code)
def generate_thread_id():
    existing_threads = st.session_state.get('chat_threads', [])
    max_num = 0
    for t in existing_threads:
        t_str = str(t)
        if t_str.startswith("thread "):
            try:
                num = int(t_str.split(" ")[1])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
    return f"thread {max_num + 1}"

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return ChatBot.get_state(config={'configurable': {'thread_id':thread_id}}).values['messages']

def extract_text(content):
    """Helper to safely extract plain text from Gemini's list-of-dicts or string content."""
    if isinstance(content, list):
        return "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return str(content) if content else ""



# --- Header / Title ---
st.title("🤖 AI Assistant ChatBot")
st.caption("Built using LangGraph, Gemini Model & Streamlit")
st.divider()

# --- session Setup ---
# if 'message_history' not in st.session_state:
#     st.session_state['message_history'] = []

# if 'thread_id' not in st.session_state:
#     st.session_state['thread_id'] = generate_thread_id()

# if 'chat_threads' not in st.session_state:
#     st.session_state['chat_threads'] = retrieve_all_threads()

# add_thread(st.session_state['thread_id'])

# --- session Setup --- (chat gpt code)
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Load existing threads FIRST
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

# Generate new thread_id SECOND
if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

add_thread(st.session_state['thread_id'])


# --- sidebar UI ---
st.sidebar.title('LangGraph ChatBot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header("My_conversation")

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            clean_content = extract_text(msg.content)
            temp_messages.append({'role':role, 'content':clean_content})
        
        st.session_state['message_history'] = temp_messages

# loading the converstion history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input('Type here')

if user_input:

    # First add the message to message_history
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message("user"):
        st.text(user_input)


    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    # with st.chat_message("assistant"):

    #     ai_message = st.write_stream(
    #         message_chunk.content for message_chunk, metadata in ChatBot.stream(
    #             {'messages' : [HumanMessage(content=user_input)]},
    #             config = CONFIG,
    #             stream_mode='messages'
    #         )
    #     )
    # st.session_state['message_history'].append({'role':'assistant','content':ai_message})

    # As i am not using chat openai model , i am using gemini model so i have to use below code as this model give output in list form
    with st.chat_message("assistant"):
        
        def generate_response():
            for message_chunk, metadata in ChatBot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            ):
                content = message_chunk.content
                
                # If content is a list of dictionaries (newer Gemini format)
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            yield block.get("text", "")
                # Fallback if content is already a plain string
                elif isinstance(content, str):
                    yield content

        ai_message = st.write_stream(generate_response())

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

# --- Footer at the end ---
st.markdown(
    """
    <div style='position: fixed; bottom: 10px; right: 20px; color: gray; font-size: 12px;'>
        Powered by LangGraph & Gemini ✨
    </div>
    """,
    unsafe_allow_html=True
)
        