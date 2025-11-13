from typing import Never
from agent_framework import (
    WorkflowBuilder,
    WorkflowContext,
    executor,
    ExecutorCompletedEvent,
    ExecutorInvokedEvent,
    WorkflowOutputEvent,
    WorkflowError,
)
import asyncio


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

    builder = WorkflowBuilder()
    builder.set_start_executor(splitter_executor)
    builder.add_fan_out_edges(splitter_executor, [summarizer, sentiment_detector, keyword_finder])
    workflow = builder.build()

    async for event in workflow.run_stream('data to work with'):
        match event:
            case ExecutorInvokedEvent() as invoke:
                print(f"Starting {invoke.executor_id}")
            case ExecutorCompletedEvent() as complete:
                print(f"Completed {complete.executor_id}: {complete.data}")
            case WorkflowOutputEvent() as output:
                print(f"Workflow produced output: {output.data}")
                return
            case WorkflowErrorEvent() as error:
                print(f"Workflow error: {error.exception}")
                return


if __name__ == "__main__":
    asyncio.run(main())
