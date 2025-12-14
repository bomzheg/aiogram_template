FROM python:3.13-bookworm AS builder
ENV VIRTUAL_ENV=/opt/venv
ENV CODE_PATH=/code
RUN python3 -m venv $VIRTUAL_ENV
WORKDIR $CODE_PATH
COPY lock.txt ${CODE_PATH}/
RUN $VIRTUAL_ENV/bin/pip install uv && $VIRTUAL_ENV/bin/uv pip install -r lock.txt

FROM python:3.13-slim-bookworm
LABEL maintainer="bomzheg <bomzheg@gmail.com>" \
      description="Telegram Bot"
ARG VCS_SHA
ARG BUILD_AT
ENV VIRTUAL_ENV=/opt/venv
ENV CODE_PATH=/code
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV
COPY . ${CODE_PATH}/app
WORKDIR $CODE_PATH/app
RUN echo "{\"vcs_hash\": \"${VCS_SHA}\", \"build_at\": \"${BUILD_AT}\" }" > version.yaml
ENTRYPOINT ["python3", "-m", "app"]
