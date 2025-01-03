import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

from loguru import logger
from src import config
from src.models.llms import load_llm
from src.utils import execute_plt_code

def process_query(data_agent, query):
    response = data_agent(query)
    action = response['intermediate_steps'][-1][0].tool_input['query']

    if "plt" in action:
        st.write(response['output'])
        fig = execute_plt_code(action, st.session_state.df)
        if fig:
            st.pyplot(fig)

        st.write("Execute code:")
        st.code(action)

        res_str = f"""{response['output']}
        Excute code:
        ```python\n{action}\n```
        """
        st.session_state.history.append((query, res_str))
    else:
        st.write(response['output'])
        st.session_state.history.append((query, response['output']))
        

def display_chat_history():
    st.markdown("## Chat History")

    for query, response in st.session_state.history:
        st.markdown(f"### Query: {query}")
        st.write(f"Response: {response}")


    
# Load LLMs
llm = load_llm(model_name=config.MODEL_NAME, 
                temperature=config.TEMPERATURE, 
                max_tokens=config.MAX_TOKENS)
logger.info(f"Successfully loaded {config.MODEL_NAME}")

# Upload data
with st.sidebar:
    st.title("Upload Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Initial chat history
if "history" not in st.session_state:
    st.session_state["history"] = []

# Read csv file
if uploaded_file is not None:
    st.session_state.df = pd.read_csv(uploaded_file)
    st.write("Data uploaded successfully!", st.session_state.df.head())

    # Create data analysis agent
    data_agent = create_pandas_dataframe_agent(
        llm=llm,
        df = st.session_state.df,
        agent_type="tool-calling",
        allow_dangerous_code=True,
        verbose=True,
        return_intermediate_steps=True
    )

    logger.info("Successfully created data analysis agent")

    # Input and process query
    query = st.text_input("Enter your question: ")


    if st.button("Submit"):
        with st.spinner("Processing..."):
            process_query(data_agent, query)

# Display chat history  
st.divider()
display_chat_history()

