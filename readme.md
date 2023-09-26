# Recursive Generation with OpenAI

NB Requires "OPEN_AI_KEY" secret set

This project demonstrates how to perform recursive generation with OpenAI's models while managing message stacks to remain within token limits.

## Process:

1. **Initialization**: We start with an initial set of messages. This could be a prompt or any other starting point for our recursive generation.

2. **OpenAI Call**: We send the set of messages to OpenAI's API. The assistant returns a continuation or response based on the provided messages.

3. **Append and Pop Messages**: 
   - We append the assistant's response to our set of messages.
   - To manage token limits, we remove the oldest assistant message (at index 2) from our message stack.

4. **Recursive Loop**: We iterate steps 2 and 3 for a set number of times or until a certain condition is met. This results in a series of recursive generations where each new response is influenced by the previous ones.

5. **Saving Data**:
   - After each iteration, we extract the CSV content from the assistant's response using the `extract_csv_content` function. This content is then appended to `extracted_data.csv`.
   - The updated message stack is saved to `messages.json` to maintain state between iterations.

6. **Restarting and Continuing**: If you wish to restart the recursive generation or continue from where you left off, load the latest set of messages from `messages.json` and continue from step 2.

## Files:

- `extracted_data.csv`: Contains the CSV data extracted from the assistant's responses across iterations.
- `messages.json`: Stores the message stack after each iteration. Use this to continue recursive generation after a break or to review the messages used in previous iterations.
---