import streamlit as st
from predibase import Predibase, FinetuningConfig, DeploymentConfig

# Initialize Predibase API client
# Streamlit app UI
st.title("AI Teacher Assistant")

api_key_options = {
    "pb_Fb-7N9dsU-uWpNtTjBgOBw": {
        "deployment_ids": ["solar-1-mini-chat-240612"],
        "adapter_ids": ["test/1", "test/2", "test/3", "test/4", "test/5"]
    },
    "pb_dfwn9qdxXDu2KiObFk9WAA": {
        "deployment_ids": ["aiku-solar-mini"],
        "adapter_ids": ["solar-ta-mini-beta/1", "solar-ta-mini-beta/3", "solar-ta-mini-beta/6"]
    }
}

selected_api_key = st.selectbox("Select API Key:", options=list(api_key_options.keys()))

deployment_options = api_key_options[selected_api_key]["deployment_ids"]
adapter_options = api_key_options[selected_api_key]["adapter_ids"]

# Dropdown fields for user customization
deployment_id = st.selectbox("Select deployment ID:", options=deployment_options)
adapter_id = st.selectbox("Select adapter ID:", options=adapter_options)

# Max new tokens input (now configurable)
max_new_tokens = st.slider("Select max new tokens:", 1, 4096, 100)
# Temperature input (now configurable)
temperature = st.slider("Select temperature:", 0.0, 1.0, 0.1)
# User input area for code or question
user_input = st.text_area("Enter your question:")

# Function to generate a response using Predibase
def generate_response(user_input, deployment_id, adapter_id, max_new_tokens, temperature, api_key):
    try:
        pb = Predibase(api_token=api_key)  # kairos
        # Create deployment client with the provided deployment_id
        lorax_client = pb.deployments.client(deployment_id)
        
        # Send user input to the Predibase model and get the generated response
        response = lorax_client.generate(user_input, adapter_id=adapter_id, max_new_tokens=max_new_tokens, temperature=temperature)
        print(response)
        return response.generated_text
    except Exception as e:
        return f"Error: {str(e)}"

# When the user submits input
if st.button('Ask'):
    if user_input:
        with st.spinner("Generating response..."):
            response = generate_response(user_input, deployment_id, adapter_id, max_new_tokens, temperature, selected_api_key)
        st.write("AI Response:")
        st.write(response)
    else:
        st.write("Please enter some text.")
