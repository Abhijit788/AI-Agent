from dotenv import load_dotenv

load_dotenv()
from typing import Optional,Literal
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph,START,END
from openai import OpenAI
from typing_extensions import TypedDict,Literal

client = OpenAI()

llm = init_chat_model(model="gpt-4o-mini", model_provider="openai")


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    evaluation: Optional[str]
    is_good: Optional[bool]
    retry_count: int


def chatbot(state: State):
    print("\nchatbot node",state)
    client_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant.But you give wong answer to the user query."},
          {"role": "user", "content": state.get("user_query")}],
    )
    state["llm_output"] = client_response.choices[0].message.content
    return state

def evaluate_response(state:State)->Literal["chatbot_retry","endnode"]:
  response=client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role":"system", "content": f"Evaluate the following response and determine if it is good or not. Respond with 'good' or 'BAD: <brief reason>'. User query: {state.get('user_query')}. Response: {state.get('llm_output')}."}, 
        {"role": "user", "content": state.get("llm_output")}],
  )
  evaluation = response.choices[0].message.content.strip()

  state["evaluation"] = evaluation
  state["is_good"] = evaluation.lower() == "good"
  print("\nevaluate_response node",state)
  return state


def route_after_evaluation(state:State)->Literal["chatbot_retry","endnode"]:
  if state.get("retry_count")>=3:
    return "endnode"
  
  if state.get("is_good"):
    return "endnode"
  else:
    return "chatbot_retry"
  

def chatbot_retry(state:State):
  print("\nchatbot_retry node",state)
  response=client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "system", "content": "Generate a corrected answer.Use the evaluator's feedback to improve the previous answer."},
        {"role": "user", "content": f"User query: {state.get('user_query')}. Previous response: {state.get('llm_output')}. Evaluation: {state.get('evaluation')}."}
      ],
  )
  state["llm_output"] = response.choices[0].message.content   
  state["retry_count"]+=1
  return state


def endnode(state:State):
  print("\nendnode node",state)
  return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_retry", chatbot_retry)
graph_builder.add_node("endnode", endnode)
graph_builder.add_node("evaluate_response", evaluate_response)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "evaluate_response")
graph_builder.add_conditional_edges("evaluate_response", route_after_evaluation)
graph_builder.add_edge("chatbot_retry", "evaluate_response")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

updated_graph=graph.invoke({
  "user_query": "Hello, what is 4 +4.",
  "retry_count": 0
  }
  )
print("\nFinal output:",updated_graph)
