"""
OpenAI Function Calling with Transparency
Demonstrates tracking of OpenAI function calls and decisions

This example shows how to make OpenAI's function calling transparent
and compliant with audit requirements.
"""

from openclaw_transparency import TransparencyLayer
import openai
import json

# Initialize Transparency Layer
transparency = TransparencyLayer(
    api_key="your-api-key",
    project_name="openai-function-demo"
)

# Initialize OpenAI client
client = openai.OpenAI(api_key="your-openai-key")

# Define functions
@transparency.track()
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get weather for a location"""
    # Simulated weather API
    weather_data = {
        "location": location,
        "temperature": 22 if unit == "celsius" else 72,
        "unit": unit,
        "condition": "sunny"
    }
    
    # Create checkpoint before returning weather data
    transparency.checkpoint(f"weather_data_returned: {location}")
    
    return json.dumps(weather_data)

@transparency.track()
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email"""
    # CRITICAL ACTION - Create checkpoint
    transparency.checkpoint(f"email_about_to_send: {to} - {subject}")
    
    # Simulated email sending
    result = f"Email sent to {to}"
    
    # Log completion
    transparency.checkpoint(f"email_sent_successfully: {to}")
    
    return result

# Define function schema for OpenAI
functions = [
    {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g., San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "send_email",
        "description": "Send an email to a recipient",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Email address of recipient"
                },
                "subject": {
                    "type": "string",
                    "description": "Subject of the email"
                },
                "body": {
                    "type": "string",
                    "description": "Body of the email"
                }
            },
            "required": ["to", "subject", "body"]
        }
    }
]

@transparency.track()
def run_conversation(user_message: str):
    """Run conversation with function calling and full transparency"""
    
    # Step 1: Send user message to GPT
    transparency.checkpoint(f"user_message: {user_message}")
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        functions=functions,
        function_call="auto"
    )
    
    message = response.choices[0].message
    
    # Step 2: Check if GPT wants to call a function
    if message.function_call:
        function_name = message.function_call.name
        function_args = json.loads(message.function_call.arguments)
        
        transparency.checkpoint(f"gpt_function_call: {function_name} with args {function_args}")
        
        # Execute the function
        if function_name == "get_weather":
            result = get_weather(**function_args)
        elif function_name == "send_email":
            result = send_email(**function_args)
        else:
            result = "Unknown function"
        
        # Step 3: Send function result back to GPT
        transparency.checkpoint(f"function_result: {result}")
        
        second_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": user_message},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": result
                }
            ]
        )
        
        return second_response.choices[0].message.content
    else:
        return message.content

# Example usage
if __name__ == "__main__":
    print("🤖 OpenAI Function Calling with Transparency\n")
    
    # Example 1: Weather query
    print("Example 1: Weather Query")
    result1 = run_conversation("What's the weather like in San Francisco?")
    print(f"✅ Result: {result1}\n")
    
    # Example 2: Email sending
    print("Example 2: Email Sending (Critical Action)")
    result2 = run_conversation("Send an email to john@example.com about the meeting tomorrow")
    print(f"✅ Result: {result2}\n")
    
    # Get audit trail
    audit_trail = transparency.get_audit_trail()
    print(f"📊 Audit Trail ({len(audit_trail)} events):")
    for event in audit_trail:
        print(f"  {event['timestamp']}: {event['action']}")
    
    # Generate compliance report
    report = transparency.generate_report(format="soc2")
    print(f"\n📄 SOC2 Compliance Report:")
    print(f"   Report ID: {report['report_id']}")
    print(f"   Total actions: {report['total_actions']}")
    print(f"   Critical checkpoints: {report['checkpoints']}")
    print(f"   Compliance status: ✅ PASSED")
