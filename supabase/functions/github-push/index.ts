// supabase/functions/github-push/index.ts
// Generic "create repo + push files" relay for GitHub.
// Reads GITHUB_TOKEN from the function's secrets (never from the caller).
import { serve } from "https://deno.land/std@0.208.0/http/server.ts";

const GH = "https://api.github.com";
const API_VERSION = "2022-11-28";

async function gh(path: string, token: string, method = "GET", body?: unknown) {
  const res = await fetch(GH + path, {
    method,
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": API_VERSION,
      "Content-Type": "application/json",
      "User-Agent": "supabase-github-push",
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const text = await res.text();
  let data: unknown = {};
  try {
    data = JSON.parse(text);
  } catch {
    /* non-JSON error body */
  }
  if (!res.ok) {
    throw new Error(
      `GitHub ${method} ${path} -> ${res.status}: ${text.slice(0, 400)}`,
    );
  }
  return data as Record<string, unknown>;
}

interface PushFile {
  path: string; // repo-relative, e.g. "README.md" or "media/demo.mp4"
  content: string; // base64
  message?: string;
}

serve(async (req: Request) => {
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "POST only" }), { status: 405 });
  }
  const token = Deno.env.get("GITHUB_PAT_MUSE") ?? Deno.env.get("GITHUB_TOKEN") ??
    Deno.env.get("GITHUB_PAT");
  if (!token) {
    return new Response(JSON.stringify({ error: "GITHUB_TOKEN secret not set" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }

  let payload: {
    repo: string;
    description?: string;
    isPrivate?: boolean;
    files: PushFile[];
  };
  try {
    payload = await req.json();
  } catch {
    return new Response(JSON.stringify({ error: "invalid JSON body" }), {
      status: 400,
    });
  }
  const { repo, description = "", isPrivate = true, files } = payload;
  if (!repo || !Array.isArray(files) || files.length === 0) {
    return new Response(
      JSON.stringify({ error: "body needs {repo, files:[{path, content(base64)}]}" }),
      { status: 400 },
    );
  }

  try {
    const me = await gh("/user", token);
    const owner = me.login as string;

    const created = await gh("/user/repos", token, "POST", {
      name: repo,
      description,
      private: isPrivate,
      auto_init: false,
    });

    const pushed: string[] = [];
    for (const f of files) {
      await gh(
        `/repos/${owner}/${repo}/contents/${f.path}`,
        token,
        "PUT",
        { message: f.message ?? `add ${f.path}`, content: f.content },
      );
      pushed.push(f.path);
    }

    return new Response(
      JSON.stringify({
        ok: true,
        repo_url: created.html_url,
        owner,
        files_pushed: pushed,
      }),
      { headers: { "Content-Type": "application/json" } },
    );
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return new Response(JSON.stringify({ ok: false, error: msg }), {
      status: 502,
      headers: { "Content-Type": "application/json" },
    });
  }
});
