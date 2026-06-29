# PROJECT GOAL

Learn algorithms intuitively, down to the guts, through simple readable code. Each algorithm is a self-contained teaching artefact.

---

# TRACK 1 — EVOLUTIONARY PROGRAMMING

Learning path (each step is a small standalone script):

1. Random search baseline — maximise a 1D function by pure guessing. Establishes the "search" mindset and a fitness function.
2. Hill climbing — one parent, mutate, keep if better. Introduces mutation and selection pressure.
3. Adaptive step size (1/5 success rule) — hill climbing that grows or shrinks its step size based on how often mutations succeed. Introduces controlling exploration over time.
4. Population-based EP — many candidates at once; mutate each, then keep the best survivors. Introduces population and competition.
5. Self-adaptive mutation — each individual carries its own step size, which evolves alongside the solution. Introduces strategy parameters.
6. Multi-dimensional optimisation — evolve a vector, not a scalar. Optimise a known benchmark (e.g. sphere, Rastrigin).
7. Evolving a structure — apply EP to a small concrete task (e.g. fit parameters, evolve a simple controller/policy).

Each step adds exactly one new idea over the previous one.
