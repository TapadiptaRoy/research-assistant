# Multi-Source Research Assistant
"# research-assistant" 
# Multi-Source Research Assistant

A research assistant that answers questions by pulling from academic papers (arXiv, PubMed, OpenAlex) and current web results, then synthesizes everything into one coherent, cited answer. Built with LangChain and LangGraph.

Ask it something, and it will:
1. Decide which sources are actually relevant to your question
2. Fetch results from those sources in parallel
3. If results come back thin, automatically broaden the search and retry
4. Write one answer that cites which source backs each claim
5. Remember the conversation so you can ask natural follow-ups

## Why this exists

Most "AI search" tools either only use the web (missing peer-reviewed science) or only use academic databases (missing anything current). This assistant routes each question to whichever sources actually fit it, rather than always querying everything.

## Architecture

```
User question
     │
     ▼
┌─────────────┐
│   Router     │  Claude decides which sources are relevant
│ (LLM call)   │  based on the question + conversation history
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Retrieve    │  Calls the chosen source(s) in parallel:
│              │  arXiv · PubMed · OpenAlex · Web (Tavily)
└──────┬──────┘
       │
       ▼
  ┌─────────┐
  │ Enough   │──No──▶ Retry with all 4 sources + broader results
  │ results? │        (capped at 1 retry to guarantee termination)
  └────┬────┘
       │ Yes
       ▼
┌─────────────┐
│  Synthesize  │  Claude writes one cited answer from the
│ (LLM call)   │  combined, normalized documents
└──────┬──────┘
       │
       ▼
   Final answer + source citations
```

This flow is implemented as a **LangGraph** state machine (`graph/workflow.py`), with each stage above being a graph node, and the "enough results?" check being a real conditional edge — not just a linear script.

## Project structure

```
research-assistant/
├── backend/
│   └── app.py              # FastAPI server wrapping the LangGraph pipeline
├── interface/
│   ├── cli.py               # Terminal interface
│   └── web/
│       └── index.html       # Web UI (calls the FastAPI backend)
├── graph/
│   ├── state.py             # Shared state schema passed between graph nodes
│   └── workflow.py          # The LangGraph graph: nodes, edges, retry logic
├── router/
│   └── query_router.py      # LLM-based decision on which sources to use
├── sources/
│   ├── arxiv_source.py      # arXiv API integration
│   ├── pubmed_source.py     # PubMed API integration (via LangChain)
│   ├── openalex_source.py   # OpenAlex API integration
│   └── web_source.py        # Web search via Tavily
├── synthesis/
│   └── synthesizer.py       # Merges documents into one cited answer
├── tests/
│   └── test_sources.py      # Unit tests for source normalization logic
└── config.py                 # Centralized env var loading
```

## Sources used

| Source | What it covers | Auth required |
|---|---|---|
| [arXiv](https://arxiv.org) | Physics, CS, math preprints | No |
| [PubMed](https://pubmed.ncbi.nlm.nih.gov) | Medical & life sciences literature | No |
| [OpenAlex](https://openalex.org) | General academic papers, 240M+ works | No |
| [Tavily](https://tavily.com) | Current web/news results | Yes (free tier) |

Every source is normalized to the same schema before being handed to the synthesizer, so the LLM sees a consistent format regardless of which API it came from:

```python
{
    "title": str,
    "authors": list[str],
    "published": str,
    "url": str,
    "source": str  # "arxiv" | "pubmed" | "openalex" | "web"
}
```

All four sources fail gracefully — if one API is down or rate-limited, the pipeline continues with whatever succeeded rather than crashing.

## Setup

### 1. Clone and create a virtual environment

```bash
git clone <your-repo-url>
cd research-assistant
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API keys

Copy the example env file and fill in your keys:

```bash
copy .env.example .env        # Windows
# cp .env.example .env        # macOS/Linux
```

Edit `.env`:

```
ANTHROPIC_API_KEY=your_key_here      # required — get one at console.anthropic.com
TAVILY_API_KEY=your_key_here         # required — free tier at tavily.com
```

arXiv, PubMed, and OpenAlex need no API key.

### 4. Run it

**Web UI (recommended):**
```bash
uvicorn backend.app:app --reload
```
Then open `http://127.0.0.1:8000`

**Terminal / CLI:**
```bash
python -m interface.cli
```

## Running tests

```bash
pytest tests/
```

## Design decisions worth knowing

- **Semantic Scholar was dropped in favor of OpenAlex** — Semantic Scholar's free-tier rate limits (429 errors) made it impractical for iterative development. OpenAlex covers similar ground with no auth requirement and no rate-limit friction.
- **Retry logic is capped at 1 attempt** — the conditional loop in the graph always terminates: after one retry with a broadened search, the pipeline proceeds with whatever it has rather than looping indefinitely.
- **The router uses the LLM, not keyword rules** — deciding which sources fit a question is a judgment call ("what's the latest on X" implies web + maybe arXiv; "explain the mechanism of X" implies academic sources), which keyword matching handles poorly.

## Known limitations

- Conversation history currently lives only in memory (browser session / CLI process) — refreshing the page or restarting the CLI clears it.
- PubMed's `authors` field is not populated (the LangChain wrapper doesn't expose it in a usable form) — every other source does return author names.
- No streaming; the full answer is generated before anything is returned to the UI.