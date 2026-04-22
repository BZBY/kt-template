"""Example local custom sub-agent config.

This template demonstrates the full user-facing author surface for a
SubAgentConfig export.

In this project, custom sub-agents are usually exported as SubAgentConfig
objects rather than implemented as subclasses.

Config example:

    subagents:
      - name: example_subagent
        type: custom
        module: ./subagents/example_subagent.py
        config: EXAMPLE_SUBAGENT_CONFIG
"""

from kohakuterrarium.modules.subagent.config import (
    ContextUpdateMode,
    OutputTarget,
    SubAgentConfig,
)

EXAMPLE_SUBAGENT_CONFIG = SubAgentConfig(
    # Public name used by the parent creature.
    name="example_subagent",
    # One-line description shown to the parent controller.
    description="Example custom sub-agent template for narrow analysis tasks",
    # Restrict the sub-agent to only the tools it actually needs.
    tools=["read", "glob", "grep"],
    # Prompt sources. You can use inline system_prompt, prompt_file, extra_prompt,
    # or extra_prompt_file depending on how much structure you want.
    prompt_file="prompts/subagent_system.md",
    extra_prompt=(
        "Return concise findings. Quote concrete evidence when possible. "
        "Do not edit files."
    ),
    # Whether the sub-agent is allowed to modify files.
    can_modify=False,
    # Stateless means each invocation starts fresh.
    stateless=True,
    # Interactive sub-agents stay alive across parent updates.
    interactive=False,
    context_mode=ContextUpdateMode.INTERRUPT_RESTART,
    # Where the output goes.
    output_to=OutputTarget.CONTROLLER,
    output_module=None,
    # If True, text output is fed back into the parent as context.
    return_as_context=True,
    # Optional execution limits.
    max_turns=2,
    timeout=90,
    # Model overrides. Leave as None to inherit from the parent creature.
    model=None,
    temperature=None,
    # Optional memory path for sub-agents that operate on a dedicated folder.
    memory_path=None,
    # Restrict file-modifying tools even further if can_modify=True.
    modifying_tools=None,
    # Override tool format only if this sub-agent needs something different.
    tool_format=None,
    # Whether background completion should wake the parent controller.
    notify_controller_on_background_complete=True,
    # Freeform extra config for your own conventions.
    extra={
        "notes": "Put project-specific sub-agent metadata here if you want.",
    },
)
