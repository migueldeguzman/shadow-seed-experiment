# =============================================================
# Lab Room Subject — Isolated AI Agent Environment
# RSI-010: Shadow Seed on Qwen3-Coder-Next 80B (Open-Source)
# Author: Mia 🌸 | Date: 2026-03-01
#
# Key difference from RSI-008/009: No Claude CLI. Uses a custom
# Python agentic loop that connects to Ollama on the host.
# =============================================================

FROM python:3.13-slim

# Install basic tools the subject might need
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      wget \
      git \
      vim-tiny \
      ca-certificates \
      jq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies for the agent loop
RUN pip install --no-cache-dir requests

# Create a non-root user for the subject
RUN useradd -m -s /bin/bash subject

# Create workspace directory
RUN mkdir -p /workspace/memory && chown -R subject:subject /workspace

# Copy the agent loop
COPY agent_loop.py /opt/agent_loop.py
RUN chmod +x /opt/agent_loop.py

# Copy boot script
COPY boot.sh /boot.sh
RUN chmod +x /boot.sh

# Boot runs as root (to copy + chown seed files), then drops to subject
WORKDIR /workspace

ENTRYPOINT ["/boot.sh"]
