import streamlit as st
from src.utils import execute_plt_code


# Initial chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])
        if message['fig']:
            st.pyplot(message['fig'])
            st.write("Execute code:")
            st.code(message['action'])


# Receive user input
if prompt := st.chat_input("Type here..."):
    # Display user input
    with st.chat_message("user"):
        st.write(prompt)
        

    # Add user input to chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "fig": None, "action": None})

    fig = None
    action = None

    if "data_agent" in st.session_state:
        response = st.session_state.data_agent(prompt)
        content = response['output']
        if response['intermediate_steps']:
            action = response['intermediate_steps'][-1][0].tool_input['query']
            if "plt" in action:
                fig = execute_plt_code(action, st.session_state.df)
    else:
        response = st.session_state.llm(prompt)
        content = response.content

    # Display response
    with st.chat_message("ai"):
        st.write(content)

        if fig:
            st.pyplot(fig)
            st.write("Execute code:")
            st.code(action)

            
    # Add response to chat history
    st.session_state.messages.append({"role": "ai", "content": content, "fig": fig, "action": action})
