"""Example package-scoped plugin.

This package version also demonstrates every user-facing hook on BasePlugin, so
people cloning the template can choose either the local or reusable pattern.

Because `kohaku.yaml` advertises this plugin, creatures can enable it with:

    plugins:
      - name: template_package_plugin
        options:
          note: "enabled"

Notes:
- plugin constructor kwargs live under `options:` in YAML
- plugins are ideal for guardrails, logging, metrics, or prompt/tool policy
- package plugins are especially useful when you want one policy shared by many agents
"""

from typing import Any

from kohakuterrarium.modules.plugin.base import (
    BasePlugin,
    PluginBlockError,
    PluginContext,
)


class TemplatePackagePlugin(BasePlugin):
    name = "template_package_plugin"
    priority = 50

    def __init__(self, note: str = "package plugin active", block_keyword: str = ""):
        self.note = note
        self.block_keyword = block_keyword
        self.context: PluginContext | None = None

    async def on_load(self, context: PluginContext) -> None:
        self.context = context
        context.set_state("note", self.note)

    async def on_unload(self) -> None:
        if self.context is not None:
            self.context.set_state("unloaded", True)

    async def pre_llm_call(
        self, messages: list[dict], **kwargs: Any
    ) -> list[dict] | None:
        return None

    async def post_llm_call(
        self,
        messages: list[dict],
        response: str,
        usage: dict,
        **kwargs: Any,
    ) -> None:
        if self.context is not None:
            self.context.set_state("last_usage", usage)

    async def pre_tool_execute(self, args: dict, **kwargs: Any) -> dict | None:
        tool_name = kwargs.get("tool_name", "")
        if tool_name == "bash" and self.block_keyword:
            command = str(args.get("command", ""))
            if self.block_keyword in command:
                raise PluginBlockError(
                    f"Blocked bash command because it contained: {self.block_keyword}"
                )
        return None

    async def post_tool_execute(self, result: Any, **kwargs: Any) -> Any | None:
        return None

    async def pre_subagent_run(self, task: str, **kwargs: Any) -> str | None:
        return None

    async def post_subagent_run(self, result: Any, **kwargs: Any) -> Any | None:
        return None

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
            self.context.set_state("compact_messages_removed", messages_removed)
