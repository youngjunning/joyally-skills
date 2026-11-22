# Progressive architecture

Use this branch when the architecture will evolve through several decisions, implementation slices, or sessions. Its purpose is to preserve the decision state that changes future work without turning the project into a documentation system.

## Keep state by meaning

Use the project's existing artifacts when they can carry the state. Add a dedicated map or graph only when the number of interacting decisions makes prose unreliable.

- **Intent:** the outcome and current scope, not a component wishlist.
- **Verified reality:** source, runtime, user, policy, hardware, cost, or integration facts with evidence and date where freshness matters.
- **Decision:** the chosen behavior or boundary, its owner, contract, reason, and reversal trigger.
- **Unresolved choice:** a decision that blocks or materially changes the next slice. Record the tradeoff and the evidence that would resolve it.
- **Deferred idea:** useful but outside the active path. Keep its intended value and activation condition so it does not silently expand scope.
- **Rejected path:** what was tried or considered, why it failed, and what new evidence would justify reopening it.
- **Implementation and acceptance:** what exists, which version or entrypoint carries it, and what has actually been verified. Do not let a design decision imply implementation or let a passing test imply adoption.

Do not mix current reality with target architecture in one unlabeled diagram. A stale graph is worse than a small current record; remove or update state that no longer governs decisions.

## Advance one useful slice

1. Start from the current outcome and the smallest local slice that contains its actor, trigger, accepted result, owning boundaries, contracts, and material failure path.
2. Identify the unresolved choice most likely to change that slice. Offer two or more credible options only while the choice is open; do not force a false binary when the user's direction is already fixed or a reversible experiment is cheaper.
3. State the value bought and cost introduced by each option. Resolve the choice from evidence, or define the smallest test and its pass/change/stop condition.
4. Update the architecture state before implementation when the decision changes contracts or ownership. Keep unrelated unknowns explicit instead of solving the whole graph.
5. Deliver a walking skeleton as soon as one end-to-end path can produce an accepted result. It may use manual or temporary internals, but the user-visible outcome, boundary contracts, and evidence path must be real.
6. Feed implementation and runtime findings back into verified reality, decisions, rejected paths, and acceptance state. Do not preserve a decision merely because code already exists.

## Control scale

Focus on the current node or responsibility and its immediate upstream and downstream contracts. Expand the slice only when a shared invariant, cross-cutting resource, or likely change crosses that boundary.

Fold a mature, cohesive group into one named capability when its internal decisions are stable and callers can rely on a narrow contract. Unfold it when a changed requirement or failure crosses the contract. Folding is a view operation, not a license to hide unresolved risk or erase traceability.

Keep the main delivery path visible. Deferred ideas remain discoverable but do not compete with active work. Rejected paths retain only the lesson needed to avoid repeating them; raw debugging logs and temporary artifacts stay in their proper project locations.

## Choose the lightest representation

- A short conversation or reversible local edit needs no persistent architecture state.
- A durable decision can use the project's ADR or decision memo.
- A multi-stage feature can use a compact table of responsibilities, contracts, unknowns, and evidence.
- A system with many interacting nodes, active and deferred branches, or repeated context loss may justify a versioned graph and a generated local view.

Any new representation needs a maintainer, update trigger, and clear relation to source and runtime facts. Prefer generated views over duplicate hand-maintained diagrams.

## Completion

The current slice is ready to advance when its outcome, verified constraints, chosen boundaries, contracts, unresolved risks, implementation status, and acceptance evidence are distinguishable. The next decision or delivery action is explicit, and deferred or rejected work cannot silently enter scope.
