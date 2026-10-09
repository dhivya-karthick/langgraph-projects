from .prompts import HANDBOOK_ANS_PROMPT, ORDER_TOOL_PROMPT, ROUTER_PROMPT

from .state import OrderDetails, Route

from .rag import build_retriever,format_docs
from .tools import ORDER_TOOL
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from .config import (LLM_MODEL)
import json

llm = ChatOpenAI(model= LLM_MODEL)

retriver = build_retriever()
tools = ToolNode(ORDER_TOOL)
llm_with_tools = llm.bind_tools(ORDER_TOOL)

def latest_question(state:OrderDetails) ->str:
    """the most recent thing the user typed"""
    for message in reversed(state["messages"]):
        if isinstance(message,HumanMessage):
            return message.content
    return ""

class RouteDescison(BaseModel):
    """The router's decision. with_structured_output forces the LLM to fill this."""
    route:Route = Field(description ="The single route that this question belongs to")
    description:str = Field(description ="Short explaination of the route choice")

router_llm = llm.with_structured_output(RouteDescison)

#node 1
def order_router(state:OrderDetails):
  
    decision =router_llm.invoke(
    [
        SystemMessage(content= ROUTER_PROMPT),
        HumanMessage(content=latest_question(state))
    ]
    )
    return {
        "route":decision.route,
        "ans_context":""
    }

#node2
def retrieve_policy(state:OrderDetails):
    question = latest_question(state)
    documents = retriver.invoke(question)
    policy_context = (format_docs(documents) or "No valid answer found")
    return {
        "ans_context":policy_context
    }

#node3ORDER_TOOL_PROMPT
def retrieve_llm_response(state:OrderDetails):
    system = SystemMessage(content=HANDBOOK_ANS_PROMPT.format(context=state["ans_context"],question=latest_question(state)))
    messages = [system] + state["messages"]
    responses =llm.invoke(messages)
    return {
        "messages":[responses]
    }

#node4
def order_agent(state:OrderDetails):
    system = SystemMessage(content=ORDER_TOOL_PROMPT)
    messages = [system] + state["messages"]
    responses = llm_with_tools.invoke(messages)
    return {
        "messages" :[responses]
    }

#node5
def order_not_found(state: OrderDetails):
    return {
        "messages": [
            AIMessage(
                content="Sorry, I couldn't find that order. "
                        "Please check your order ID and try again."
            )
        ]
    }
#node6

def capture_order_info(state: OrderDetails):
    for message in reversed(state["messages"]):
        if isinstance(message, ToolMessage):
            result = json.loads(message.content)

            if result.get("order_found", False):
                return {
                    "order_info": result
                }

    return {"order_info": {}}
#node 7

def combined_response(state: OrderDetails):
    system = SystemMessage(
        content=(
            "You are an e-commerce customer support assistant.\n"
            "Use the order details and policy context provided below.\n"
            "Do not invent order information or policy rules.\n"
            "If the order status makes the requested action ineligible, "
            "explain that clearly.\n\n"
            f"Order details: {state['order_info']}\n\n"
            f"Policy context: {state['ans_context']}\n"
        )
    )

    messages = [system] + state["messages"]
    response = llm.invoke(messages)

    return {"messages": [response]}