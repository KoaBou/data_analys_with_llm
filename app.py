import streamlit as st
from st_pages import get_nav_from_toml

import pandas as pd
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent


from loguru import logger
from src import config
from src.models.llms import load_llm
from src.utils import execute_plt_code

def main():
    # Set page config
    st.set_page_config(layout="wide")

    # Load LLMs
    st.session_state.llm = load_llm(model_name=config.MODEL_NAME, 
                                    temperature=config.TEMPERATURE, 
                                    max_tokens=config.MAX_TOKENS)
    logger.info(f"Successfully loaded {config.MODEL_NAME}")


    with st.sidebar:
        st.title("Upload Data")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        # st.write("Data uploaded successfully!", st.session_state.df.head())

        # Create data analysis agent
        st.session_state.data_agent = create_pandas_dataframe_agent(
            llm=st.session_state.llm,
            df = st.session_state.df,
            agent_type="tool-calling",
            allow_dangerous_code=True,
            verbose=True,
            return_intermediate_steps=True
        )

        logger.info("Successfully created data analysis agent")


    nav = get_nav_from_toml(".streamlit/pages.toml")
    pg = st.navigation(nav)
    pg.run()


if __name__ == "__main__":
    main()