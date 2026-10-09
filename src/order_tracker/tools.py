from langchain_core.tools import tool


@tool
def get_delivery_timings():
    """ Return the order  delivery timings """
    return "Monday-Saturday 10AM to 8PM"

@tool
def get_order_details(orderId:str):
    """Retturn the order details for the given order"""
    orders = {
    "ORD1245": {"status": "SHIPPED", "price": 120},
    "ORD1246": {"status": "DELIVERED", "price": 321}
}
    details = orders.get(orderId)
    if details is not None:
        return {
            "status":details["status"],
            "order_id":orderId,
            "order_found":True
        }
    else:
         return {
                   
                    "order_id":orderId,
                    "order_found":False
                }

ORDER_TOOL =[
    get_delivery_timings,
    get_order_details
]