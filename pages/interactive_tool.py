import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer


def main():
    # Set up interface
    st.set_page_config(page_title="PygWalker", page_icon="🚶", layout='wide')
    
    # Render pygwalker
    if st.session_state.get("df") is not None:
        pyg_app = StreamlitRenderer(st.session_state.df)
        pyg_app.explorer()
    else:
        st.info("Please upload a CSV file to get started.")
    


if __name__ == "__main__":
    main()