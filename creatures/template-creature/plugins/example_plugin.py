"""Example local lifecycle plugin.

This template demonstrates every user-facing hook on BasePlugin.
Copy it when you want to observe or intercept the seams between the
controller, tools, and sub-agents.

Config example:

    plugins:
      - name: example_plugin
        type: custom
        module: ./plugins/example_plugin.py
        class: ExamplePlugin
        options:
          note: "template plugin active"
          block_keyword: "rm -rf"

Important note for this codebase:
- plugin constructor args live under `options:` in YAML
- plugins are the odd one out; most other custom module types use inline fields
"""

from typing import Any

from kohakuterrarium.modules.plugin.base import (
    BasePlugin,
    PluginBlockError,
    PluginContext,
)


class ExamplePlugin(BasePlugin):
    # Public plugin name used in config and runtime management.
    name = "example_plugin"

    # Lower priority runs earlier in pre_* hooks and later in post_* hooks.
    priority = 50

    def __init__(
        self,
        note: str = "template plugin",
        block_keyword: str = "",
    ):
        self.note = note
        self.block_keyword = block_keyword
        self.context: PluginContext | None = None

    # ── Lifecycle ──────────────────────────────────────────────────────

    async def on_load(self, context: PluginContext) -> None:
        # Called once when the plugin is loaded.
        self.context = context
        context.set_state("note", self.note)
        context.set_state("loaded", True)

    async def on_unload(self) -> None:
        # Called when the agent shuts down and the plugin is being unloaded.
        if self.context is not None:
            self.context.set_state("loaded", False)

    # ── LLM hooks ───────────────────────────────────────────────────────

    async def pre_llm_call(
        self, messages: list[dict], **kwargs: Any
    ) -> list[dict] | None:
        # Return a modified messages list to rewrite the prompt, or None to keep
        # the original unchanged.
        if self.context is not None:
            self.context.set_state("last_model", kwargs.get("model", ""))
        return None

    async def post_llm_call(
        self,
        messages: list[dict],
        response: str,
        usage: dict,
        **kwargs: Any,
    ) -> None:
        # Observation-only hook after the model returns.
        if self.context is not None:
            self.context.set_state("last_response_preview", response[:120])
            self.context.set_state("last_usage", usage)

    # ── Tool hooks ──────────────────────────────────────────────────────

    async def pre_tool_execute(self, args: dict, **kwargs: Any) -> dict | None:
        # Return modified args to rewrite the tool call.
        # Raise PluginBlockError to prevent execution.
        tool_name = kwargs.get("tool_name", "")
        if tool_name == "bash" and self.block_keyword:
            command = str(args.get("command", ""))
            if self.block_keyword in command:
                raise PluginBlockError(
                    f"Blocked bash command because it contained: {self.block_keyword}"
                )
        return None

    async def post_tool_execute(self, result: Any, **kwargs: Any) -> Any | None:
        # Return a replacement result if you want to transform tool output.
        if self.context is not None:
            self.context.set_state("last_tool_name", kwargs.get("tool_name", ""))
        return None

    # ── Sub-agent hooks ────────────────────────────────────────────────

    async def pre_subagent_run(self, task: str, **kwargs: Any) -> str | None:
        # Return a modified task string to rewrite the sub-agent prompt.
        # Raise PluginBlockError to block the sub-agent call.
        if self.context is not None:
            self.context.set_state("last_subagent", kwargs.get("name", ""))
        return None

    async def post_subagent_run(self, result: Any, **kwargs: Any) -> Any | None:
        # Return a replacement result if you want to transform it.
        return None

    # ── Fire-and-forget callbacks ──────────────────────────────────────

    async def on_agent_start(self) -> None:
        if self.context is not None:
            self.context.set_state("agent_running", True)

    async def on_agent_stop(self) -> None:
        if self.context is not None:
            self.context.set_state("agent_running", False)

    async def on_event(self, event: Any) -> None:
        if self.context is not None:
            self.context.set_state("last_event_type", getattr(event, "type", "unknown"))

    async def on_interrupt(self) -> None:
        if self.context is not None:
            self.context.set_state("interrupted", True)

    async def on_task_promoted(self, job_id: str, tool_name: str) -> None:
        if self.context is not None:
            self.context.set_state("last_promoted_job", job_id)
            self.context.set_state("last_promoted_tool", tool_name)

    async def on_compact_start(self, context_length: int) -> None:
        if self.context is not None:
            self.context.set_state("compact_start_context_length", context_length)

    async def on_compact_end(self, summary: str, messages_removed: int) -> None:
        if self.context is not None:
            self.context.set_state("compact_summary_preview", summary[:120])
            self.context.set_state("compact_messages_removed", messages_removed)
