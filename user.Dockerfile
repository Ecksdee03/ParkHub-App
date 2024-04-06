FROM python:3-slim
WORKDIR /usr/src/app
COPY user.requirements.txt ./
RUN python -m pip install --no-cache-dir -r user.requirements.txt
COPY ./user.py ./
CMD [ "python", "./user.py" ]