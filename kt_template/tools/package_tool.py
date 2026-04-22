"""Example package-scoped tool.

This package version demonstrates the same author-facing surface as the local
tool template:
- constructor kwargs from config
- class attrs such as needs_context / require_manual_read
- tool_name
- description
- execution_mode
- _execute
- optional get_full_documentation

Because `kohaku.yaml` advertises this tool, creatures can enable it with:

    tools:
      - name: template_package_tool
        type: package
"""

from typing import Any

from kohakuterrarium.modules.tool.base import (
    BaseTool,
    ExecutionMode,
    ToolContext,
    ToolResult,
)


class TemplatePackageTool(BaseTool):
    needs_context = True
    require_manual_read = False

    def __init__(self, label: str = "template package tool"):
        super().__init__()
        self.label = label

    @property
    def tool_name(self) -> str:
        return "template_package_tool"

    @property
    def description(self) -> str:
        return "Example package tool shipped by kt-template"

    @property
    def execution_mode(self) -> ExecutionMode:
        return ExecutionMode.DIRECT

    async def _execute(
        self,
        args: dict[str, Any],
        *,
        context: ToolContext | None = None,
    ) -> ToolResult:
        subject = str(args.get("subject", "world"))
        pieces = [f"{self.label}: hello, {subject}"]
        if context is not None:
            pieces.append(f"agent={context.agent_name}")
        return ToolResult(output=" | ".join(pieces))

    def get_full_documentation(self) -> str:
        return """# template_package_tool

Package-scoped custom tool example.

Example arguments:
- subject (string): target of the greeting
"""
