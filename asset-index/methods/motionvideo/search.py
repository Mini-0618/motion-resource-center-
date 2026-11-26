"""Public MotionVideo metadata lookup. Python 3 + requests. No account needed."""
import argparse
import json
import sys

import requests

ENDPOINT = "https://mcp.motionvideo.xyz/mcp"
PUBLIC = ("list-filters", "search-videos", "get-video", "search-directory")


def request(session, method, params, call_id=None):
    payload = {"jsonrpc": "2.0", "method": method, "params": params}
    if call_id is not None:
        payload["id"] = call_id
    response = session.post(ENDPOINT, json=payload, timeout=(10, 35))
    response.raise_for_status()
    if session_id := response.headers.get("Mcp-Session-Id"):
        session.headers["Mcp-Session-Id"] = session_id
    if call_id is None:
        return None
    raw = response.content.decode("utf-8")
    if "text/event-stream" in response.headers.get("Content-Type", ""):
        messages = []
        for event in raw.replace("\r\n", "\n").split("\n\n"):
            lines = [line[5:].lstrip(" ") for line in event.split("\n") if line.startswith("data:")]
            if lines:
                messages.append(json.loads("\n".join(lines)))
        result = next((m for m in messages if m.get("id") == call_id), {})
    else:
        result = json.loads(raw)
    if "error" in result or "result" not in result:
        raise ValueError("MCP error: " + str(result.get("error", "missing response")))
    return result["result"]


def lookup(name, arguments):
    with requests.Session() as session:
        session.headers.update({"Accept": "application/json, text/event-stream"})
        hello = request(session, "initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                        "clientInfo": {"name": "motion-library-lookup", "version": "1"}}, 1)
        session.headers["MCP-Protocol-Version"] = hello["protocolVersion"]
        request(session, "notifications/initialized", {})
        listed = request(session, "tools/list", {}, 2)
        if name not in {tool["name"] for tool in listed["tools"]}:
            raise ValueError("Tool absent from current tools/list: " + name)
        response = request(session, "tools/call", {"name": name, "arguments": arguments}, 3)
        if response.get("isError"):
            raise ValueError(str(response.get("content"))[:500])
        result = response.get("structuredContent")
        if result is None:
            raise ValueError("Missing structuredContent in tool result")
        keys = ["slug", "title", "handle", "pageUrl", "promptShared", "category"]
        if name == "get-video":
            return {key: result.get(key) for key in keys}
        if name == "search-videos":
            result["videos"] = [{key: item.get(key) for key in keys} for item in result["videos"]]
        if name == "search-directory":
            result["entries"] = [{key: item.get(key) for key in ("id", "name", "url", "category")}
                                 for item in result["entries"]]
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tool", choices=PUBLIC)
    parser.add_argument("arguments", nargs="?", default="{}", help="JSON object")
    parser.add_argument("--input", help="Read UTF-8 JSON arguments from file")
    args = parser.parse_args()
    try:
        if args.input:
            with open(args.input, encoding="utf-8-sig") as file:
                params = json.load(file)
        else:
            params = json.loads(args.arguments)
        if not isinstance(params, dict):
            raise ValueError("Expected a JSON object")
        print(json.dumps(lookup(args.tool, params), ensure_ascii=False, indent=2))
    except (requests.RequestException, OSError, ValueError) as error:
        sys.exit(str(error))
