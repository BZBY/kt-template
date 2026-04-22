"""Example local custom tool.

This template demonstrates the full user-facing author surface for a tool:
- constructor kwargs from config
- class attrs such as needs_context / require_manual_read
- tool_name
- description
- execution_mode
- _execute
- optional get_full_documentation

Copy this file when you need a creature-local tool.

Config example in config.yaml:

    tools:
      - name: template_tool
        type: custom
        module: ./tools/example_tool.py
        class: ExampleTool
        greeting: "Hello from my tool"
        include_working_dir: true

Important note for this codebase:
- tool options are passed as normal constructor kwargs
- they are NOT nested under `options:` in YAML for tools
"""

from typing import Any

from kohakuterrarium.modules.tool.base import (
    BaseTool,
    ExecutionMode,
    ToolContext,
    ToolResult,
)


class ExampleTool(BaseTool):
    # Set this to True when your tool needs access to session, cwd, channels,
    # scratchpad, path guards, or other runtime context.
    needs_context = True

    # Set this to True if the tool should only be usable after the model reads
    # its full manual via the built-in info tool.
    require_manual_read = False

    def __init__(
        self,
        greeting: str = "Hello from ExampleTool",
        include_working_dir: bool = True,
    ):
        super().__init__()
        self.greeting = greeting
        self.include_working_dir = include_working_dir

    @property
    def tool_name(self) -> str:
        return "template_tool"

    @property
    def description(self) -> str:
        return "Example custom tool template with comments and ToolContext access"

    @property
    def execution_mode(self) -> ExecutionMode:
        # DIRECT = run now
        # BACKGROUND = run as a job and deliver later
        # STATEFUL = multi-turn / generator-like patterns
        return ExecutionMode.DIRECT

    async def _execute(
        self,
        args: dict[str, Any],
        *,
        context: ToolContext | None = None,
    ) -> ToolResult:
        target = str(args.get("target", "world"))
        excited = bool(args.get("excited", False))

        pieces = [f"{self.greeting}, {target}"]

        if self.include_working_dir and context is not None:
            pieces.append(f"working_dir={context.working_dir}")
            pieces.append(f"agent={context.agent_name}")
            pieces.append(f"tool_format={context.tool_format}")

        output = " | ".join(pieces)
        if excited:
            output += "!"

        return ToolResult(output=output)

    def get_full_documentation(self) -> str:
        return """# template_tool

Example arguments:
- target (string): who or what to greet
- excited (boolean): whether to end with an exclamation mark

This template shows the current custom-tool contract used by this project:
- subclass BaseTool
- implement tool_name, description, execution_mode
- implement async _execute(...)
- return ToolResult

Optional author controls:
- needs_context = True
- require_manual_read = True/False
"""
