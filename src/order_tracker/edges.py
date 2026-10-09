import json
from langchain_core.messages import AIMessage, ToolMessage
from .state import OrderDetails


def route_question(state:OrderDetails) -> str:
    """Branch 1: send the question down the right path."""
    return state["route"]

# def tool_validation(state:OrderDetails) -> str:
#     for message in reversed(state["messages"]):
#         print(message)
#         if isinstance(message,AIMessage):
#             break
#         if isinstance(message,ToolMessage):
#             result = json.loads(message.content)
#             if result["order_found"]:
#                 return "order_agent"
#             # Order exists: choose the next node based on the route 
#             if state["route"] == "order_policy": return "capture_order_info"
    
#             return "order_not_found"

def tool_validation(state: OrderDetails) -> str:
    for message in reversed(state["messages"]):
        if isinstance(message, ToolMessage):
            result = json.loads(message.content)

            if not result.get("order_found", False):
                return "order_not_found"

            # Order exists: check which route was selected
            if state["route"] == "order_policy":
                return "capture_order_info"

            return "order_agent"

    return "order_not_found"
def after_policy_retrieval(state: OrderDetails) -> str:
    if state["route"] == "order_policy":
        return "combined_response"
    return "retrieve_llm_response"