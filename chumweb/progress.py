"""
Simple package to show generation progress
"""

ESC = "\x1B"
SGR_FG_BLUE = f"{ESC}[34m"
SGR_RESET = f"{ESC}[0m"

_current_step_name: str | None = None

StepHandle = int
_current_step: StepHandle = 1


def begin_step(step_name: str) -> StepHandle:
    global _current_step_name, _current_step
    step = _current_step
    if _current_step_name != step_name:
        _current_step_name = step_name
        _print_step(step_name)
        step += 1
        _current_step = step

    return step


def step_progress(step: StepHandle, subtask_name: str, progress: int, total: int):
    if _current_step == step:
        _print_step_progress(subtask_name, progress, total)


def _print_step(step_name: str) -> None:
    print(f"{SGR_FG_BLUE}::{SGR_RESET} {step_name}")


def _print_step_progress(subtask_name: str, progress: int, total: int):
    print(f" - ({progress}/{total}) {subtask_name}")
