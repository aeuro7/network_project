from datetime import datetime

def protocol_handler(protocol_message):
    """Handle protocol message based on its response code."""
    # protocol_message is already a string, no need to decode
    decoded_message = protocol_message.strip()  # Remove any leading/trailing whitespace including '\n'
    
    # Extract the response code and additional info using '_' as the delimiter
    parts = decoded_message.split('_', 1)  # Limit split to 1 to get at most 2 parts
    response_code = parts[0]
    additional_info = parts[1] if len(parts) > 1 else ""

    # Get current time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Handle different response codes
    if response_code == "200":
        print(f"[{current_time}]Server response:  200 OK Login successful: \n{additional_info}")
    elif response_code == "204":
        print(f"[{current_time}]Server response:  204 OK You selected: \n{additional_info}")
    elif response_code == "201":
        print(f"[{current_time}]Server response:  201 OK Position updated: \n{additional_info}")
    elif response_code == "401":
        print(f"[{current_time}]Server response:  401 ERROR Position already taken: \n{additional_info}")
    elif response_code == "402":
        print(f"[{current_time}]Server response:  402 ERROR Position out of bounds: \n{additional_info}")
    elif response_code == "403":
        print(f"[{current_time}]Server response:  403 ERROR Invalid command format: \n{additional_info}")
    elif response_code == "404":
        print(f"[{current_time}]Server response:  404 Forbidden Login failed: \n{additional_info}")
    elif response_code == "405":
        print(f"[{current_time}]Server response:  405 ERROR Invalid selection: \n{additional_info}")
    elif response_code == "406":
        print(f"[{current_time}]Server response:  406 ERROR Invalid input: \n{additional_info}")
    elif response_code == "202":
        print(f"[{current_time}]Server response:  202 OK Connection closed: \n{additional_info}")
    elif response_code == "203":
        print(f"[{current_time}]Server response:  203 OK Server shutting down: \n{additional_info}")
    elif response_code == "400":
        print(f"[{current_time}]Server response:  400 ERROR Invalid command: \n{additional_info}")
    elif response_code == "205":
        print(f"[{current_time}]Server response:  205 OK Changing movie selection... \n{additional_info}")
    else:
        print(f"[{current_time}]Server response:  Unknown response code: {response_code}")

# Example usage:
# protocol_message = "200_EURO"
# protocol_handler(protocol_message)
