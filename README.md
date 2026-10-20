# check-my-numbers

Data and scripts behind the [Check My Numbers](https://www.youtube.com/@CheckMyNumbers)
channel. Every video is built from numbers computed here, not quoted from
somewhere else. Re-run anything; the figures will have moved since.

## 01 — Release velocity (19 October 2026)

**Question.** When you pick a Python library, does "this project ships often"
mean it is healthy?

**Method.** Pulled the complete release history of 39 packages from the PyPI
JSON API (`https://pypi.org/pypi/<package>/json`) and counted upload dates per
calendar year. No stars, no download counts. 2026 figures run to 19 October,
so they cover 292 days and understate the year.

**Findings.**

| Package | 2023 | 2024 | 2025 | 2026 (to 19 Oct) |
|---|---|---|---|---|
| crewai | 8 | 118 | 60 | 289 |
| crewai-tools | 0 | 49 | 67 | 289 |
| pydantic-ai | 0 | 21 | 172 | 154 |
| langchain-core | 20 | 136 | 87 | 70 |
| llama-index-core | 0 | 167 | 78 | 13 |
| autogen-core | 0 | 15 | 34 | 0 |
| ag2 | 0 | 17 | 49 | 29 |
| requests | 4 | 4 | 2 | 6 |

1. **crewai's 289 releases are automated.** 289 across 193 distinct days, and
   `crewai-tools` reports the identical count and identical version
   (1.15.28). Two packages do not independently land on the same release count.
   The monthly series shows a step, not a ramp: 6 releases in February 2026,
   40 in March. The number measures a CI pipeline.
2. **The llama-index family contracted about six-fold.** Core went 167 → 78 →
   13. Tested against the "it just split into sub-packages" explanation and
   rejected it: `llama-index-readers-file` went 47 → 16 → 2,
   `llama-index-vector-stores-chroma` 20 → 7 → 1,
   `llama-index-agent-openai` 28 → 11 → 0.
3. **Microsoft's AutoGen line stopped on 2025-09-30**, all three packages at
   version 0.7.5. It did not die — the project continues as `ag2` under its
   original authors, last released 2026-10-03. The first draft of the video
   said "AutoGen is dead". That was wrong, and the correction is left in.
4. **requests shipped 6 releases this year** and is a dependency of nearly
   every package above.

**Conclusion.** Release frequency measures how unsettled a project's API still
is, not how healthy it is. High velocity is interesting to watch and expensive
to depend on.

### Re-running it

```bash
python3 pull.py        # writes releases.csv
python3 mkcharts.py    # writes charts/*.png  (needs matplotlib)
```

`pull.py` hits the public PyPI API with no key and no rate limit worth
worrying about. `releases.csv` is the output as of 19 October 2026 and
`crewai_monthly.csv` is the per-month series for that package.

### Corrections

Found an error? Open an issue. Corrections get named in the next video.
