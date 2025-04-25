OPENAI_API_KEY = "your_openai_api_key"
# 模型配置
MODEL_CONFIG = {
    'translation': {
        'model': 'openai/gpt-4.1-nano',
        'temperature': 0.3,
        'max_tokens': 500
    },
    'summarization': {
        'model': 'openai/gpt-4.1-nano',
        'temperature': 0.3,
        'max_tokens': 300
    }
}