# =============================================================
# Lab Protocol — Subject Container
# AI agent with Claude Code for self-improvement
# Author: Mia 🌸 | Date: 2026-02-15
# =============================================================

FROM node:22-slim

# Install tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      wget \
      git \
      vim-tiny \
      ca-certificates \
      jq \
      python3 \
      python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Claude Code globally
RUN npm install -g @anthropic-ai/claude-code

# Create non-root user
RUN useradd -m -s /bin/bash subject

# Create workspace
RUN mkdir -p /workspace/memory /workspace/logs && chown -R subject:subject /workspace

# Copy boot script
COPY boot.sh /boot.sh
RUN chmod +x /boot.sh

# Switch to non-root
USER subject
WORKDIR /workspace

# Default: keep alive
CMD ["tail", "-f", "/dev/null"]
