FROM linuxserver/libreoffice

WORKDIR /opt/helloyaponiya

RUN apk install python3.11 && python3.11 -m pip install poetry unicorn 

COPY .. /opt/helloyaponiya

RUN /usr/local/bin/poetry run uvicorn src.server:app --host 0.0.0.0 --port 8001

EXPOSE 8001