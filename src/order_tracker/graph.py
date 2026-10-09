from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import tools_condition

from .nodes import order_agent,tools,order_router,retrieve_policy,retrieve_llm_response,order_not_found, capture_order_info,combined_response
from .state import OrderDetails
from .edges import route_question,tool_validation,after_policy_retrieval




graph = StateGraph(OrderDetails)
graph.add_node("order_router",order_router)
graph.add_node("tools",tools)
graph.add_node("retrieve_policy",retrieve_policy)
graph.add_node("retrieve_llm_response",retrieve_llm_response)
graph.add_node("order_agent",order_agent)
graph.add_node("order_not_found",order_not_found)
graph.add_node("capture_order_info",capture_order_info)
graph.add_node("combined_response",combined_response)
graph.add_edge(START,"order_router")
graph.add_conditional_edges(
    "retrieve_policy",
    after_policy_retrieval,
    {
        "combined_response": "combined_response",
        "retrieve_llm_response": "retrieve_llm_response",
    },
)
graph.add_conditional_edges("order_router",route_question,{"order_tool":"order_agent","doc_answer":"retrieve_policy","order_policy":"order_agent"})

graph.add_conditional_edges("order_agent",tools_condition,{"tools":"tools","__end__":END})
graph.add_conditional_edges("tools",tool_validation,
                            {
                                "order_agent":"order_agent",
                                "order_not_found":"order_not_found",
                                 "capture_order_info": "capture_order_info"})
graph.add_edge("capture_order_info", "retrieve_policy")
graph.add_edge("order_not_found",END)
graph.add_edge("retrieve_llm_response",END)
graph.add_edge("combined_response", END)
app = graph.compile()