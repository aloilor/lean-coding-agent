# Mirror Project Operating Files Across Supported Tools

## Mistake Pattern

I added support for another agent tool but left shared agent memory or repo-local tool files in a layout that made one tool see different operating context than another.

## Rule

When this repo supports multiple agent tools, keep shared agent memory in tool-neutral locations like `.agents/lessons/`, and keep tool-specific files mirrored only where each tool requires its own copy.
