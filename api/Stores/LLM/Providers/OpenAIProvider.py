from ..LLMFactory import LLMFactory
from openai import OpenAI
from ..LLMEnum import LLMEnum, OPENAIEnum
class OpenAIProvider(LLMFactory):
    def __init__(self, api_key: str, api_url: str = None, 
                 max_input_tokens: int = 2000, max_output_tokens: int = 2000, temperature: float = 0.2):
        self.api_key = api_key
        self.api_url = api_url
        self.max_input_tokens = max_input_tokens
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature

        self.model_name = None

        self.embedding_model_name = None
        self.embedding_model_output_dim = None

        self.client = OpenAI(api_key=self.api_key)
    def set_generation_LLM(self, llm_name: str):
        self.model_name = llm_name
    def set_embedding_LLM(self, embedding_model_name: str, embedding_model_output_dim: int = None):
        self.embedding_model_name = embedding_model_name
        self.embedding_model_output_dim = embedding_model_output_dim
    def process_text(self, text: str) -> str:
        return text.strip()[:self.max_input_tokens]
    def generate_response(self, prompt: str, chat_history: list = None, max_tokens: int = None, temperature: float = None) -> str:
        if not self.model_name:
            raise ValueError("Generation LLM model name is not set.")
        if not prompt:
            raise ValueError("Prompt cannot be empty.")
        if not self.client:
            raise ValueError("OpenAI client is not initialized.")
        max_tokens = max_tokens or self.max_output_tokens
        temperature = temperature if temperature is not None else self.temperature

        chat_history.append(self.construct_prompt(prompt, OPENAIEnum.USER.value))

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=chat_history,
            max_tokens=max_tokens,
            temperature=temperature
        )
        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message.content:
            raise ValueError("Invalid response from OpenAI API.")
        return response.choices[0].message.content.strip()
    def generate_embedding(self, text: str) -> list:
        if not self.embedding_model_name:
            raise ValueError("Embedding LLM model name is not set.")
        if not text:
            raise ValueError("Input text cannot be empty.")
        if not self.client:
            raise ValueError("OpenAI client is not initialized.")

        response = self.client.embeddings.create(
            model=self.embedding_model_name,
            input=text
        )
        return response.data[0].embedding
    
    def construct_prompt(self, prompt: str, role: str) -> dict:
        if role not in ["system", "user", "assistant"]:
            raise ValueError("Role must be one of 'system', 'user', or 'assistant'.")
        return {"role": role, "content": self.process_text(prompt)}
