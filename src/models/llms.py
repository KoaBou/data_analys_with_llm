from langchain_openai import ChatOpenAI

def load_llm(model_name: str = 'gpt-3.5-turbo', temperature: float = 0.0, max_tokens: int = 1000):
    """
    Load a language model.

    Args:
        model_name (str): The name of the language model to load.
        temperature (float): The temperature to use for sampling.
        max_tokens (int): The maximum number of tokens to generate.

    Returns:
        ChatOpenAI: The language model instance.
    """
    
    if model_name == "gpt-3.5-turbo":
        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
    elif model_name == "gpt-4":
        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
    else:
        raise ValueError(f"Model {model_name} not found.\
                         Please choose from ['gpt-3.5-turbo', 'gpt-4',...]")