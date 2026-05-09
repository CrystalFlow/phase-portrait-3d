# Professor feedback on straight-line solutions project

The following is the professor's email responding to the initial project proposal
(a 2D phase portrait visualizer focused on straight-line solutions / eigenvector geometry).

---

> If you want to do straight-line solutions, in a sense, we know all about them already,
> and even with the repeated and zero eigenvalues, we're essentially talking about drawing
> lines. This also means the visualizer wouldn't support complex eigenvalues, which is a
> bit too restrictive. Also, are you intending to draw the full phase portrait and not just
> the straight-line solutions? (You should, it's just transforming one vector into another.)
>
> To make this worth a high pass, I would suggest making the visualizer more advanced in
> either of two ways.
>
> You could make it a visualizer for three-dimensional systems with a proper 3D plot. If
> you wanted to, you could also do a heat map or similar for 4D.
>
> You could make it a visualizer for higher-dimensional systems. In this case, you would
> have to run through all n(n-1)/2 pairs of coordinates and project down to each phase
> plane.
>
> Alternatively or additionally, since this is not terribly easy to interpret, you could
> throw in something that allows for exploring the phase space. This would require the
> most creativity.

---

## Chosen path

**Path 1: 3D (and optionally 4D) visualizer.**

Rationale:
- Most natural extension of the 2D phase portrait concept
- Allows complex eigenvalues (spiraling in eigenplanes — genuinely hard to picture in 2D)
- 4D color encoding adds a mathematically meaningful layer without extra axes
- Easier to produce compelling figures for the written report than the n-dimensional projection approach

The professor explicitly noted that Path 2 (n-dimensional projections) is "not terribly easy
to interpret" and that Path 1 with interactivity "would require the most creativity" — which
is the high-pass signal.

## Key constraints implied by the feedback

- Must draw the **full phase portrait** (trajectories), not just straight-line solutions
- Must handle **complex eigenvalues** (the 2D-only version couldn't)
- "Proper 3D plot" — this means actual 3D axes, not three separate 2D projections
- Interactivity is valued ("exploring the phase space")
