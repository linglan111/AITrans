from celery import Celery
import time
from src.trans import translate_zh_to_en, translate_en_to_zh, summarize_text
from config import REDIS_URL

# 初始化Celery
celery = Celery(
    'ai_tasks',
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery.task(name='translate_zh_to_en')
def translate_zh_to_en_task(text):
    """异步中译英任务"""
    # 模拟处理时间
    time.sleep(2)
    return translate_zh_to_en(text)

@celery.task(name='translate_en_to_zh')
def translate_en_to_zh_task(text):
    """异步英译中任务"""
    # 模拟处理时间
    time.sleep(2)
    return translate_en_to_zh(text)

@celery.task(name='summarize')
def summarize_task(text):
    """异步文本总结任务"""
    # 模拟处理时间
    time.sleep(3)
    return summarize_text(text)
