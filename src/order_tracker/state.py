from typing import Literal,TypedDict
from typing_extensions import Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

Route = Literal["order_tool","doc_answer","order_policy"]
class OrderDetails(TypedDict):
    messages:Annotated[list[AnyMessage],add_messages]
    route:Route
    order_info:dict
    order_id:str
    order_found:bool
    ans_context:str
    
