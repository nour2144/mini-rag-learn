from .LLMEnum import LLMEnum
from .Providers import OpenAIProvider
class LLMProvider:
    def __init__(self, config):
        self.config = config

    def create_provider(self, provider_name: str):
        if provider_name == LLMEnum.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.openai_api_key,
                api_url=self.config.openai_api_url,
                max_input_tokens=self.config.default_input_token_limit,
                max_output_tokens=self.config.default_max_tokens,
                temperature=self.config.default_temperature
            )
        else:
            raise ValueError(f"Unsupported LLM provider type: {provider_name}")