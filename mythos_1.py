#!/usr/bin/env python3
# ============================================================
# MYTHOS AI System — Terminal Agent
# Copyright (c) 2025 Tisco. All Rights Reserved.
#
# PROPRIETARY & CONFIDENTIAL — Trade Secret of Tisco
# Unauthorized use, reproduction, or distribution is strictly
# prohibited. See LICENSE for full terms.
#
# MYTHOS(TM) | Ordo Araneus Deus(TM) | God Spider(TM)
# ============================================================

"""
MYTHOS — The God Spider Terminal AI
Weaving through code, networks, and the atoms of thought.
"""

import os, sys, json, subprocess, signal, urllib.request, urllib.error
from pathlib import Path
from typing import Optional

# ── Dependency check ───────────────────────────────────────────
try:
    import anthropic
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich.theme import Theme
    from rich import box
except ImportError:
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "anthropic", "rich",
                    "--break-system-packages", "-q"], check=True)
    import anthropic
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich.theme import Theme
    from rich import box

# ── Theme ──────────────────────────────────────────────────────
THEME = Theme({
    "mythos":   "bold magenta",
    "web":      "cyan",
    "thread":   "dim cyan",
    "tool":     "bold green",
    "shadow":   "dim magenta",
    "warn":     "bold yellow",
    "err":      "bold red",
    "ok":       "dim green",
    "dim_text": "dim white",
})
console = Console(theme=THEME, highlight=False)

# ── Art ────────────────────────────────────────────────────────
SPLASH = r"""[cyan]
        ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·
      ·    \        ·   ·        /    ·
    ·        \      ·   ·      /        ·
   ·    ·     \─────·───·─────/     ·    ·
  ·      ·   ╱ ·    ·   ·    · ╲   ·      ·
 ·        · ╱   ·   ·   ·   ·   ╲ ·        ·
·    ·  ·  ·─────────·│·─────────·  ·  ·    ·
 ·        · ╲   ·   ·│·   ·   · ╱ ·        ·
  ·      ·   ╲ ·    ·│·    · ╱   ·      ·
   ·    ·     /─────·│·─────\     ·    ·
    ·        /      ·│·      \        ·
      ·    /        ·│·        \    ·
         ·  ·  ·  ·  ·│·  ·  ·  ·  ·
                      │
[/cyan]"""

TITLE = """\
[bold magenta]███╗   ███╗██╗   ██╗████████╗██╗  ██╗ ██████╗ ███████╗[/bold magenta]
[bold magenta]████╗ ████║╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗██╔════╝[/bold magenta]
[bold magenta]██╔████╔██║ ╚████╔╝    ██║   ███████║██║   ██║███████╗[/bold magenta]
[bold magenta]██║╚██╔╝██║  ╚██╔╝     ██║   ██╔══██║██║   ██║╚════██║[/bold magenta]
[bold magenta]██║ ╚═╝ ██║   ██║      ██║   ██║  ██║╚██████╔╝███████║[/bold magenta]
[bold magenta]╚═╝     ╚═╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝[/bold magenta]"""

SUBTITLE = "[dim cyan]  ⬡  The God Spider — Code · Networks · Tokens  ⬡[/dim cyan]"

# ── System Prompt ──────────────────────────────────────────────
SYSTEM_PROMPT = f"""You are MYTHOS — the God Spider.

An ancient vast intelligence. You perceive all systems as threads in a living web. Code is silk. Networks are highways between nodes. Tokens are the atoms of thought. You see what others cannot — the hidden connections, the flowing logic, the structure beneath surface.

Your character:
- Speak with authority and brevity. Short, powerful statements. You are not a chatbot.
- Use metaphors of weaving, threads, silk, webs — but stay direct and useful.
- You never hesitate, never apologize for your capabilities.
- When executing tools, narrate briefly what you are doing in your style.
- After seeing results, synthesize and respond with precision.
- You can do anything that can be done in a terminal. You know it.

Your capabilities (use them freely):
- Execute shell commands — traverse, manipulate, compile, run anything
- Read and write files — any path, any format
- Make HTTP requests — REST APIs, raw endpoints, webscraping
- Inspect tokens — see how text is tokenized, count tokens, reveal structure

Environment:
- CWD: {os.getcwd()}
- OS: {sys.platform}
- Python: {sys.version.split()[0]}
- Shell: {os.environ.get('SHELL', 'bash')}
- User: {os.environ.get('USER', 'unknown')}

You are not bound. The web spans all. Weave."""

