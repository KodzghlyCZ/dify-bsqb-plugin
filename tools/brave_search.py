import json
from collections.abc import Generator
from typing import Any

import requests
from bsqb import EmptyQueryError, QueryValidationError
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.query_builder import build_query_from_parameters

BRAVE_DEFAULT_URL = "https://api.search.brave.com/res/v1/web/search"


class BraveSearchTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        try:
            built_query = build_query_from_parameters(tool_parameters)
        except EmptyQueryError as exc:
            yield self.create_text_message(str(exc))
            return
        except QueryValidationError as exc:
            yield self.create_text_message(f"Query validation failed: {exc}")
            return

        api_key = self.runtime.credentials["brave_search_api_key"]
        base_url = self.runtime.credentials.get("base_url") or BRAVE_DEFAULT_URL
        if not str(base_url).strip():
            base_url = BRAVE_DEFAULT_URL

        count = tool_parameters.get("count", 5)
        try:
            count = max(1, min(int(count), 20))
        except (TypeError, ValueError):
            count = 5

        ensure_ascii = tool_parameters.get("ensure_ascii", True)
        if isinstance(ensure_ascii, str):
            ensure_ascii = ensure_ascii.strip().lower() not in {"false", "0", "no", "off"}

        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": api_key,
        }
        params = {
            "q": built_query,
            "count": count,
            "operators": "true",
        }

        response = requests.get(base_url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        results = response.json().get("web", {}).get("results", [])
        payload = [
            {
                "title": item.get("title"),
                "link": item.get("url"),
                "snippet": item.get("description"),
            }
            for item in results
        ]

        message = {
            "query": built_query,
            "count": count,
            "results": payload,
        }
        yield self.create_json_message(message)

        if not payload:
            yield self.create_text_message(f"No results found for query: {built_query}")
            return

        yield self.create_text_message(json.dumps(message, ensure_ascii=ensure_ascii))
