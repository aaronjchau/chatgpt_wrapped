FROM python:3.14-slim

# install system dependencies
RUN apt-get update && apt-get install -y git curl nodejs npm && rm -rf /var/lib/apt/lists/*

# install uv by copying binary from its official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
