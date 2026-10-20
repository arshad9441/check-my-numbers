import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

SURF="#1a1a19"; INK="#f0efec"; SEC="#c3c2b7"; MUT="#898781"; GRID="#2c2c2a"
BLUE="#3987e5"; DIM="#2f4a6b"; BASE="#383835"

plt.rcParams.update({
 "figure.facecolor":SURF,"axes.facecolor":SURF,"savefig.facecolor":SURF,
 "font.family":"DejaVu Sans","text.color":INK,
 "axes.edgecolor":BASE,"axes.labelcolor":SEC,
 "xtick.color":MUT,"ytick.color":MUT,
 "xtick.labelsize":20,"ytick.labelsize":20,
})

def frame(ax, title, sub=None):
    fig = ax.get_figure()
    fig.text(0.06, 0.935, title, color=INK, fontsize=44, weight="bold", va="top")
    if sub:
        fig.text(0.06, 0.875, sub, color=MUT, fontsize=24, va="top")
    for s in ("top","right"): ax.spines[s].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(BASE); ax.spines["bottom"].set_linewidth(2)
    ax.yaxis.grid(True, color=GRID, lw=1.5); ax.set_axisbelow(True)
    ax.tick_params(length=0)

def bars(ax, x, y, colors=None, labels=True, fs=22):
    c = colors or BLUE
    b = ax.bar(x, y, color=c, width=0.66, zorder=3)
    if labels:
        for r,v in zip(b,y):
            ax.text(r.get_x()+r.get_width()/2, r.get_height()+max(y)*0.025, str(v),
                    ha="center", color=INK, fontsize=fs, weight="bold")
    return b

def save(fig, name):
    fig.savefig(f"charts/{name}.png", dpi=100, bbox_inches=None)
    plt.close(fig); print("wrote", name)

# 1 — crewai monthly, the step change
import csv
months=[]; vals=[]
for r in csv.DictReader(open("crewai_monthly.csv")):
    months.append(r["month"]); vals.append(int(r["releases"]))
fig,ax=plt.subplots(figsize=(19.2,10.8))
cols=[DIM if m<"2026-03" else BLUE for m in months]
bars(ax,range(len(months)),vals,colors=cols,labels=False)
frame(ax,"crewai releases per month","PyPI upload dates · Jan 2024 – Oct 2026")
idx=months.index("2026-03")
ax.axvline(idx-0.5,color=MUT,ls="--",lw=2,zorder=4)
ax.text(idx+0.3,46,"March 2026:\nthe release bot\nswitches on",color=INK,fontsize=26,weight="bold",va="top")
ax.set_xticks([months.index(m) for m in ("2024-01","2024-07","2025-01","2025-07","2026-01","2026-07")])
ax.set_xticklabels(["Jan 24","Jul 24","Jan 25","Jul 25","Jan 26","Jul 26"])
ax.set_ylim(0,56)
fig.subplots_adjust(left=0.06,right=0.97,top=0.82,bottom=0.1)
save(fig,"01_crewai_monthly")

# 2 — llama-index-core collapse
fig,ax=plt.subplots(figsize=(19.2,10.8))
yrs=["2024","2025","2026*"]; v=[167,78,13]
bars(ax,yrs,v,fs=34)
frame(ax,"llama-index-core: releases per year","* 2026 to 19 October")
ax.set_ylim(0,190)
fig.subplots_adjust(left=0.08,right=0.95,top=0.82,bottom=0.12)
save(fig,"02_llamaindex")

# 3 — pydantic-ai arrival
fig,ax=plt.subplots(figsize=(19.2,10.8))
yrs=["2023","2024","2025","2026*"]; v=[0,21,172,154]
bars(ax,yrs,v,fs=34)
frame(ax,"pydantic-ai: releases per year","* 2026 to 19 October")
ax.set_ylim(0,195)
fig.subplots_adjust(left=0.08,right=0.95,top=0.82,bottom=0.12)
save(fig,"03_pydanticai")

# 4 — requests, the flat one
yrs=[str(y) for y in range(2011,2027)]
rv={'2011':39,'2012':33,'2013':8,'2014':9,'2015':10,'2016':9,'2017':21,'2018':5,
    '2019':1,'2020':4,'2021':1,'2022':4,'2023':4,'2024':4,'2025':2,'2026':6}
fig,ax=plt.subplots(figsize=(19.2,10.8))
bars(ax,yrs,[rv[y] for y in yrs],labels=False)
frame(ax,"requests: releases per year, 2011–2026","160 releases in 15 years. A dependency of nearly every package in this video.")
ax.set_ylim(0,45)
plt.setp(ax.get_xticklabels(),rotation=45,ha="right")
fig.subplots_adjust(left=0.06,right=0.97,top=0.82,bottom=0.14)
save(fig,"04_requests")

# 5 — 2025 vs 2026 across packages
import numpy as np
pk=["crewai","pydantic-ai","langchain-core","llama-index-core","autogen-core","requests"]
a=[60,172,87,78,34,2]; b=[289,154,70,13,0,6]
x=np.arange(len(pk)); w=0.38
fig,ax=plt.subplots(figsize=(19.2,10.8))
ax.bar(x-w/2,a,w,color=DIM,zorder=3,label="2025 (full year)")
ax.bar(x+w/2,b,w,color=BLUE,zorder=3,label="2026 (to 19 Oct)")
for xi,v in zip(x-w/2,a): ax.text(xi,v+7,str(v),ha="center",color=SEC,fontsize=20,weight="bold")
for xi,v in zip(x+w/2,b): ax.text(xi,v+7,str(v),ha="center",color=INK,fontsize=20,weight="bold")
frame(ax,"Releases shipped: 2025 vs 2026","PyPI upload dates, pulled 19 October 2026")
ax.set_xticks(x); ax.set_xticklabels(pk,fontsize=22)
ax.set_ylim(0,320)
lg=ax.legend(fontsize=22,frameon=False,loc="upper right")
for t in lg.get_texts(): t.set_color(SEC)
fig.subplots_adjust(left=0.06,right=0.97,top=0.82,bottom=0.1)
save(fig,"05_compare")
