FROM tiangolo/uvicorn-gunicorn:python3.11

WORKDIR /opt/helloyaponiya

RUN apt update && apt install -y libreoffice && apt -y install locales && locale-gen en_US.UTF-8 && python -m pip install poetry

ENV LANG=en_US.UTF-8

COPY .. /opt/helloyaponiya

EXPOSE 8001

RUN poetry update

CMD ["poetry", "run", "uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8001"]
