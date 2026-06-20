from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.brave_search import BraveSearchTool


class BsqbProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            for _ in BraveSearchTool.from_credentials(credentials, user_id="").invoke(
                tool_parameters={"query": "bsqb", "count": 1},
            ):
                pass
        except Exception as exc:
            raise ToolProviderCredentialValidationError(str(exc)) from exc
