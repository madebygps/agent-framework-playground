# agent-framework-playground

Learning playground for Microsoft Agent Framework (MAF) - exploring workflow concepts with practical examples.

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

## Installation

```bash
uv sync
```

## Examples

### Direct Edges (`direct_edge.py`)
Demonstrates direct workflow connections between executors. Shows how to chain operations that always execute in sequence.

**Example**: Converts text to uppercase (`hola mundo` → `HLA MNDÖ`), then removes vowels.

Based on: [Direct Edges documentation](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/core-concepts/edges?pivots=programming-language-python#direct-edges)

```bash
uv run direct_edge.py
```

### Conditional Edges (`conditional_edge.py`)
Demonstrates conditional routing in workflows. Shows how to branch execution based on runtime conditions.

**Example**: Email spam detector that routes messages to different handlers based on spam keyword detection.

Based on: [Conditional Edges documentation](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/core-concepts/edges?pivots=programming-language-python#conditional-edges)

```bash
uv run conditional_edge.py
```

## Resources

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/)
