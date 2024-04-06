FROM python:3-slim
WORKDIR /usr/src/app
COPY searchAmenities.requirements.txt ./
RUN python -m pip install --no-cache-dir -r searchAmenities.requirements.txt
COPY ./searchAmenities.py .
COPY ./invokes.py .
CMD [ "python", "./searchAmenities.py" ]
