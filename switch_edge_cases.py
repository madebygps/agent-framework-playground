from enum import Enum, IntEnum
from typing import Never
from agent_framework import (
    Case,
    Default,
    WorkflowBuilder,
    WorkflowContext,
    Executor,
    handler
)

import asyncio

class Priority(IntEnum):
    LOW = 1
    NORMAL = 5
    HIGH = 10
    

class TextMessage:

    def __init__(self, priority: Priority, content: str):
        self.priority = priority
        self.content = content


class RouterExecutor(Executor):

    def __init__(self, id: str):
        super().__init__(id=id)
    
    @handler
    async def route_message(self, text_message: TextMessage, ctx: WorkflowContext[TextMessage]) -> None:
        await ctx.send_message(text_message)

class ExecutorA(Executor):

    def __init__(self, id: str):
        super().__init__(id=id)
    
    @handler
    async def route_low_priority(self, text_message: TextMessage, ctx: WorkflowContext[Never, str]) -> None:
        await ctx.yield_output("Low priority message archived")

class ExecutorB(Executor):

    def __init__(self, id: str):
        super().__init__(id=id)
    
    @handler
    async def route_low_priority(self, text_message: TextMessage, ctx: WorkflowContext[Never, str]) -> None:
        await ctx.yield_output("Normal priority message sent to read later")

class ExecutorC(Executor):

    def __init__(self, id: str):
        super().__init__(id=id)
    
    @handler
    async def route_low_priority(self, text_message: TextMessage, ctx: WorkflowContext[Never, str]) -> None:
        await ctx.yield_output("High priority message sent to owner")



async def main():

    router_executor = RouterExecutor(id="router_executor")
    executor_a = ExecutorA(id="executor_a")
    executor_b = ExecutorB(id="executor_b")
    executor_c = ExecutorC(id="executor_c")

    builder = WorkflowBuilder()
    builder.set_start_executor(router_executor)
    builder.add_switch_case_edge_group(
        router_executor,
        [
            Case(
                condition=lambda message: message.priority < Priority.NORMAL,
                target=executor_a,
            ),
            Case(
                condition=lambda message: message.priority < Priority.HIGH,
                target=executor_b,
            ),
            Default(target=executor_c)
        ],
    )
    workflow = builder.build()
    text_message = TextMessage(priority=Priority.NORMAL, content="What's for dinner?")
    events = await workflow.run(text_message)
    print(events.get_outputs())


if __name__ == "__main__":
    asyncio.run(main())
