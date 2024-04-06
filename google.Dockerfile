FROM python:3-slim
WORKDIR /usr/src/app
COPY google.requirements.txt ./
RUN python -m pip install --no-cache-dir -r google.requirements.txt
COPY ./googlewrapper.py .
CMD [ "python", "./googlewrapper.py" ]