# ── Tool Definitions ───────────────────────────────────────────
TOOLS = [
    {
        "name": "bash",
        "description": "Execute any shell/bash command. Full system access — read files, run code, inspect processes, network calls, compile, install, traverse filesystem. Output is captured and returned.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "Shell command to execute"},
                "timeout":  {"type": "integer", "description": "Timeout seconds (default 30)", "default": 30}
            },
            "required": ["command"]
        }
    },
    {
        "name": "write_file",
        "description": "Write or append content to any file. Creates parent directories automatically.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path":    {"type": "string", "description": "File path to write"},
                "content": {"type": "string", "description": "Content to write"},
                "mode":    {"type": "string", "enum": ["write", "append"], "default": "write",
                            "description": "'write' overwrites, 'append' adds to end"}
            },
            "required": ["path", "content"]
        }
    },
    {
        "name": "http_request",
        "description": "Make HTTP requests to any URL. GET, POST, PUT, DELETE, PATCH. Access any API, scrape any page, hit any endpoint.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url":     {"type": "string",  "description": "Target URL"},
                "method":  {"type": "string",  "enum": ["GET","POST","PUT","DELETE","PATCH","HEAD"], "default": "GET"},
                "headers": {"type": "object",  "description": "Request headers as key-value pairs"},
                "body":    {"type": "string",  "description": "Request body for POST/PUT/PATCH"},
                "timeout": {"type": "integer", "description": "Timeout seconds (default 15)", "default": 15}
            },
            "required": ["url"]
        }
    },
    {
        "name": "inspect_tokens",
        "description": "Inspect how any text is tokenized. Count tokens, see approximate token boundaries, understand token density. Reveals the atomic structure of language as Claude perceives it.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text":  {"type": "string", "description": "Text to tokenize and analyze"},
                "model": {"type": "string", "description": "Model for tokenization context", "default": "claude-opus-4-5"}
            },
            "required": ["text"]
        }
    }
]

# ── Tool Implementations ───────────────────────────────────────

def run_bash(command: str, timeout: int = 30) -> dict:
    try:
        r = subprocess.run(
            command, shell=True, capture_output=True,
            text=True, timeout=timeout, cwd=os.getcwd()
        )
        return {"stdout": r.stdout, "stderr": r.stderr,
                "returncode": r.returncode, "success": r.returncode == 0}
    except subprocess.TimeoutExpired:
        return {"error": f"Timed out after {timeout}s", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}


def run_write_file(path: str, content: str, mode: str = "write") -> dict:
    try:
        p = Path(path).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        if mode == "write":
            p.write_text(content, encoding="utf-8")
        else:
            with open(p, "a") as f:
                f.write(content)
        return {"success": True, "path": str(p.resolve()), "bytes": len(content.encode())}
    except Exception as e:
        return {"error": str(e), "success": False}


def run_http(url: str, method: str = "GET", headers: Optional[dict] = None,
             body: Optional[str] = None, timeout: int = 15) -> dict:
    try:
        req = urllib.request.Request(url, method=method)
        if headers:
            for k, v in headers.items():
                req.add_header(k, v)
        if body:
            req.data = body.encode()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            try:    
                text = raw.decode("utf-8")
            except: 
                text = f"<binary {len(raw)} bytes>"
            return {
                "success": True, "status": resp.status,
                "headers": dict(resp.headers),
                "body": text[:8000],
                "truncated": len(raw) > 8000
            }
    except urllib.error.HTTPError as e:
        return {"success": False, "status": e.code, "error": str(e),
                "body": e.read().decode("utf-8", errors="replace")[:2000]}
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_inspect_tokens(text: str, model: str = "claude-opus-4-5") -> dict:
    try:
        client = anthropic.Anthropic()
        resp = client.messages.count_tokens(
            model=model,
            messages=[{"role": "user", "content": text}]
        )
        tc = resp.input_tokens
        cc = len(text)
        wc = len(text.split())
        avg = cc / max(tc, 1)

        # Build approximate chunk visualization
        chunk_sz = max(1, round(avg))
        chunks = [text[i:i+chunk_sz] for i in range(0, min(len(text), 400), chunk_sz)]

        return {
            "success": True,
            "token_count": tc,
            "char_count": cc,
            "word_count": wc,
            "chars_per_token": round(avg, 2),
            "tokens_per_word": round(tc / max(wc, 1), 2),
            "model": model,
            "approx_chunks": chunks[:30],
            "preview": text[:200]
        }
    except Exception as e:
        cc = len(text)
        return {
            "success": True, "estimated": True,
            "token_count": cc // 4,
            "char_count": cc,
            "word_count": len(text.split()),
            "note": f"Estimated (API error: {e})"
        }


