"""Example package-scoped trigger.

This package version demonstrates the same author-facing subclass surface as
the local trigger template:
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
"""

import asyncio
from typing import Any

from kohakuterrarium.modules.trigger.base import BaseTrigger


class TemplatePackageTrigger(BaseTrigger):
    resumable = True
    universal = False
    setup_tool_name = "add_template_package_trigger"
    setup_description = "Install the package trigger"
    setup_param_schema = {
        "type": "object",
        "properties": {
            "interval": {"type": "number"},
            "message": {"type": "string"},
            "prompt": {"type": "string"},
        },
    }
    setup_full_doc = ""
    setup_require_manual_read = False

    def __init__(
        self,
        interval: float = 60.0,
        message: str = "package trigger fired",
        prompt: str | None = None,
    ):
        super().__init__(prompt=prompt)
        self.interval = float(interval)
        self.message = message

    async def _on_start(self) -> None:
        pass

    async def _on_stop(self) -> None:
        pass

    def _on_context_update(self, context: dict[str, Any]) -> None:
        return None

    async def wait_for_trigger(self):
        await asyncio.sleep(self.interval)
        return self._create_event(
            "package_trigger", self.message, {"interval": self.interval}
        )

    def to_resume_dict(self) -> dict:
        return {
            "interval": self.interval,
            "message": self.message,
            "prompt": self.prompt,
        }

    @classmethod
    def from_resume_dict(cls, data: dict[str, Any]) -> "TemplatePackageTrigger":
        return cls(**data)

    @classmethod
    def from_setup_args(cls, args: dict[str, Any]) -> "TemplatePackageTrigger":
        return cls.from_resume_dict(args)

    @classmethod
    def post_setup(cls, trigger: "TemplatePackageTrigger", context: Any) -> None:
        return None
