from src.order_tracker.graph import app


result = app.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Can i cancel my order ORD1245?"
        }
    ]
})

print(result["messages"][-1].content)