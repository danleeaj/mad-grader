from enum import Enum

class Model(Enum):
    """
    Represents the available LLM options for the debate system.
    """
    GPT = "gpt-3.5-turbo-0125"
    GEMINI = "gemini-pro"
    CLAUDE = "claude-3-haiku-20240307"