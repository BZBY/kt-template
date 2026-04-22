"""Example local custom output module.

This template demonstrates the full user-facing subclass surface of
BaseOutputModule:
- __init__
- _on_start
- _on_stop
- write
- write_stream
- flush
- on_processing_start
- on_processing_end
- on_activity
- on_user_input
- on_resume

Copy this file when your creature should deliver output somewhere other than
stdout or the built-in TUI output.

Typical real uses:
- Discord webhooks
- chat APIs
- files or audit logs
- text-to-speech backends
- dashboards or message buses

Config example:

    output:
      type: custom
      module: ./outputs/example_output.py
      class: ExampleOutputModule
      path: ./output.log
      prefix: "[my-output]"
"""

from pathlib import Path

from kohakuterrarium.modules.output.base import BaseOutputModule


class ExampleOutputModule(BaseOutputModule):
    def __init__(self, path: str = "./output.log", prefix: str = "[output]"):
        super().__init__()
        self.path = Path(path)
        self.prefix = prefix
        self._stream_buffer: list[str] = []

    async def _on_start(self) -> None:
        # Prepare files, HTTP clients, sockets, or SDK clients here.
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"{self.prefix} started\n")

    async def _on_stop(self) -> None:
        # Close network clients or external handles here.
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"{self.prefix} stopped\n")

    async def write(self, content: str) -> None:
        # `write` receives a complete message.
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"{self.prefix} {content}\n")

    async def write_stream(self, chunk: str) -> None:
        # Streaming output arrives in chunks while the model is still speaking.
        self._stream_buffer.append(chunk)

    async def flush(self) -> None:
        # Flush any buffered streaming chunks.
        if not self._stream_buffer:
            return
        await self.write("".join(self._stream_buffer))
        self._stream_buffer.clear()

    async def on_processing_start(self) -> None:
        # Called before the model starts generating.
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"{self.prefix} processing_start\n")

    async def on_processing_end(self) -> None:
        # Good place to flush streaming buffers.
        await self.flush()
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"{self.prefix} processing_end\n")

    def on_activity(self, activity_type: str, detail: str) -> None:
        # Activity callbacks are synchronous in this API.
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"{self.prefix} activity={activity_type} detail={detail}\n")

    async def on_user_input(self, text: str) -> None:
        # Called when user input arrives before processing starts.
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"{self.prefix} user_input={text}\n")

    async def on_resume(self, events: list[dict]) -> None:
        # Called during session resume with historical events.
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"{self.prefix} resumed_events={len(events)}\n")
