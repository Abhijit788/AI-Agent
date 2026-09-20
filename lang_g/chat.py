from dotenv import load_dotenv
load_dotenv()
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import Annotated
from langgraph.graph import StateGraph,START,END
from langchain.chat_models import init_chat_model\


llm = init_chat_model(
    model="gpt-4o-mini",
    model_provider="openai"
)

class State(TypedDict):
  messages: Annotated[list,add_messages]

def chatbot(state:State):
  response=llm.invoke(state.get("messages"))
  print("\n")
  return {"messages":response}

def samplenode(state:State):
  print("This is inside the samplenode node :",state)
  print("\n")
  return {"messages":"This is sample message append"}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("samplenode",samplenode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","samplenode")
graph_builder.add_edge("samplenode",END)

graph = graph_builder.compile()

updated_state=graph.invoke(State({"messages":["HI, my name is Abhijit."]}))
print("\n Updated State after graph execution:",updated_state)