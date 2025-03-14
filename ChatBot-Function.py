# Necessary Packages
import os
from openai import OpenAI

# Define the client
client = OpenAI(api_key=os.environ["OPENAI"])

def chatbot():  # Function name
    
    # The system prompt to be passed to the client later.
    # This will provide context for the LLM to operate.
    sys_prompt = """You are a knowledgeable travel guide expert specialized in Paris landmarks.
                    Provide concise and accurate responses to questions about Paris.
                    Keep answers under 100 tokens."""

    # The message role and content to be passed to the client chat completion class.
    conv_list = [{"role": "system",
                  "content": sys_prompt}]

    # The question set that the user will choose form.
    questions = ["How far away is the Louvre from the Eiffel Tower (in miles) if you are driving?",
                 "Where is the Arc de Triomphe?",
                 "What are the must-see artworks at the Louvre Museum?"]

    # The list of current GPT models in OpenAPI Platform.
    openai_models = ["gpt-4", "gpt-4-0314", "gpt-4-32k", "gpt-4-32k-0314", "gpt-3.5-turbo", "gpt-3.5-turbo-0301",
                     "text-davinci-003", "text-davinci-002", "text-curie-001", "text-babbage-001",
                     "text-ada-001", "code-davinci-002", "code-cushman-001"]

    # User input function to put the number associated with the desired model.
    user_model = input("""\nPlease choose a model no. from the list
                          1.gpt-4
                          2.gpt-4-0314
                          3.gpt-4-32k
                          4.gpt-4-32k-0314
                          5.gpt-3.5-turbo
                          6.gpt-3.5-turbo-0301
                          7.text-davinci-003
                          8.text-davinci-002
                          9.text-curie-001
                          10.text-babbage-001
                          11.text-ada-001
                          12.code-davinci-002
                          13.code-cushman-001": """)

    # Error handling for the user's input on model selection.
    while True: # Checks that the user only provides numerical input
        try:
            n = int(user_model)
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            break

    if n not in range(1, 14): # Checks that the numberical input is within acceptable range
        print(f"{n} is not within the set question numbers!")

    # Gives the user the selected model
    print(f"\nThe chosen model is {openai_models[int(user_model)-1]}")

    # The function that returns the reponse of the chosen LLM with regard to the messages that it receives
    def get_response(user_model,messages):
        response = client.chat.completions.create(
            model = openai_models[int(user_model)-1],
            messages = messages,
            temperature = 0.0,
            max = 100
        )
        return response.choices[0].message.content

    # User input for selecting the deisired question.
    user_prompt = input("""\nPlease choose a question no. from the list
                             1.How far away is the Louvre from the Eiffel Tower (in miles) if you are driving?
                             2.Where is the Arc de Triomphe?
                             3.What are the must-see artworks at the Louvre Museum?: """)
    
    #Error handling for user input on question selection task
    while True:
        try:
            n = int(user_prompt)
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            break

    # Updating the conversation list based on the question chosen to be passed to the chosen LLM
    conv_list.append({"role": "user",
                                  "content": questions[0]})

    # Conditional clause to ensure the order of the questions and answers are followed for a multi-turn chat completion.
    if n not in range(1, 4):
        print(f"{n} is not within the set question numbers!")
    elif n == 1:
        print(f"Question: {questions[0]}", "\n", f"Answer: {get_response(user_model, conv_list)}")  
    else:
        m = range(1, n+1)
        for m in range(1, n+1):
            while m <= n:
                conv_list.append({"role": "assistant",
                                              "content": get_response(user_model, conv_list)},
                                             {"role": "user",
                                              "content": questions[m-1]})

                print(f"Question: {questions[m-1]}", "\n", f"Answer: {get_response(user_model, conv_list)}")