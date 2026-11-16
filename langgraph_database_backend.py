# imports
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
# from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3
load_dotenv()

# Model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0.7
)

# Define State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Function
def chat_node(state : ChatState):
    messages = state["messages"]        # Take user Query From state
    response = llm.invoke(messages)     # send to llm
    return{'messages':[response]}       # Store response in state

#Checkpointer
# code for db integerate
conn = sqlite3.connect(database='chatbot.db',check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# Graph
graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node) # add node

graph.add_edge(START, 'chat_node') # add Edges
graph.add_edge('chat_node',END)

ChatBot = graph.compile(checkpointer=checkpointer) # Compile the Graph
# END


# code for db integerate
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)