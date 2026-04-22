"""Example local custom input module.

This template demonstrates the full user-facing subclass surface of
BaseInputModule:
- __init__
- _on_start
- _on_stop
- get_input
- render_command_data

Copy this file when your creature should receive events from somewhere other
than the built-in CLI/TUI inputs.

Typical real uses:
- Discord / Slack / Telegram listeners
- queues or webhooks
- local files or sockets
- synthetic test event feeds

Config example:

    input:
      type: custom
      module: ./inputs/example_input.py
      class: ExampleInputModule
      source: template_input
      seed_messages:
        - "First message"
        - "Second message"
"""

import asyncio
from collections.abc import Iterable

from kohakuterrarium.core.events import TriggerEvent, create_user_input_event
from kohakuterrarium.modules.input.base import BaseInputModule
from kohakuterrarium.modules.user_command.base import UserCommandResult


class ExampleInputModule(BaseInputModule):
    def __init__(
        self,
        source: str = "template_input",
        seed_messages: Iterable[str] | None = None,
    ):
        super().__init__()
        self.source = source
        self.seed_messages = list(seed_messages or [])
        self._queue: asyncio.Queue[str | None] = asyncio.Queue()
        self._background_task: asyncio.Task | None = None

    async def _on_start(self) -> None:
        # Start any background listener, websocket, poller, or adapter here.
        # This template simply queues synthetic messages.
        self._background_task = asyncio.create_task(self._seed_queue())

    async def _seed_queue(self) -> None:
        for message in self.seed_messages:
            await self._queue.put(str(message))

        # `None` is the sentinel meaning "this input is exhausted".
        # If your real input is long-lived, do not enqueue the sentinel until the
        # external source truly ends.
        await self._queue.put(None)

    async def _on_stop(self) -> None:
        # Close sockets, cancel background tasks, or disconnect clients here.
        if self._background_task is not None:
            self._background_task.cancel()
            self._background_task = None

    async def get_input(self) -> TriggerEvent | None:
        # The runtime calls this repeatedly. Return a TriggerEvent when you have
        # one, or None when the input source is fully exhausted.
        item = await self._queue.get()
        if item is None:
            return None

        # Convert your external payload into a standard TriggerEvent.
        return create_user_input_event(item, source=self.source)

    async def render_command_data(
        self,
        result: UserCommandResult,
        command_name: str,
    ) -> UserCommandResult | None:
        # Optional hook for interactive slash-command payloads.
        # CLI/TUI/web inputs can override this to render custom UIs.
        # Returning None means "use the original command result as-is".
        return None
