from typing import List
from typing_extensions import TypedDict

class ReWOO(TypedDict):
    task: str
    plan_string: str
    steps: List
    results: dict
    result: str