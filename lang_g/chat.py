from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from typing import Annotated
from langgraph.graph import StateGraph,START,END

class State(TypedDict):
  messages: Annotated[list,add_messages]

def chatbot(State:State):
  print("This is inside the chatbot node :",State)
  print("\n")
  return {"messages":"This is message returned from the chatbot node."}

def samplenode(State:State):
  print("This is inside the samplenode node :",State)
  print("\n")
  return {"messages":"This is message returned from the samplenode node."}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("samplenode",samplenode)

graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("chatbot","samplenode")
graph_builder.add_edge("samplenode",END)

graph = graph_builder.compile()

updated_state=graph.invoke(State({"messages":["HI, my name is Abhijit."]}))
print("\n Updated State after graph execution:",updated_state)