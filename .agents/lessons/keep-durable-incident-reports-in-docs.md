# Keep Durable Incident Reports In Docs

## Mistake Pattern

I put incident reports under `.agents/`, which made them look like local agent handoff artifacts instead of durable project records.

## Rule

Store durable incident reports under `docs/incidents/` unless the project defines a different committed documentation location. Keep transient diagnosis and handoff artifacts under `.agents/`.
