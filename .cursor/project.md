# PROJECT GOAL

Learn algorithms intuitively, down to the guts, through simple readable code. Each algorithm is a self-contained teaching artefact.

---

# TRACK 1 — EVOLUTIONARY PROGRAMMING

Learning path (each step is a small standalone script). Each step adds exactly one new idea over the previous one.

1. [DONE] `step1_random_search.py` — maximise a 1D function by pure guessing. The "search" mindset + a fitness function.
2. [DONE] `step2_hill_climbing.py` — one solution, mutate with a small Gaussian step, keep if better. Search locally around the best instead of guessing blindly.
3. [DONE] `step3_adaptive_step_size.py` — (1+1)-ES with the 1/5 success rule: grow/shrink the step size from how often mutations succeed. Controlling exploration over time.
4. [DONE] `step4_population.py` — (μ+λ)-ES with truncation selection; many candidates, mutate each, keep best survivors. Population + competition; escapes local peaks (switched to a multimodal cos landscape to show this).
5. [DONE] `step5_self_adaptive.py` — each individual carries its own step size which mutates first, then drives the x-mutation. Selection tunes step sizes for free (strategy parameters).
6. [DONE] `step6_multidimensional.py` — individual is now a vector; mutation nudges every component. Optimised on 2D Rastrigin, plotted as a contour map.
7. [TODO — START HERE] Evolving a structure — apply the same engine to a concrete task (e.g. fit parameters of a curve to data, or evolve a tiny controller/policy). Ties EP to a real use; strong candidate: feature/band selection (combinatorial, no gradient) since that is Arif's domain.

## Conventions established (keep consistent for step 7)
1. No comments/docstrings; full descriptive names; gritty bits in small helpers; `__main__` guard; `random.seed(0)`.
2. Each script prints its iteration/generation number so Arif can see how many steps run.
3. Plot convention: green/scatter attempt points fade small+faint (early) to large+solid (late) via `point_size_and_opacity`; black `fitness landscape` curve (or contour in 2D); red `best found`.
4. Explain every new concept intuitively before/while using it; keep replies very brief; never paste code in chat (Arif reads files).
5. matplotlib + numpy required (`pip install numpy matplotlib`).
