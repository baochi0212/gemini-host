import streamlit as st
# from decouple import config
# import openai
import requests
response = False
prompt_tokens = 0
completion_tokes = 0
total_tokens_used = 0
cost_of_response = 0

# API_KEY = config('OPENAI_API_KEY')
# openai.api_key = API_KEY
API_KEY = "AIzaSyDo7DTaM8MCyuz-nYhmXtunjj6vK6US3MA"
# API_KEY = sys.argv[1]
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + API_KEY
url_token = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:countTokens?key=" + API_KEY


st.header("gemini cua tao")

st.markdown("""---""")

question_input = st.text_area("Prompt")
temp = st.slider(
    "Temperature", 0., 1., 0., 0.01)

print("Question input", question_input)
rerun_button = st.button("Regenerate")

st.markdown("""---""")
def make_response(text, temp):
    headers = {
        "Content-Type": "application/json"
    }
    token_data = {
      "contents": [{
        "parts":[{
          "text": text}]}]}
    num_tokens = requests.post(url_token, headers=headers, json=token_data).json()["totalTokens"]

    data = {
        "contents": [{
            "parts": [
                {"text": text}
            ]
        }],
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            }
        ],
        "generationConfig": {
            "stopSequences": [
                "Title"
            ],
            "temperature": temp,
            "maxOutputTokens": 4096,
            "topP": 0.9,
            "topK": 50
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response, num_tokens
if question_input:
    response, num_tokens = make_response(question_input, temp)
    st.write("Num tokens:")
    st.write(num_tokens)
else:
    pass

if rerun_button:
    response, _ = make_response(question_input, temp)
else:
    pass
print("???", response)
if response:
    st.write("Response:")

    st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])

    # prompt_tokens = response["usage"]["prompt_tokens"]
    # completion_tokes = response["usage"]["completion_tokens"]
    # total_tokens_used = response["usage"]["total_tokens"]

    # cost_of_response = total_tokens_used * 0.000002
else:
    pass


# with st.sidebar:
#     st.title("Usage Stats:")
#     st.markdown("""---""")
#     st.write("Promt tokens used :", prompt_tokens)
#     st.write("Completion tokens used :", completion_tokes)
#     st.write("Total tokens used :", total_tokens_used)
#     st.write("Total cost of request: ${:.8f}".format(cost_of_response))
