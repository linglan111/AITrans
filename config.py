# Redis配置
REDIS_URL = 'redis://localhost:6379/0'

# 模型配置（实际项目中可能需要API密钥等）
MODEL_CONFIG = {
    'translation': {
        'model': 'gpt-3.5-turbo',
        'temperature': 0.3,
        'max_tokens': 500
    },
    'summarization': {
        'model': 'gpt-3.5-turbo',
        'temperature': 0.3,
        'max_tokens': 300
    }
}

# 应用配置
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000
