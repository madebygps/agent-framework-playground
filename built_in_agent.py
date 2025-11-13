from agent_framework import AgentRunUpdateEvent, ChatAgent, WorkflowBuilder
from agent_framework.azure import AzureOpenAIChatClient
from dotenv import load_dotenv
import os

load_dotenv()

chat_client = AzureOpenAIChatClient(
    api_key=os.getenv("AZURE_OPENAI_API_KEY_GPT5"),
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_GPT5"),
    deployment_name=os.getenv("AZURE_OPENAI_MODEL_DEPLOYMENT_NAME_GPT5"),
    api_version=os.getenv(
        "AZURE_OPENAI_ENDPOINT_VERSION_GPT5", "2025-04-01-preview"
    ),
)


writer_agent: ChatAgent = chat_client.create_agent(
    instructions="You are the best technical writer in the world.", 
    name="writer_agent")

reviewer_agent: ChatAgent = chat_client.create_agent(
    instructions="Review the content for grammar and spelling errors.", 
    name="reviewer_agent"
)

builder = WorkflowBuilder()

builder.set_start_executor(writer_agent)
builder.add_edge(writer_agent, reviewer_agent)
workflow = builder.build()


async def main():
    last_executor_id = None
    async for event in workflow.run_stream("Write a spicy tweet about AI agents."):
        if isinstance(event, AgentRunUpdateEvent):
            if event.executor_id != last_executor_id:
                if last_executor_id is not None:
                    print()
                print(f"{event.executor_id}:", end=" ", flush=True)
                last_executor_id = event.executor_id
            print(event.data, end="", flush=True)

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())