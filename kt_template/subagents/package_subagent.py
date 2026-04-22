"""Example package-scoped sub-agent config export.

This package version demonstrates the same author-facing surface as the local
sub-agent template.

Unlike tools, sub-agents in this codebase are usually exported as config
objects, not implemented as subclasses.
"""

from kohakuterrarium.modules.subagent.config import (
    ContextUpdateMode,
    OutputTarget,
    SubAgentConfig,
)

TEMPLATE_PACKAGE_SUBAGENT_CONFIG = SubAgentConfig(
    name="template_package_subagent",
    description="Example package sub-agent config",
    tools=["read", "glob", "grep"],
    system_prompt="You are a focused package sub-agent. Return concise findings.",
    can_modify=False,
    stateless=True,
    interactive=False,
    context_mode=ContextUpdateMode.INTERRUPT_RESTART,
    output_to=OutputTarget.CONTROLLER,
    output_module=None,
    return_as_context=True,
    max_turns=2,
    timeout=60,
    model=None,
    temperature=None,
    memory_path=None,
    modifying_tools=None,
    tool_format=None,
    notify_controller_on_background_complete=True,
    extra={"notes": "Package-scoped sub-agent template"},
)
