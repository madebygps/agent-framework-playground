from agent_framework import (
    ExecutorCompleteEvent,
    ExecutorInvokeEvent,
    WorkflowOutputEvent,
    WorkflowErrorEvent,
)

def main():
    workflow = ConcurrentBuilder().participants([researcher, marketer, legal]).build()
    completion: WorkflowCompletedEvent