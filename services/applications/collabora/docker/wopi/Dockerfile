FROM docker.io/node:lts-alpine3.16 as build-stage

WORKDIR /app
COPY files/ui/yarn.lock files/ui/package*.json ./
RUN yarn install

COPY files/ui .
RUN yarn build


FROM local-only/base-python-cpu:latest

LABEL IMAGE="kaapana-wopi"
LABEL VERSION="0.1.0"
LABEL BUILD_IGNORE="False"

COPY --from=build-stage /app/dist /app/ui/dist
WORKDIR /app

COPY files/requirements.txt /app/
RUN python -m pip install -c https://raw.githubusercontent.com/kaapana/kaapana/0.2.1/build-scripts/constraints-0.2.1.txt --no-cache-dir -r /app/requirements.txt

COPY files/run.sh /app
COPY files/app /app/app

ENTRYPOINT ["/app/run.sh"]