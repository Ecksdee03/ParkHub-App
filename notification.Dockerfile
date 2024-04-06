FROM python:3-slim
WORKDIR /usr/src/app
COPY ./amqp.requirements.txt ./
RUN python -m pip install --no-cache-dir -r amqp.requirements.txt
COPY ./notification.py ./amqp_connection.py ./
CMD [ "python", "./notification.py" ]