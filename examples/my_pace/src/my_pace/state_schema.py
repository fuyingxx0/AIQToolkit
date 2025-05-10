from typing import TypedDict, Literal, Optional

class MyPaceState(TypedDict):
    user_input: str
    current_step: int
    plan: list[str]