import json,urllib.request,csv,sys
pkgs=["langchain","langchain-core","langchain-openai","llama-index","llama-index-core","crewai","crewai-tools",
"autogen-agentchat","openai","anthropic","google-genai","mistralai","cohere","litellm","instructor","dspy",
"haystack-ai","semantic-kernel","guidance","outlines","transformers","sentence-transformers","vllm","peft",
"chromadb","qdrant-client","weaviate-client","pinecone","faiss-cpu","pydantic","pydantic-ai","fastapi",
"streamlit","gradio","django","flask","requests","numpy","pandas"]
rows=[]
for p in pkgs:
    try:
        d=json.load(urllib.request.urlopen(f"https://pypi.org/pypi/{p}/json",timeout=25))
    except Exception as e:
        print("MISS",p,file=sys.stderr); continue
    ds=sorted(f[0]["upload_time"][:10] for f in d["releases"].values() if f)
    if not ds: continue
    c=lambda y:sum(1 for x in ds if x.startswith(y))
    rows.append({"package":p,"first_release":ds[0],"latest":ds[-1],"total":len(ds),
                 "y2023":c("2023"),"y2024":c("2024"),"y2025":c("2025"),"y2026ytd":c("2026")})
with open("releases.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"{'package':24}{'2023':>6}{'2024':>6}{'2025':>6}{'2026':>6}  {'latest':>11}")
for r in sorted(rows,key=lambda r:-r["y2026ytd"]):
    print(f"{r['package']:24}{r['y2023']:6}{r['y2024']:6}{r['y2025']:6}{r['y2026ytd']:6}  {r['latest']:>11}")
