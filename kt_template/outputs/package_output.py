"""Example package-scoped output module.

This package version demonstrates the same author-facing subclass surface as
the local output template:
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
"""

from pathlib import Path

from kohakuterrarium.modules.output.base import BaseOutputModule


class TemplatePackageOutput(BaseOutputModule):
    def __init__(self, path: str = "./package-output.log"):
        super().__init__()
        self.path = Path(path)
        self._stream_buffer: list[str] = []

    async def _on_start(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

    async def _on_stop(self) -> None:
        pass

    async def write(self, content: str) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(content + "\n")

    async def write_stream(self, chunk: str) -> None:
        self._stream_buffer.append(chunk)

    async def flush(self) -> None:
        if not self._stream_buffer:
            return
        await self.write("".join(self._stream_buffer))
        self._stream_buffer.clear()

    async def on_processing_start(self) -> None:
        pass

    async def on_processing_end(self) -> None:
        await self.flush()

    def on_activity(self, activity_type: str, detail: str) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"activity={activity_type} detail={detail}\n")

    async def on_user_input(self, text: str) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"user_input={text}\n")

    async def on_resume(self, events: list[dict]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(f"resumed_events={len(events)}\n")
