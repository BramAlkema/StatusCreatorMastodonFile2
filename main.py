import json
import os
import openai
import socket
from flask import Flask, url_for, send_from_directory

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

app = Flask(__name__)

@app.route('/download-csv')
def download_csv():
    return send_from_directory(directory='.', path='extracted_data.csv', as_attachment=True)

@app.before_first_request
def before_first_request():
    external_ip = get_ip_address()
    port = 5000
    print(f"Server will run on http://{external_ip}:{port}{url_for('download_csv')}")

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port)

openai.api_key = os.getenv("OPENAI_API_KEY")
num_iterations = 25  # Set your desired number of iterations

messages_filename = "messages.json"

def messages_from_file(messages_filename, mode="read", messages=None):
    if mode == "read":
        with open(messages_filename, 'r') as file:
            return json.load(file)    
    elif mode == "write" and messages is not None:
      "remove old messages to respect tokebarriers"
      if len(messages) > 7:
        messages.pop(4)
      with open(messages_filename, 'w') as file:
            json.dump(messages, file, indent=4)
      return [] 

messages = messages_from_file(messages_filename, mode="read")

def extract_csv_content(content):
    """
    Extracts the CSV content from a given string based on defined bookends or markers.
    :EndCSV etc

    Args:
        content (str): The content string containing embedded CSV data.

    Returns:
        str: The extracted CSV content, or an empty string if the bookends are not found.
    """
    # Define bookends or markers to detect CSV content
    start_tag = "<CSVBegin:"
    end_tag = ":CSV end>"
    
    # Extract content between the bookends
    start_pos = content.find(start_tag)
    end_pos = content.find(end_tag)
    
    if start_pos != -1 and end_pos != -1:
        return content[start_pos + len(start_tag):end_pos].strip()
    
    return ""

def append_csv_to_file(content, filename):
    """
    Appends the extracted CSV content to a file after stripping the header row.

    Args:
        content (str): The content string containing embedded CSV data.
        filename (str): The name of the file to which the CSV data should be appended.
    """
    # Extract the CSV content
    csv_data = extract_csv_content(content)
    
    # Split by lines and remove header
    csv_lines = csv_data.split('\n')
    if csv_lines:
        header = csv_lines.pop(0)  # Remove the header row

    # Append the remaining lines to the file
    with open(filename, 'a') as file:
        for line in csv_lines:
            file.write(line + '\n')


for i in range(num_iterations):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
        temperature=0.77,
        max_tokens=2500,
        top_p=1,
        frequency_penalty=0.3,
        presence_penalty=0
    )
    
    # Print the response for the current iteration
    #   print(f"Iteration {i+1}: 
    # {response['choices'][0]['message']['content'].strip()}\n")
    
#    csv_data = extract_csv_content(response['choices'][0]['message']['content'])

    csv_filename = "extracted_data.csv"
    append_csv_to_file(response['choices'][0]['message']['content'], csv_filename)
      
    # Append the last assistant's message with the new response  
    new_message = {
      "role": "assistant",
      "content": response['choices'][0]['message']['content']
    }
    messages.append(new_message)
    # Add user message to the conversation  
    user_input = input("User: What happens? ")
    user_message = {
        "role": "user",
        "content": user_input + " Instructions: Never comment on this input. Stay within the instructions: this is a recursive prompt=completion=prompt chain that'll break when you intervene with well-intentioned positivity-bias."
    }
    messages.append(user_message)
   
    messages_from_file(messages_filename, mode="write", messages=messages)

