"""GitHub metadata discovery prototype.

Collects candidates only. It NEVER runs downloaded code or claims that a
repository/homepage contains a verified motion preview.
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

BEIJING = ZoneInfo("Asia/Shanghai")
TOPICS = (
    ("gsap", "UI-01"), ("lottie", "UI-11"), ("threejs", "UI-05"),
    ("remotion", "V-01"), ("manim", "V-02"), ("blender", "V-12"),
    ("svg-animation", "UI-11"), ("motion-graphics", "V-10"),
    ("rive", "UI-01"), ("web-animation", "UI-02"),
    ("animated-charts", "V-02"), ("parallax", "V-09"),
    ("kinetic-typography", "V-01"), ("react-animation", "UI-01"),
    ("after-effects", "V-10"), ("generative-art", "V-11"),
)
MAX_PER_RUN = 24


def timestamp():
    return datetime.now(BEIJING)


def source_queries(now=None):
    """Rotate discovery topics across 15-minute Beijing-time windows."""
    now = now or timestamp()
    slot = ((now.toordinal() * 96) + now.hour * 4 + now.minute // 15)
    count = len(TOPICS)
    queries = []
    for offset in (0, 5, 10, 13):
        topic, category = TOPICS[(slot + offset) % count]
        # 'evergreen' is a discovery source pool, not evidence of validation.
        pool = "evergreen" if offset == 13 else "daily"
        queries.append((topic, category, pool))
    return queries


def api_search(topic, token, pool):
    q = f"topic:{topic} archived:false fork:false"
    params = urlencode({"q": q, "sort": "stars" if pool == "evergreen" else "updated",
                        "order": "desc", "per_page": 100})
    request = Request(
        "https://api.github.com/search/repositories?" + params,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "motion-resource-center-v4",
            "X-GitHub-Api-Version": "2022-11-28",
            **({"Authorization": "Bearer " + token} if token else {}),
        },
    )
    with urlopen(request, timeout=25) as response:
        return json.load(response).get("items", [])


def safe_http_url(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = urlparse(value.strip())
    except ValueError:
        return None
    if parsed.scheme not in ("https", "http") or not parsed.netloc:
        return None
    return value.strip()


def candidate_from_repo(repo, category, pool, discovered_at):
    url = safe_http_url(repo.get("html_url"))
    if not url or "github.com" not in urlparse(url).hostname.casefold():
        return None
    license_data = repo.get("license") or {}
    license_id = license_data.get("spdx_id") if isinstance(license_data, dict) else None
    if license_id in (None, "NOASSERTION", ""):
        license_id = None
    repo_id = str(repo.get("id") or hashlib.sha256(url.encode()).hexdigest())
    return {
        "id": "github-" + repo_id,
        "title": str(repo.get("full_name") or repo.get("name") or url),
        "url": url,
        "description": str(repo.get("description") or "")[:500],
        "demo_url": safe_http_url(repo.get("homepage")),
        "preview_url": None,
        "preview_verified": False,
        "source_verified": False,
        "reproduced": False,
        "status": "DISCOVERED",
        "category": category,
        "source_pool": pool,
        "source": "GitHub repository search",
        "license_spdx_reported": license_id,
        "license_verified": False,
        "source_updated_at": repo.get("pushed_at"),
        "discovered_at": discovered_at,
    }


def seen_file(root, digest):
    return root / "state" / "seen" / (digest[:2] + ".txt")


def already_seen(root, digest, cache):
    path = seen_file(root, digest)
    if path not in cache:
        cache[path] = set(path.read_text(encoding="ascii").splitlines()) if path.exists() else set()
    return digest in cache[path]


def collect(root, api=api_search, now=None, token=None, max_results=MAX_PER_RUN):
    """Persist candidates and permanent SHA-256 de-duplication across runs."""
    if not 1 <= max_results <= MAX_PER_RUN:
        raise ValueError("max_results must be between 1 and 24")
    root = Path(root)
    now = now or timestamp()
    token = token if token is not None else os.environ.get("GH_TOKEN", "")
    stamp = now.isoformat(timespec="seconds")
    seen_cache, pending, errors, candidates = {}, {}, [], []
    examined = 0
    for topic, category, pool in source_queries(now):
        try:
            records = api(topic, token, pool)
        except Exception as exc:
            errors.append({"topic": topic, "error": str(exc)[:200]})
            continue
        for repo in records:
            examined += 1
            entry = candidate_from_repo(repo, category, pool, stamp)
            if entry is None:
                continue
            digest = hashlib.sha256(entry["url"].casefold().encode("utf-8")).hexdigest()
            path = seen_file(root, digest)
            if already_seen(root, digest, seen_cache):
                continue
            entry["url_sha256"] = digest
            candidates.append(entry)
            seen_cache[path].add(digest)
            pending.setdefault(path, []).append(digest)
            if len(candidates) >= max_results:
                break
        if len(candidates) >= max_results:
            break

    day = now.strftime("%Y-%m-%d")
    catalog = root / "daily" / (day + ".jsonl")
    catalog.parent.mkdir(parents=True, exist_ok=True)
    with catalog.open("a", encoding="utf-8") as out:
        for entry in candidates:
            out.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")
    for path, hashes in pending.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="ascii") as out:
            for digest in hashes:
                out.write(digest + "\n")
    result = {
        "time_beijing": stamp,
        "target": max_results,
        "new_candidates": len(candidates),
        "source_repositories_examined": examined,
        "errors": errors,
        "candidates_without_verified_preview": sum(not x["preview_verified"] for x in candidates),
        "source": "GitHub public repositories only",
    }
    summary_file = root / "latest-run.json"
    summary_file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description="Collect real GitHub repository candidates only")
    parser.add_argument("--data-dir", default="./motion-data")
    parser.add_argument("--max-results", type=int, default=24)
    args = parser.parse_args()
    result = collect(args.data_dir, max_results=args.max_results)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    # If all provider requests fail, fail the workflow rather than presenting a successful run.
    if result["new_candidates"] == 0 and result["errors"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
