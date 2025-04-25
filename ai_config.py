BASE_URL = "https://openrouter.ai/api/v1"
OPENAI_API_KEY = "your_openai_api_key_here"
# 模型配置
MODEL_CONFIG = {
    'translation': {
        'model': 'openai/gpt-4.1-nano',
        'temperature': 0.3,
        'max_tokens': 2000
    },
    'summarization': {
        'model': 'openai/gpt-4.1-nano',
        'temperature': 0.3,
        'max_tokens': 1000
    }
}