FROM astral/uv:python3.13-bookworm AS builder
LABEL maintainer="bomzheg <bomzheg@gmail.com>" \
      description="Telegram Bot"
ARG VCS_SHA
ARG BUILD_AT
ENV VIRTUAL_ENV=/opt/venv
ENV CODE_PATH=/code
# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy
# Omit development dependencies
ENV UV_NO_DEV=1
# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin
RUN uv venv $VIRTUAL_ENV
# Place executables in the environment at the front of the path
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
WORKDIR $CODE_PATH
COPY . ${CODE_PATH}/
RUN uv sync --locked --project ${CODE_PATH}

RUN echo "{\"vcs_hash\": \"${VCS_SHA}\", \"build_at\": \"${BUILD_AT}\" }" > version.yaml
ENTRYPOINT ["python3", "-m", "app.tgbot"]
