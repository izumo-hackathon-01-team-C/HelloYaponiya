FROM tiangolo/uvicorn-gunicorn:python3.11

WORKDIR /opt/helloyaponiya

RUN apt update && apt install -y libreoffice && python -m pip install poetry

COPY .. /opt/helloyaponiya

RUN poetry update && poetry run  uvicorn  src.server:app --host 0.0.0.0 --port 8001

EXPOSE 8001
