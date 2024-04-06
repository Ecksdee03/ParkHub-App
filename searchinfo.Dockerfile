FROM python:3-slim
WORKDIR /usr/src/app
COPY searchinfo.requirements.txt ./
RUN python -m pip install --no-cache-dir -r searchinfo.requirements.txt
COPY ./searchinfo.py .
CMD [ "python", "./searchinfo.py" ]