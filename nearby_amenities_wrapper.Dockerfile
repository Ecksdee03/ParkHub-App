FROM python:3-slim
WORKDIR /usr/src/app
COPY nearby_amenities_wrapper.requirements.txt ./
RUN python -m pip install --no-cache-dir -r nearby_amenities_wrapper.requirements.txt
COPY ./nearby_amenities_wrapper.py .
CMD [ "python", "./nearby_amenities_wrapper.py" ]
