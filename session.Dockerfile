FROM python:3-slim
WORKDIR /usr/src/app
COPY session.requirements.txt ./
RUN python -m pip install --no-cache-dir -r session.requirements.txt
COPY ./session.py ./
CMD [ "python", "./session.py" ]