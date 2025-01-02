import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def execute_plt_code(code: str, df: pd.DataFrame,):
    """
    Execute code that contains a matplotlib plot and save the figure to a file.

    Args:
        code (str): The code to execute.
        df (pd.DataFrame): The dataframe to use in the code.
        output_file (str): The file path to save the figure.
    
    Returns:
        plt.Figure: The figure that was created.
    """
    
    try:
        local_vars = {"plt": plt, "df": df}
        print("Executing code:", code)
        compiled_code = compile(code, "<string>", "exec")
        exec(compiled_code, globals(), local_vars)

        return plt.gcf()
    except Exception as e:
        st.error(f"Error when executing code: {e}")
        return None
    