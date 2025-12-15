import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_order(message_text):
    """
    Parse order message into structured JSON.
    """
    prompt = f"""
    Extract order information from the text: "{message_text}".
    Return as JSON with fields:
    product_name, quantity, unit, destination, delivery_time
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    try:
        content = response.choices[0].message.content
        data = json.loads(content)
        return data
    except Exception:
        return {
            "product_name": "Unknown",
            "quantity": 0,
            "unit": "kg",
            "destination": "Unknown",
            "delivery_time": "Unknown"
        }

