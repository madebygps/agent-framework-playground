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

- **Direct Edges** (`direct_edge.py`) - Chain operations that always execute in sequence. [Documentation](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/core-concepts/edges?pivots=programming-language-python#direct-edges)

- **Conditional Edges** (`conditional_edge.py`) - Branch execution based on runtime conditions. [Documentation](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/core-concepts/edges?pivots=programming-language-python#conditional-edges)

- **Switch-Case Edges** (`switch_edge_cases.py`) - Multi-way branching with case conditions and default fallback. [Documentation](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/core-concepts/edges?pivots=programming-language-python#switch-case-edges)

- **Fan-Out Edges (Broadcast)** (`fan_out_edges_all.py`) - Distribute messages to multiple executors in parallel, where all targets receive every message. [Documentation](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/core-concepts/edges?pivots=programming-language-python#fan-out-edges)

- **Fan-Out Edges (Selective)** (`fan_out_edges_selective.py`) - Selectively route messages to specific executors based on custom logic using `selection_func`. *Note: Requires a newer library version than currently published (>1.0.0b251028).* [Documentation](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/core-concepts/edges?pivots=programming-language-python#fan-out-edges)

## Resources

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/)
