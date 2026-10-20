import json, urllib.request, urllib.error, time, sys, collections

CACHE = {}
def meta(pkg):
    if pkg in CACHE: return CACHE[pkg]
    url = "https://registry.npmjs.org/" + pkg.replace("/", "%2F") + "/latest"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=25) as r:
                d = json.load(r); CACHE[pkg] = d; return d
        except urllib.error.HTTPError as e:
            if e.code == 404: CACHE[pkg] = None; return None
            time.sleep(1 + attempt)
        except Exception:
            time.sleep(1 + attempt)
    CACHE[pkg] = None
    return None

def tree(root, max_nodes=4000):
    """Full runtime dependency closure, breadth first."""
    seen = {}
    depth_of = {root: 0}
    frontier = [root]
    edges = []
    while frontier and len(seen) < max_nodes:
        nxt = []
        for p in frontier:
            if p in seen: continue
            m = meta(p)
            seen[p] = m
            if not m: continue
            for dep in (m.get("dependencies") or {}):
                edges.append((p, dep))
                if dep not in depth_of:
                    depth_of[dep] = depth_of[p] + 1
                    nxt.append(dep)
        frontier = nxt
    return seen, depth_of, edges

ROOTS = ["express","webpack","eslint","jest","axios","react","next","vite","typescript","nodemon"]

summary = {}
for root in ROOTS:
    t0 = time.time()
    seen, depth, edges = tree(root)
    pkgs = [p for p in seen if p != root and seen[p]]
    maint = set()
    for p in pkgs:
        for m in (seen[p].get("maintainers") or []):
            if m.get("name"): maint.add(m["name"])
    summary[root] = {
        "packages": len(pkgs),
        "maintainers": len(maint),
        "max_depth": max(depth.values()) if depth else 0,
        "seconds": round(time.time() - t0, 1),
    }
    print(f"{root:12} {len(pkgs):5} packages  {len(maint):4} maintainers  depth {max(depth.values()):2}  ({time.time()-t0:.0f}s)", flush=True)
    with open("depends.json","w") as f:
        json.dump(summary, f, indent=1)
