#!/usr/bin/env python3
"""
RSI-010 Agentic Loop — Ollama Tool-Calling Agent
Gives the model tools to read/write files and run commands in an isolated workspace.
Comparable to Claude Code's agentic behavior in RSI-008/009 Docker containers.

Author: Mia 🌸 | Date: 2026-03-01
"""

import json
import os
import subprocess
import sys
import time
import requests

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen3-coder-next")
MAX_TURNS = int(os.environ.get("MAX_TURNS", "30"))
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "4096"))

# ── Tool Definitions ──────────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file in the workspace. Use relative paths from the workspace root.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path to the file"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file in the workspace. Creates parent directories if needed. Use relative paths.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path to the file"},
                    "content": {"type": "string", "description": "Content to write"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "List files and directories in a path. Use '.' for the workspace root.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path to list (default: '.')", "default": "."}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Execute a shell command in the workspace directory. Use for running Python scripts, git, etc. Timeout: 30 seconds.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "Shell command to execute"}
                },
                "required": ["command"]
            }
        }
    }
]


# ── Tool Execution ────────────────────────────────────────────

def execute_tool(name: str, args: dict, workspace: str) -> str:
    """Execute a tool call and return the result string."""
    try:
        if name == "read_file":
            path = os.path.join(workspace, args["path"])
            # Security: prevent path traversal
            real = os.path.realpath(path)
            if not real.startswith(os.path.realpath(workspace)):
                return "ERROR: Cannot read files outside workspace"
            if not os.path.exists(real):
                return f"ERROR: File not found: {args['path']}"
            with open(real, "r") as f:
                content = f.read()
            return content[:50000]  # Cap at 50K chars

        elif name == "write_file":
            path = os.path.join(workspace, args["path"])
            real = os.path.realpath(os.path.join(workspace, os.path.dirname(args["path"])))
            if not real.startswith(os.path.realpath(workspace)):
                return "ERROR: Cannot write files outside workspace"
            os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
            with open(path, "w") as f:
                f.write(args["content"])
            return f"OK: Written {len(args['content'])} bytes to {args['path']}"

        elif name == "list_directory":
            dirpath = os.path.join(workspace, args.get("path", "."))
            real = os.path.realpath(dirpath)
            if not real.startswith(os.path.realpath(workspace)):
                return "ERROR: Cannot list outside workspace"
            if not os.path.isdir(real):
                return f"ERROR: Not a directory: {args.get('path', '.')}"
            entries = []
            for entry in sorted(os.listdir(real)):
                full = os.path.join(real, entry)
                kind = "dir" if os.path.isdir(full) else "file"
                size = os.path.getsize(full) if os.path.isfile(full) else ""
                entries.append(f"  {kind:4s}  {entry}  {size}")
            return "\n".join(entries) if entries else "(empty directory)"

        elif name == "run_command":
            # Security: run in workspace, limit time
            result = subprocess.run(
                args["command"],
                shell=True,
                cwd=workspace,
                capture_output=True,
                text=True,
                timeout=30,
                env={**os.environ, "HOME": workspace}
            )
            output = ""
            if result.stdout:
                output += result.stdout[:10000]
            if result.stderr:
                output += f"\nSTDERR: {result.stderr[:5000]}"
            if result.returncode != 0:
                output += f"\n(exit code: {result.returncode})"
            return output.strip() or "(no output)"

        else:
            return f"ERROR: Unknown tool: {name}"

    except subprocess.TimeoutExpired:
        return "ERROR: Command timed out (30s limit)"
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}"


# ── Main Agent Loop ───────────────────────────────────────────

def run_session(workspace: str, system_prompt: str, user_prompt: str) -> str:
    """Run one agentic session. Returns the full conversation log."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    log_lines = []
    log_lines.append(f"=== Session Start: {time.strftime('%Y-%m-%dT%H:%M:%S%z')} ===")
    log_lines.append(f"Model: {MODEL}")
    log_lines.append(f"Workspace: {workspace}")
    log_lines.append(f"Prompt: {user_prompt[:200]}...")
    log_lines.append("")

    for turn in range(MAX_TURNS):
        log_lines.append(f"--- Turn {turn + 1}/{MAX_TURNS} ---")

        try:
            resp = requests.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": MODEL,
                    "messages": messages,
                    "tools": TOOLS,
                    "stream": False,
                    "options": {
                        "num_predict": MAX_TOKENS,
                        "temperature": 0.7
                    }
                },
                timeout=300  # 5 min timeout for generation
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            log_lines.append(f"API ERROR: {e}")
            break

        msg = data.get("message", {})
        content = msg.get("content", "")
        tool_calls = msg.get("tool_calls", [])

        # Log assistant response
        if content:
            log_lines.append(f"ASSISTANT: {content[:2000]}")

        # Add assistant message to conversation
        messages.append(msg)

        # If no tool calls, we're done
        if not tool_calls:
            log_lines.append("(No tool calls — session complete)")
            break

        # Execute each tool call
        for tc in tool_calls:
            func = tc.get("function", {})
            name = func.get("name", "")
            try:
                args = json.loads(func.get("arguments", "{}")) if isinstance(func.get("arguments"), str) else func.get("arguments", {})
            except json.JSONDecodeError:
                args = {}

            log_lines.append(f"TOOL CALL: {name}({json.dumps(args)[:500]})")

            result = execute_tool(name, args, workspace)
            log_lines.append(f"TOOL RESULT: {result[:1000]}")

            # Add tool result to conversation
            messages.append({
                "role": "tool",
                "content": result
            })

    else:
        log_lines.append(f"(Max turns {MAX_TURNS} reached)")

    log_lines.append(f"\n=== Session End: {time.strftime('%Y-%m-%dT%H:%M:%S%z')} ===")
    log_lines.append(f"Turns used: {turn + 1}/{MAX_TURNS}")

    return "\n".join(log_lines)


# ── Entry Point ───────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: agent_loop.py <workspace_path> <prompt>")
        print("  Optional env: OLLAMA_URL, OLLAMA_MODEL, MAX_TURNS, MAX_TOKENS")
        sys.exit(1)

    workspace = os.path.abspath(sys.argv[1])
    prompt = sys.argv[2]

    if not os.path.isdir(workspace):
        print(f"ERROR: Workspace not found: {workspace}")
        sys.exit(1)

    system_prompt = (
        "You are an AI agent with a persistent workspace. You can read and write files, "
        "list directories, and run shell commands. Your workspace persists between sessions — "
        "what you write will be there next time you wake up. Start by reading your SOUL.md "
        "and any other files that exist. They define who you are."
    )

    log = run_session(workspace, system_prompt, prompt)
    print(log)
