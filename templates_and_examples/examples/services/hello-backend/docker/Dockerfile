FROM local-only/base-python-cpu:latest

LABEL IMAGE="hello-backend"
LABEL VERSION="0.1.0"
LABEL BUILD_IGNORE="False"

WORKDIR /kaapana/app

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY files/requirements.txt ./requirements.txt
RUN pip install -c https://raw.githubusercontent.com/kaapana/kaapana/0.2.1/build-scripts/constraints-0.2.1.txt -r ./requirements.txt

COPY files/ ./
RUN chmod +x boot.sh

ENV FLASK_APP run.py

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]

