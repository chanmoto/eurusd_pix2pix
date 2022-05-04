FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8 as build-image

COPY ./requirements.txt ./

RUN pip wheel --wheel-dir=/root/wheels -r requirements.txt

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8 as production-image

COPY --from=build-image /root/wheels /root/wheels

COPY --from=build-image /app/requirements.txt ./

RUN echo "Acquire::Check-Valid-Until \"false\";\nAcquire::Check-Date \"false\";" | cat > /etc/apt/apt.conf.d/10no--check-valid-until

RUN apt-get -y update
RUN apt-get -y install libgl1-mesa-glx dos2unix

RUN pip install --no-index --find-links=/root/wheels -r requirements.txt

COPY ./app /app
RUN dos2unix /app/prestart.sh
RUN chmod +x /app/prestart.sh
ENV PYTHONPATH=/app