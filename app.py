from flask import Flask, request, jsonify, Response, render_template
from flask_cors import CORS
import json
import time
from celery.result import AsyncResult
from src.tasks import celery, translate_zh_to_en_task, translate_en_to_zh_task, summarize_task
from src.trans import (
    translate_zh_to_en, translate_en_to_zh, summarize_text,
    stream_translate_zh_to_en, stream_translate_en_to_zh, stream_summarize
)

app = Flask(__name__)
CORS(app)

# 任务结果存储 (模拟数据库)
task_results = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/functions', methods=['GET'])
def get_functions():
    """获取所有功能列表"""
    return jsonify({
        'success': True,
        'functions': [
            {'id': 'translate_zh_to_en', 'name': '中译英', 'description': '将中文翻译为英文'},
            {'id': 'translate_en_to_zh', 'name': '英译中', 'description': '将英文翻译为中文'},
            {'id': 'summarize', 'name': '文本总结', 'description': '生成文本摘要'},
        ]
    })


@app.route('/api/function/<function_id>', methods=['POST'])
def execute_function(function_id):
    """同步调用功能"""
    text = request.json.get('text', '')

    if not text:
        return jsonify({'success': False, 'message': 'Text is required'})

    if function_id == 'translate_zh_to_en':
        result = translate_zh_to_en(text)
    elif function_id == 'translate_en_to_zh':
        result = translate_en_to_zh(text)
    elif function_id == 'summarize':
        result = summarize_text(text)
    else:
        return jsonify({'success': False, 'message': 'Function not found'})

    return jsonify({'success': True, 'result': result})


@app.route('/api/async/<function_id>', methods=['POST'])
def async_execute_function(function_id):
    """异步调用功能"""
    text = request.json.get('text', '')

    if not text:
        return jsonify({'success': False, 'message': 'Text is required'})

    if function_id == 'translate_zh_to_en':
        task = translate_zh_to_en_task.delay(text)
    elif function_id == 'translate_en_to_zh':
        task = translate_en_to_zh_task.delay(text)
    elif function_id == 'summarize':
        task = summarize_task.delay(text)
    else:
        return jsonify({'success': False, 'message': 'Function not found'})

    return jsonify({'success': True, 'task_id': task.id})


@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """获取异步任务状态"""
    task = AsyncResult(task_id, app=celery)
    if task.state == 'PENDING':
        response = {'status': 'pending', 'result': None}
    elif task.state == 'SUCCESS':
        response = {'status': 'completed', 'result': task.result}
    else:
        response = {'status': 'failed', 'result': str(task.result)}
    return jsonify(response)


@app.route('/api/stream/<function_id>', methods=['POST'])
def stream_function(function_id):
    """流式返回功能结果 (使用chunked response)"""
    text = request.json.get('text', '')

    if not text:
        return jsonify({'success': False, 'message': 'Text is required'})

    def generate():
        if function_id == 'translate_zh_to_en':
            for chunk in stream_translate_zh_to_en(text):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                time.sleep(0.1)
        elif function_id == 'translate_en_to_zh':
            for chunk in stream_translate_en_to_zh(text):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                time.sleep(0.1)
        elif function_id == 'summarize':
            for chunk in stream_summarize(text):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                time.sleep(0.1)
        else:
            yield f"data: {json.dumps({'error': 'Function not found'})}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
