from abc import ABC, abstractmethod
class LLMFactory(ABC):
    @abstractmethod
    def set_generation_LLM(self, llm_name: str):
        pass
    @abstractmethod
    def set_embedding_LLM(self, llm_name: str):
        pass
    @abstractmethod
    def generate_response(self, prompt: str,chat_history: list, max_tokens: int, temperature: float = None) -> str:
        pass
    @abstractmethod
    def generate_embedding(self, text: str) -> list:
        pass
    @abstractmethod
    def construct_prompt(self, prompt: str, role: str) -> str:
        pass