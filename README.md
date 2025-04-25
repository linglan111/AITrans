# AITrans
Flask 小型AI应用后端接口，对接大模型， 提供中译英、英译中、总结等功能

## run

```
celery -A src.tasks.celery worker --loglevel=info
python app.py
```