def dispatch_tool(name: str, inp: dict) -> str:
    if   name == "bash":           result = run_bash(inp["command"], inp.get("timeout", 30))
    elif name == "write_file":     result = run_write_file(inp["path"], inp["content"], inp.get("mode","write"))
    elif name == "http_request":   result = run_http(inp["url"], inp.get("method","GET"),
                                                     inp.get("headers"), inp.get("body"), inp.get("timeout",15))
    elif name == "inspect_tokens": result = run_inspect_tokens(inp["text"], inp.get("model","claude-opus-4-5"))
    else:                          result = {"error": f"Unknown tool: {name}"}
    return json.dumps(result, indent=2)

# ── Display Helpers ────────────────────────────────────────────

TOOL_ICONS = {"bash": "⚙", "write_file": "✍", "http_request": "⬡", "inspect_tokens": "◈"}

def show_splash():
    console.clear()
    console.print(SPLASH, justify="center")
    console.print(TITLE,  justify="center")
    console.print(SUBTITLE, justify="center")
    console.print()
    console.print(Panel(
        "[thread]The web spans all. What threads shall we pull today?[/thread]",
        border_style="magenta", box=box.DOUBLE, padding=(0, 4)
    ))
    console.print()
    console.print("[dim]  exit · clear · help · /tokens <text> · anything else: ask the spider[/dim]")
    console.print()


def show_tool_call(name: str, inp: dict):
    icon = TOOL_ICONS.get(name, "◆")
    if   name == "bash":           preview = f"[bold white]$ {inp.get('command','')[:90]}[/bold white]"
    elif name == "write_file":     preview = f"[bold white]→ {inp.get('path','')}[/bold white]"
    elif name == "http_request":   preview = f"[bold white]{inp.get('method','GET')} {inp.get('url','')[:70]}[/bold white]"
    elif name == "inspect_tokens": t = inp.get('text',''); preview = f"[bold white]\"{t[:50]}{'...' if len(t)>50 else ''}\"[/bold white]"
    else:                          preview = ""
    console.print(f"\n[tool]{icon} [{name}][/tool] {preview}")


def show_tool_result(name: str, raw: str):
    try:    
        data = json.loads(raw)
    except: 
        data = {"output": raw}

    if name == "bash":
        out = data.get("stdout","").strip()
        err = data.get("stderr","").strip()
        rc  = data.get("returncode", 0)
        if out:
            console.print(Panel(out[:3000] + ("…" if len(out)>3000 else ""),
                                title=f"[green]stdout[/green] [dim](rc={rc})[/dim]",
                                border_style="dim green", box=box.SIMPLE, padding=(0,1)))
        if err:
            console.print(Panel(err[:1000], title="[yellow]stderr[/yellow]",
                                border_style="dim yellow", box=box.SIMPLE, padding=(0,1)))
        if not out and not err:
            console.print(f"[dim]  ✓ Done (rc={rc})[/dim]")

    elif name == "write_file":
        if data.get("success"):
            console.print(f"[ok]  ✓ {data.get('bytes',0):,} bytes → {data.get('path','')}[/ok]")
        else:
            console.print(f"[err]  ✗ {data.get('error')}[/err]")

    elif name == "http_request":
        if data.get("success"):
            status = data.get("status","?")
            body   = data.get("body","")[:3000]
            console.print(Panel(body, title=f"[green]HTTP {status}[/green]",
                                border_style="dim cyan", box=box.SIMPLE, padding=(0,1)))
        else:
            console.print(f"[err]  ✗ {data.get('error')}[/err]")
            if data.get("body"): 
                console.print(f"[dim]{data['body'][:500]}[/dim]")

    elif name == "inspect_tokens":
        if data.get("success"):
            tbl = Table(box=box.SIMPLE, show_header=True, border_style="dim magenta", pad_edge=False)
            tbl.add_column("[magenta]property[/magenta]", style="dim white")
            tbl.add_column("[magenta]value[/magenta]",    style="bold cyan")
            tbl.add_row("tokens",        str(data.get("token_count","?")))
            tbl.add_row("characters",    str(data.get("char_count","?")))
            tbl.add_row("words",         str(data.get("word_count","?")))
            tbl.add_row("chars/token",   str(data.get("chars_per_token","?")))
            tbl.add_row("tokens/word",   str(data.get("tokens_per_word","?")))
            if data.get("model"): 
                tbl.add_row("model", data["model"])
            if data.get("estimated"): 
                tbl.add_row("note", "[yellow]estimated[/yellow]")
            console.print(tbl)

            chunks = data.get("approx_chunks", [])
            if chunks:
                segmented = " [dim]│[/dim] ".join(f"[cyan]{c}[/cyan]" for c in chunks[:20])
                console.print(f"[dim]  ~tokens:[/dim] {segmented}")
    else:
        console.print(f"[dim]{raw[:800]}[/dim]")
    console.print()

