# Event-driven FastAPI ML App

# Start the app
1. Start RabbitMQ
```bash
ONF_ENV_FILE="/opt/homebrew/etc/rabbitmq/rabbitmq-env.conf" /opt/homebrew/opt/rabbitmq/sbin/rabbitmq-server
```
2. Start Redis
```bash
brew services start redis
```
3. Start Celery Worker
```bash
celery -A app.celery_tasks.inference_task worker --loglevel=info --concurrency 10
```