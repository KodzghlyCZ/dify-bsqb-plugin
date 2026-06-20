# Dify BSQB Plugin

Dify tool plugin for [bsqb](https://pypi.org/project/bsqb/) — a type-safe Brave Search query builder.

Unlike the stock Brave Search plugin, this plugin lets agents and workflows build validated operator-based queries (`site:`, `filetype:`, `lang:`, exclusions, exact phrases, AND/OR/NOT) before searching.

## Tools

| Tool | Purpose |
| --- | --- |
| **Build Brave Query** | Build and validate a Brave Search `q` string with bsqb. No API call. |
| **Brave Search (BSQB)** | Build the query with bsqb, then call the Brave Search API and return results. |

## Prerequisites

- Python 3.12+
- [Dify plugin CLI](https://docs.dify.ai/en/develop-plugin/getting-started/cli) (optional, for packaging)
- Brave Search API key from [brave.com/search/api](https://brave.com/search/api/)

## Setup

```bash
cd dify-bsqb-plugin
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Edit `.env` with your Dify remote debug credentials from **Plugin Management** in Dify.

## Remote debug

```bash
python -m main
```

Install the plugin in your Dify workspace, then authorize it with your Brave Search API key.

## Package locally

```bash
dify-plugin-daemon plugin package . -o bsqb-0.1.0.difypkg
```

Upload the `.difypkg` via **Plugins → Install → Via Local File**.

## Automated GitHub releases

Push a version tag that matches `version` in `manifest.yaml`:

```bash
# 1. Bump version in manifest.yaml
# 2. Commit and tag
git add manifest.yaml
git commit -m "chore: release v0.1.0"
git tag v0.1.0
git push origin main --tags
```

GitHub Actions (`.github/workflows/release.yml`) will:

1. Verify the tag matches `manifest.yaml`
2. Regenerate `requirements.txt`
3. Build `bsqb-<version>.difypkg`
4. Publish a GitHub Release with the package attached

Download the `.difypkg` from the release page and install it in Dify.

## Example agent usage

Ask an agent to:

> Find PDFs about climate change on `.edu` sites published with "2024" in the title, in English from US results.

The **Brave Search (BSQB)** tool maps that to something like:

```text
climate change filetype:pdf site:edu intitle:2024 lang:en loc:us
```

## Operator parameters

Both tools accept the same query-building fields:

- `query` — main keywords
- `raw_query` — skip structured fields and use a full query string
- `phrase`, `include`, `exclude`
- `site`, `filetype`, `ext`
- `intitle`, `inbody`, `inpage`
- `lang`, `loc`
- `and_query`, `or_query`, `not_query`
- `validate` — enforce Brave's 400 character / 50 word limits (default: true)

**Brave Search (BSQB)** also accepts `count` (1–20) and `ensure_ascii`.

## References

- [Dify tool plugin guide](https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/tool-plugin)
- [bsqb on PyPI](https://pypi.org/project/bsqb/)
- [Brave Search operators](https://api-dashboard.search.brave.com/documentation/resources/search-operators)
