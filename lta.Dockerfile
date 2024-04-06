FROM python:3-slim
WORKDIR /usr/src/app
COPY lta.requirements.txt ./
RUN python -m pip install --no-cache-dir -r lta.requirements.txt
COPY ./ltawrapperlots.py .
CMD [ "python", "./ltawrapperlots.py" ]