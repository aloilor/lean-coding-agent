# Object-Oriented Programming

This folder collects reusable object-oriented programming best practices, with a strong focus on SOLID and a few complementary design principles that help OOP stay maintainable in real codebases.

## Sources

- Robert C. Martin, [The Single Responsibility Principle](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html)
- Robert C. Martin, [The Open Closed Principle](https://blog.cleancoder.com/uncle-bob/2014/05/12/TheOpenClosedPrinciple.html)
- Robert C. Martin, [Solid Relevance](https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html)
- Robert C. Martin, [A Little Architecture](https://blog.cleancoder.com/uncle-bob/2016/01/04/ALittleArchitecture.html)
- Barbara Liskov and Jeannette Wing, [A Behavioral Notion of Subtyping](https://www.cs.cmu.edu/afs/cs/project/venari/www/subtype-toplas.html)
- Joshua Bloch, [You should favor composition over inheritance in Java. Here's why.](https://blogs.oracle.com/content/published/api/v1.1/assets/CONT2E5A3210DD844F7893E5193CD3DB0D83/native/You%2Bshould%2Bfavor%2Bcomposition%2Bover%2Binheritance%2Bin%2BJava.%2BHere%E2%80%99s%2Bwhy_.pdf?cb=_cache_c90d&channelToken=4d6a6a00a153413e9a7a992032379dbf)
- Martin Fowler, [Tell Don't Ask](https://martinfowler.com/bliki/TellDontAsk.html)
- Karl Lieberherr, Ian Holland, and Arthur Riel, [Object-Oriented Programming: An Objective Sense of Style](https://www2.ccs.neu.edu/research/demeter/papers/law-of-demeter/oopsla88-law-of-demeter.pdf)
- Oracle, [The Java Language Environment: Object-Oriented Programming](https://www.oracle.com/java/technologies/object-oriented.html)

## Contents

- [SOLID](./solid.md): how to apply SRP, OCP, LSP, ISP, and DIP without turning them into dogma.
- [Composition And Encapsulation](./composition-and-encapsulation.md): when to favor composition, how to hide internals, and how to keep abstractions stable.

## Core Rules

- Keep responsibilities separated by reason to change, not by arbitrary class size.
- Extend behavior through abstractions and composition before reaching for inheritance.
- Treat subtype contracts as behavioral contracts, not only type signatures.
- Keep interfaces small and dependencies pointing toward abstractions.
- Let objects own behavior close to their data instead of leaking internal structure.
