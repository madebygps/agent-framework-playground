from enum import IntEnum
from typing import Never
from agent_framework import (
    WorkflowBuilder,
    WorkflowContext,
    executor,
)
import asyncio


class Priority(IntEnum):
    LOW = 1
    NORMAL = 5
    HIGH = 10


@executor
async def splitter_executor(work_message: str, ctx: WorkflowContext[str]) -> None:
    await ctx.send_message(work_message)


@executor(id="summarizer")
async def summarizer(work_message: str, ctx: WorkflowContext[Never, str]) -> None:
    await ctx.yield_output(f'worker 1 summarized: {work_message}')


@executor(id="sentiment_detector")
async def sentiment_detector(work_message: str, ctx: WorkflowContext[Never, str]) -> None:
    await ctx.yield_output(f'worker 2 detected sentiment: {work_message}')  


@executor(id="keyword_finder")
async def keyword_finder(work_message: str, ctx: WorkflowContext[Never,str]) -> None:
    await ctx.yield_output(f'worker 3 found keywords: {work_message}')  



async def main():


    # Send to specific targets based on partitioner function
    builder = WorkflowBuilder()
    builder.set_start_executor(splitter_executor)
    builder.add_fan_out_edges(
        splitter_executor,
        [summarizer, sentiment_detector, keyword_finder],
        selection_func=lambda message, target_ids: (
            [0, 1, 2] if len(message) > 5 else
            [1, 2] if message.priority == Priority.NORMAL else
            list(range(len(target_ids)))
        )
    )
    workflow = builder.build()

if __name__ == "__main__":
    asyncio.run(main())