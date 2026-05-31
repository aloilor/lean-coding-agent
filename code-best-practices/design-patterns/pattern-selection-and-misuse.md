# Pattern Selection And Misuse

## Start With The Problem, Not The Pattern Name

- Do not begin with "I want to use Strategy" or "I need a Factory".
- Begin with the design problem: too many conditionals, creation logic spread everywhere, tight coupling to vendor code, or hard-to-extend behavior.
- Choose a pattern only if it clearly improves that problem.

## Prefer Small Honest Designs

- A named pattern is not automatically better than a plain function or small class.
- If a simple design is already readable and stable, do not wrap it in pattern language.
- Many good designs use the idea behind a pattern without needing formal ceremony.

## Watch For Pattern Smells

- Too many interfaces with one implementation
- Factories for trivial constructors
- Strategy classes that could be small functions
- Event systems where control flow becomes impossible to follow
- Inheritance used only to bolt on side behavior

## Refactor Into Patterns, Do Not Force Them Early

- Patterns are often best introduced after a problem becomes visible.
- Let duplication, branching, or coupling show you where a pattern helps.
- It is usually safer to refactor toward a pattern than to predict one too early.

## Practical Checks

- What exact pain does this pattern remove?
- Will the code be easier to read for the next engineer?
- If I removed the pattern name, would the design still make sense?
- Am I introducing ceremony faster than the code is earning it?
