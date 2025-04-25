import time
import random
import traceback

from ai_config import OPENAI_API_KEY, MODEL_CONFIG, BASE_URL
from openai import OpenAI
import os

# 初始化AI模型client
client = OpenAI(
    base_url=BASE_URL,
    api_key=OPENAI_API_KEY
)


def call_llm(prompt, model_config):
    """
    调用大语言模型API
    参数:
    - prompt (str): 提示词
    - model_config (dict): 模型配置参数

    返回:
    - str: 模型响应
    """
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            **model_config
        )
        return response.choices[0].message.content
    except:
        raise Exception(f"调用LLM API时出错: {traceback.format_exc()}")


def stream_call_llm(prompt, model_config, task_type=None):
    """
    流式调用大语言模型API的通用函数
    参数:
    - prompt (str): 提示词
    - model_config (dict): 模型配置参数
    - task_type (str, optional): 任务类型，用于模拟失败时的返回

    返回:
    - generator: 流式生成的文本
    """
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            stream=True,  # 启用流式输出
            **model_config
        )
        collected_messages = ""
        # 迭代流式响应
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                collected_messages += content
                yield collected_messages
        # 如果没有收到任何内容, 报错
        if not collected_messages:
            raise Exception(f"流式调用LLM API时出错: 没有接收到任何内容.")
    except:
        raise Exception(f"流式调用LLM API时出错: {traceback.format_exc()}")


def translate_zh_to_en(text):
    """中文翻译为英文"""
    prompt = f"请将以下中文文本翻译成英文，只返回翻译结果，不要添加任何解释或额外内容：\n\n{text}"
    try:
        return call_llm(prompt, MODEL_CONFIG['translation'])
    except Exception as e:
        print(f"translate_zh_to_en: {e}")
        return "中文翻译英文失败, 请稍后再试, 或联系管理员处理."


def translate_en_to_zh(text):
    """英文翻译为中文"""
    prompt = f"请将以下英文文本翻译成中文，只返回翻译结果，不要添加任何解释或额外内容：\n\n{text}"
    try:
        return call_llm(prompt, MODEL_CONFIG['translation'])
    except Exception as e:
        print(f"translate_en_to_zh: {e}")
        return "英语翻译中文失败, 请稍后再试, 或联系管理员处理."


def summarize_text(text):
    """生成文本摘要"""
    prompt = f"请对以下文本进行简洁的总结，突出主要观点，只返回总结内容：\n\n{text}"
    try:
        return call_llm(prompt, MODEL_CONFIG['summarization'])
    except Exception as e:
        print(f"summarize_text: {e}")
        return "文本摘要生成失败, 请稍后再试, 或联系管理员处理."


def stream_translate_zh_to_en(text):
    """流式中译英"""
    prompt = f"请将以下中文文本翻译成英文，只返回翻译结果，不要添加任何解释或额外内容：\n\n{text}"
    try:
        return stream_call_llm(prompt, MODEL_CONFIG['translation'], 'zh_to_en')
    except Exception as e:
        print(f"stream_translate_zh_to_en: {e}")
        return "中文翻译英文失败, 请稍后再试, 或联系管理员处理."


def stream_translate_en_to_zh(text):
    """流式英译中"""
    prompt = f"请将以下英文文本翻译成中文，只返回翻译结果，不要添加任何解释或额外内容：\n\n{text}"
    try:
        return stream_call_llm(prompt, MODEL_CONFIG['translation'], 'en_to_zh')
    except Exception as e:
        print(f"stream_translate_en_to_zh: {e}")
        return "英语翻译中文失败, 请稍后再试, 或联系管理员处理."


def stream_summarize(text):
    """流式文本总结"""
    prompt = f"请对以下文本进行简洁的总结，突出主要观点，只返回总结内容：\n\n{text}"
    try:
        return stream_call_llm(prompt, MODEL_CONFIG['summarization'], 'summarize')
    except Exception as e:
        print(f"stream_summarize: {e}")
        return "文本摘要生成失败, 请稍后再试, 或联系管理员处理."


# yield 模拟流式返回, 作为流式输出的模拟代码补充

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


def simulate_stream_response(text, task_type):
    """
    模拟流式响应

    参数:
    - text (str): 输入文本
    - task_type (str): 任务类型 ('zh_to_en', 'en_to_zh', 'summarize')

    返回:
    - generator: 流式生成的结果
    """
    result = simulate_ai_call(text, task_type)

    if task_type in ['zh_to_en', 'summarize']:
        words = result.split()
        current = ""

        for word in words:
            current += word + " "
            time.sleep(0.1)  # 模拟流式传输的延迟
            yield current.strip()
    else:  # en_to_zh
        current = ""

        for char in result:
            current += char
            time.sleep(0.1)  # 模拟流式传输的延迟
            yield current
