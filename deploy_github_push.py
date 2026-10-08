#!/usr/bin/env python3
"""Deploy the github-push edge function via Supabase Management API.

Usage:
  SUPABASE_ACCESS_TOKEN=sbp_... ./deploy_github_push.py

The token is read ONLY from the env var (never printed, never logged).
Project ref: jlvozmgxxojvljxuhywv
"""
import json
import os
import sys
import urllib.request
import uuid

PROJECT_REF = "jlvozmgxxojvljxuhywv"
MGMT = "https://api.supabase.com"
SLUG = "github-push"
FUNC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "supabase", "functions", SLUG)


def mgmt_request(method, path, body=None, headers=None):
    token = os.environ.get("SUPABASE_ACCESS_TOKEN", "")
    if not token:
        print("SUPABASE_ACCESS_TOKEN is not set", file=sys.stderr)
        sys.exit(1)
    # mask token in any error output
    def mask(s):
        return s.replace(token, "***") if isinstance(s, str) else s

    data = None
    h = {"Authorization": "Bearer " + token}
    if headers:
        h.update(headers)
    if body is not None:
        data = json.dumps(body).encode()
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(MGMT + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode()
            return resp.status, json.loads(raw) if raw else {}
    except Exception as e:  # urllib.error.HTTPError etc.
        print(f"request failed: {mask(str(e))}", file=sys.stderr)
        try:
            print(mask(e.read().decode()[:500]), file=sys.stderr)  # type: ignore
        except Exception:
            pass
        sys.exit(1)


def deploy():
    index_path = os.path.join(FUNC_DIR, "index.ts")
    with open(index_path, "rb") as f:
        code = f.read()

    boundary = uuid.uuid4().hex
    metadata = json.dumps({
        "entrypoint_path": "index.ts",
        "name": SLUG,
        "verify_jwt": True,
    })
    parts = []
    parts.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="metadata"\r\n\r\n{metadata}\r\n'
        .encode()
    )
    parts.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="index.ts"\r\n'
        f'Content-Type: application/typescript\r\n\r\n'.encode() + code + b'\r\n'
    )
    parts.append(f'--{boundary}--\r\n'.encode())
    body = b"".join(parts)

    token = os.environ.get("SUPABASE_ACCESS_TOKEN", "")
    req = urllib.request.Request(
        f"{MGMT}/v1/projects/{PROJECT_REF}/functions/deploy?slug={SLUG}",
        data=body,
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            print("deploy status:", resp.status)
            print(resp.read().decode()[:800].replace(token, "***"))
    except Exception as e:
        print(f"deploy failed: {str(e)[:200].replace(token, '***')}", file=sys.stderr)
        sys.exit(1)


def set_secret(name, value):
    # value comes from argv (never logged)
    status, out = mgmt_request(
        "POST", f"/v1/projects/{PROJECT_REF}/secrets",
        body=[{"name": name, "value": value}],
    )
    print("secret status:", status)


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "set-secret":
        set_secret(sys.argv[2], sys.argv[3])
    else:
        deploy()
