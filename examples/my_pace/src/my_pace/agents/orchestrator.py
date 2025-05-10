from my_pace.state_schema import MyPaceState

async def orchestrator_node(state: MyPaceState) -> dict:
    plan = state.get("plan", [])
    idx = state.get("current_step", 0)
    if idx >= len(plan): return {"current_step": idx, "__next__": "__end__"}
    return {
        "current_step": idx + 1,
        "__next__": plan[idx]
    }
