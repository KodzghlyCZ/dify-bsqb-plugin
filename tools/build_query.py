from collections.abc import Generator
from typing import Any

from bsqb import EmptyQueryError, QueryValidationError
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from tools.query_builder import build_query_from_parameters


class BuildQueryTool(Tool):
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

        yield self.create_json_message(
            {
                "query": built_query,
                "operators_enabled": True,
            }
        )
