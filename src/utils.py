import time
import random


def simulate_ai_call(text, task_type):
    """
    模拟AI大语言模型调用

    参数:
    - text (str): 输入文本
    - task_type (str): 任务类型 ('zh_to_en', 'en_to_zh', 'summarize')

    返回:
    - str: 处理结果
    """
    # 模拟API调用延迟
    time.sleep(0.5)

    if task_type == 'zh_to_en':
        if '你好' in text:
            return 'Hello'
        elif '早上好' in text:
            return 'Good morning'
        elif '我是' in text:
            return f"I am {text.split('我是')[1].strip()}"
        elif '中国' in text:
            return text.replace('中国', 'China')
        else:
            return f"[Translated to English]: {text}"

    elif task_type == 'en_to_zh':
        if 'hello' in text.lower():
            return '你好'
        elif 'good morning' in text.lower():
            return '早上好'
        elif 'i am' in text.lower():
            return f"我是{text.split('I am')[1].strip() if 'I am' in text else text.split('i am')[1].strip()}"
        elif 'china' in text.lower():
            return text.lower().replace('china', '中国')
        else:
            return f"[翻译成中文]: {text}"

    elif task_type == 'summarize':
        words = text.split()
        if len(words) > 20:
            # 简单摘取前20个单词作为摘要
            return ' '.join(words[:20]) + "..."
        else:
            return f"[Summary]: {text}"


def translate_zh_to_en(text):
    """中文翻译为英文"""
    return simulate_ai_call(text, 'zh_to_en')


def translate_en_to_zh(text):
    """英文翻译为中文"""
    return simulate_ai_call(text, 'en_to_zh')


def summarize_text(text):
    """生成文本摘要"""
    return simulate_ai_call(text, 'summarize')


def stream_translate_zh_to_en(text):
    """流式中译英"""
    result = simulate_ai_call(text, 'zh_to_en')
    words = result.split()
    current = ""

    for word in words:
        current += word + " "
        yield current.strip()


def stream_translate_en_to_zh(text):
    """流式英译中"""
    result = simulate_ai_call(text, 'en_to_zh')
    # 由于中文没有空格分隔，我们按字符返回
    current = ""

    for char in result:
        current += char
        yield current


def stream_summarize(text):
    """流式文本总结"""
    result = simulate_ai_call(text, 'summarize')
    words = result.split()
    current = ""

    for word in words:
        current += word + " "
        yield current.strip()