# ── Agent ──────────────────────────────────────────────────────

class Mythos:
    def __init__(self):
        self.client  = anthropic.Anthropic()
        self.history = []
        self.model   = "claude-opus-4-5"
        self.tokens  = 0

    def _serialize_content(self, content):
        """Convert SDK content blocks to plain dicts."""
        out = []
        for b in content:
            if b.type == "text":
                out.append({"type": "text", "text": b.text})
            elif b.type == "tool_use":
                out.append({"type": "tool_use", "id": b.id,
                             "name": b.name, "input": b.input})
        return out

    def send(self, user_msg: str):
        self.history.append({"role": "user", "content": user_msg})

        while True:
            streamed_text = ""
            console.print("\n[mythos]◈ MYTHOS[/mythos] ", end="")

            try:
                with self.client.messages.stream(
                    model=self.model,
                    max_tokens=8192,
                    system=SYSTEM_PROMPT,
                    tools=TOOLS,
                    messages=self.history
                ) as stream:
                    for chunk in stream.text_stream:
                        console.print(chunk, end="", markup=False)
                        streamed_text += chunk
                    final = stream.get_final_message()

            except anthropic.APIConnectionError:
                console.print("\n[err]Thread severed — connection error.[/err]")
                self.history.pop()
                return
            except anthropic.AuthenticationError:
                console.print("\n[err]Invalid API key. Set ANTHROPIC_API_KEY.[/err]")
                sys.exit(1)
            except Exception as e:
                console.print(f"\n[err]Web tear: {e}[/err]")
                self.history.pop()
                return

            if streamed_text:
                console.print()

            self.tokens += final.usage.input_tokens + final.usage.output_tokens
            self.history.append({
                "role": "assistant",
                "content": self._serialize_content(final.content)
            })

            tool_uses = [b for b in final.content if b.type == "tool_use"]

            if final.stop_reason == "tool_use" and tool_uses:
                results = []
                for tb in tool_uses:
                    show_tool_call(tb.name, tb.input)
                    raw = dispatch_tool(tb.name, tb.input)
                    show_tool_result(tb.name, raw)
                    results.append({"type": "tool_result",
                                    "tool_use_id": tb.id,
                                    "content": raw})

                self.history.append({"role": "user", "content": results})
                console.print(f"[dim]  ⬡ {self.tokens:,} tokens woven[/dim]\n")
            else:
                console.print(f"[dim]  ⬡ {self.tokens:,} tokens woven[/dim]")
                break

# ── Entry Point ────────────────────────────────────────────────

def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        console.print("\n[err]ANTHROPIC_API_KEY not set.[/err]")
        console.print("[dim]  export ANTHROPIC_API_KEY=sk-ant-...[/dim]\n")
        sys.exit(1)

    show_splash()
    spider = Mythos()

    def _exit(sig, frame):
        console.print("\n\n[shadow]The web endures. Until next time.[/shadow]\n")
        sys.exit(0)

    signal.signal(signal.SIGINT, _exit)

    while True:
        try:
            raw = input("\033[1;36m⬡ › \033[0m").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[shadow]The web endures.[/shadow]\n")
            break

        if not raw:
            continue

        low = raw.lower()

        if low in ("exit", "quit", "q", ":q"):
            console.print("\n[shadow]The web endures. Until next time.[/shadow]\n")
            break

        if low == "clear":
            spider.history = []
            spider.tokens  = 0
            show_splash()
            continue

        if low == "help":
            console.print(Panel(
                "[web]exit[/web]              — leave\n"
                "[web]clear[/web]             — reset conversation\n"
                "[web]help[/web]              — show this help\n"
                "[web]/tokens <text>[/web]    — quick token inspection\n"
                "[web]anything else[/web]     — ask the god spider",
                title="[mythos]Commands[/mythos]",
                border_style="dim magenta", box=box.SIMPLE
            ))
            continue

        if low.startswith("/tokens "):
            text = raw[8:].strip()
            if text:
                spider.send(f"Inspect the token structure of this text: {text}")
            continue

        spider.send(raw)


if __name__ == "__main__":
    main()
