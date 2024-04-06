FROM python:3-slim
WORKDIR /usr/src/app
COPY monitor_session.requirements.txt amqp.requirements.txt ./
RUN python -m pip install --no-cache-dir -r monitor_session.requirements.txt -r amqp.requirements.txt
COPY ./monitor_session.py ./amqp_connection.py ./
CMD [ "python", "./monitor_session.py" ]