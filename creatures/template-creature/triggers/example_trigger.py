"""Example local custom trigger.

This template demonstrates the full user-facing subclass surface of BaseTrigger:
- class attrs such as resumable / universal
- __init__
- _on_start
- _on_stop
- _on_context_update
- wait_for_trigger
- to_resume_dict
- from_resume_dict
- from_setup_args
- post_setup

Copy this file when your creature should wake up on its own.

Typical real uses:
- polling an external system
- waiting for a socket or webhook signal
- a domain-specific scheduler
- context-sensitive checks that do not come from user input

Config example:

    triggers:
      - type: custom
        module: ./triggers/example_trigger.py
        class: ExampleTrigger
        interval: 60
        message: "Custom trigger fired"
        prompt: "Handle the trigger event"
"""

import asyncio
from typing import Any

from kohakuterrarium.core.events import TriggerEvent
from kohakuterrarium.modules.trigger.base import BaseTrigger


class ExampleTrigger(BaseTrigger):
    # Set resumable=True if you want the trigger persisted in sessions.
    resumable = True

    # Set universal=True and fill the setup metadata below if you want this
    # trigger to be installable by the agent at runtime via `type: trigger`.
    universal = False
    setup_tool_name = "add_example_trigger"
    setup_description = "Install the example trigger"
    setup_param_schema = {
        "type": "object",
        "properties": {
            "interval": {"type": "number"},
            "message": {"type": "string"},
            "prompt": {"type": "string"},
            "immediate": {"type": "boolean"},
        },
    }
    setup_full_doc = ""
    setup_require_manual_read = False

    def __init__(
        self,
        interval: float = 60.0,
        message: str = "Example trigger fired.",
        prompt: str | None = None,
        immediate: bool = False,
    ):
        super().__init__(prompt=prompt)
        self.interval = float(interval)
        self.message = message
        self.immediate = immediate
        self._first_fire = True

    async def _on_start(self) -> None:
        # Open subscriptions or allocate resources here.
        pass

    async def _on_stop(self) -> None:
        # Tear down any external resources here.
        pass

    def _on_context_update(self, context: dict[str, Any]) -> None:
        # Context triggers can react to runtime state changes here.
        # This template just keeps the default stored context.
        return None

    async def wait_for_trigger(self) -> TriggerEvent | None:
        if not self.is_running:
            return None

        if self.immediate and self._first_fire:
            self._first_fire = False
        else:
            await asyncio.sleep(self.interval)

        return self._create_event(
            event_type="example_trigger",
            content=self.message,
            context={"interval": self.interval},
        )

    def to_resume_dict(self) -> dict:
        return {
            "interval": self.interval,
            "message": self.message,
            "prompt": self.prompt,
            "immediate": self.immediate,
        }

    @classmethod
    def from_resume_dict(cls, data: dict[str, Any]) -> "ExampleTrigger":
        return cls(**data)

    @classmethod
    def from_setup_args(cls, args: dict[str, Any]) -> "ExampleTrigger":
        # Override this when the setup-tool args differ from the resume payload.
        return cls.from_resume_dict(args)

    @classmethod
    def post_setup(cls, trigger: "ExampleTrigger", context: Any) -> None:
        # Override when a runtime-installed trigger needs agent-derived state.
        return None
