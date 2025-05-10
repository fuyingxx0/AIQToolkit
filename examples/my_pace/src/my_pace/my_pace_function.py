import logging

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig
from aiq.data_models.component_ref import LLMRef
from aiq.builder.framework_enum import LLMFrameworkEnum
from my_pace.state_schema import MyPaceState
from langgraph.graph import StateGraph

from my_pace.agents.orchestrator import orchestrator_node

logger = logging.getLogger(__name__)


class MyPaceFunctionConfig(FunctionBaseConfig, name="my_pace"):
    """
    AIQ Toolkit function template. Please update the description.
    """
    # Add your custom configuration parameters here
    llm_name: LLMRef = Field(..., description="The LLM to use for the profiler agent")
    parameter: str = Field(default="default_value", description="Notional description for this parameter")


@register_function(config_type=MyPaceFunctionConfig)
async def my_pace_function(
    config: MyPaceFunctionConfig, builder: Builder
):

    graph = StateGraph(MyPaceState)
    
    graph.add_node("orchestrator", orchestrator_node)

    graph.set_entry_point("orchestrator")

    graph.set_finish_point("orchestrator")

    compiled_graph = graph.compile()

    # llm = await builder.get_llm(config.llm_name, wrapper_type=LLMFrameworkEnum.LANGCHAIN)
    async def _response_fn(input_message: str) -> str:
        # response = await llm.ainvoke(input_message)
        # output_message = f"Hello from my_pace workflow! You said: {input_message}, Output generated: {response}"
        init_state: MyPaceState = {
            "user_input": input_message,
            "current_step": 0,
            "plan": ["orchestrator"]
        }
        result = await compiled_graph.ainvoke(init_state)
        return f"result: {result}"
    try:
        yield FunctionInfo.create(single_fn=_response_fn)
    except GeneratorExit:
        print("Function exited early!")
    finally:
        print("Cleaning up my_pace workflow.")