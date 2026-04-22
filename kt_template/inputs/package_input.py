"""Example package-scoped input module.

This package version demonstrates the same author-facing subclass surface as
the local input template:
- __init__
- _on_start
- _on_stop
- get_input
- render_command_data

Reference it explicitly in creature config:

    input:
      type: package
      module: kt_template.inputs.package_input
      class: TemplatePackageInput
      source: package_input
"""

import asyncio
from collections.abc import Iterable

from kohakuterrarium.core.events import TriggerEvent, create_user_input_event
from kohakuterrarium.modules.input.base import BaseInputModule
from kohakuterrarium.modules.user_command.base import UserCommandResult


class TemplatePackageInput(BaseInputModule):
    def __init__(
        self, source: str = "package_input", seed_messages: Iterable[str] | None = None
    ):
        super().__init__()
        self.source = source
        self.seed_messages = list(seed_messages or [])
        self._queue: asyncio.Queue[str | None] = asyncio.Queue()
        self._background_task: asyncio.Task | None = None

    async def _on_start(self) -> None:
        self._background_task = asyncio.create_task(self._seed_queue())

    async def _seed_queue(self) -> None:
        for message in self.seed_messages:
            await self._queue.put(str(message))
        await self._queue.put(None)

    async def _on_stop(self) -> None:
        if self._background_task is not None:
            self._background_task.cancel()
            self._background_task = None

    async def get_input(self) -> TriggerEvent | None:
        item = await self._queue.get()
        if item is None:
            return None
        return create_user_input_event(item, source=self.source)

    async def render_command_data(
        self,
        result: UserCommandResult,
        command_name: str,
    ) -> UserCommandResult | None:
        return None
