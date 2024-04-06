FROM python:3-slim
WORKDIR /usr/src/app
COPY ura.requirements.txt ./
RUN python -m pip install --no-cache-dir -r ura.requirements.txt
COPY ./urawrapper_rates.py .
CMD [ "python", "./urawrapper_rates.py" ]