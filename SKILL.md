---
name: ultraplot-figures
description: >-
  Create clean, publication-quality scientific figures with UltraPlot (the
  matplotlib wrapper, imported as `uplt`). Use whenever the task is to make,
  refine, or review an UltraPlot figure — line/scatter plots, pcolor/contour
  fields, maps, statistical plots — and you want the result to be both
  scientifically sound (honest encodings, perceptually uniform colormaps,
  colorblind-safe) and visually polished. Triggers on: "ultraplot", "uplt",
  "make a figure/plot", "publication figure", "colormap/colorbar", "subplots",
  proplot-style plotting.
---

# UltraPlot figures: sound + beautiful

UltraPlot (`import ultraplot as uplt`) subclasses matplotlib's `Figure`, `Axes`,
and `GridSpec` to remove boilerplate and ship better defaults. Your job with this skill is to produce figures that are **scientifically honest first, beautiful second** — and to lean on UltraPlot's automation instead of hand-rolling matplotlib calls.

For chart-selection and general design theory (which chart for which data, when a color scale lies, accessibility thresholds), defer to the `dataviz` skill. This skill is the **UltraPlot execution layer**: how to express good choices in `uplt`.

## The non-negotiables (check every figure against these)
1. **Perceptually uniform, colorblind-safe colormaps.** Never `jet`/`rainbow`. Use sequential for magnitude, diverging for signed data with a meaningful zero, cyclic for phase/angle. UltraPlot's `PerceptualColormap`s (`fire`, `dusk`, `ice`, `boreal`) and the bundled cmOcean / Fabio Crameri "scientific colour maps" (`batlow`, `roma`, `viko`, `romaO`) are all safe defaults.
2. **Honest encodings.** Don't truncate a bar/area baseline away from a meaningful zero. Center diverging maps on the true neutral value (use `values=`/`levels=` so the midpoint is real, not implied). Keep aspect ratios undistorted for spatial data (`ax.format(aspect='equal')` / maps).
3. **Data-ink.** Trust UltraPlot's clean defaults. Turn gridlines off when they don't aid reading (`grid=False`). No chartjunk, no 3D for 2D data, no redundant legends when a colorbar already encodes the variable.
4. **One `format()`, not scattered setters.** Titles, labels, limits, ticks, a-b-c labels, row/col labels all go through `ax.format(...)` / `fig.format(...)`. This is the single biggest readability win over raw mpl.
5. **Let UltraPlot lay out.** Prefer `uplt.subplots(...)`, automatic axis sharing, spanning labels, and *outer* colorbars/legends over manual `bbox_to_anchor` and `subplots_adjust`. Outer guides get their own gridspec slot, so they never distort subplot aspect ratios.
6. **Vector output, sized for the medium.** Default `savefig.format` is PDF and `savefig.dpi` is 1000 — good for journals. Size with `refwidth`/`figwidth` in real units so text stays legible at print size; don't rescale after the fact.
7. Ensure that spacing is correctly done; no overlapping insets with abc labels, titles, annotations or what not. Insets should be sized appropriately to the main plot unless specified otherwise.

## Minimal workflow

```python
import numpy as np
import ultraplot as uplt

fig, axs = uplt.subplots(ncols=2, refwidth=2.2, share=True)
axs[0].plot(x, y, lw=2, cycle="538", labels=["a", "b", "c"], legend="b")
m = axs[1].pcolormesh(field, cmap="batlow", levels=11, extend="both")
axs[1].colorbar(m, loc="r", label="value")
axs.format(
    abc="a.", abcloc="ul",
    suptitle="Descriptive figure title",
    xlabel="x (units)", ylabel="y (units)",
    grid=False,
)
fig.save("~/figure.pdf")
```

Steps every time:
1. **Pick the plot command** — see `references/api.md` for the full menu (`plot`,`scatter`, `bar`/`barh`, `area`, `hist`, `boxplot`/`violin`, `pcolormesh`,
   `contour`/`contourf`, `heatmap`, `imshow`, `quiver`/`streamplot`, `parametric`, maps). Feed it pandas/xarray directly — labels are auto-detected.
2. **Choose color** — `references/color.md`. Match colormap/cycle *type* to data *type*. Build/tune with `uplt.Colormap(...)` and `uplt.Cycle(...)`.
3. **Annotate** — colorbars and legends on-the-fly via `colorbar=`/`legend=` keywords, or explicit `ax.colorbar()`/`ax.legend()`/`fig.colorbar()`. Use `loc` shorthands (`'r'`, `'b'`, `'ul'`, `'ll'`). Semantic keys (`catlegend`, `sizelegend`, `numlegend`) when the legend describes an *encoding*, not existing artists.
4. **Format once** — one `format()` per grouping. Use `abc=True` for panel letters, `toplabels`/`leftlabels` for grid headers, `suptitle` for the figure.
5. **Verify** — actually render it and look. See "Verifying" below.

## Colormap & cycle quick reference

- **Sequential** (0→max magnitude): `batlow`, `viko`, `fire`, `dusk`, `ice`,`boreal`, `marine`, `Blues`, mpl `viridis`/`magma`.
- **Diverging** (signed, meaningful zero): `Div`, `roma`, `vik`, `BuRd`,`RdBu`. Name reversal is flexible (`BuRd` == `RdBu_r`).
- **Cyclic** (phase/angle/longitude): `romaO`, or build one with `uplt.Colormap(h=(0,360), c=50, l=70, space='hcl', cyclic=True)`.
- **Categorical cycles** (distinct lines/bars): `538`, `ggplot`, `colorblind`, `qual1`, `Set3`, `bmh`. Set globally with `uplt.rc.cycle = '538'` or per-call with `cycle=`.
- Append `_r` to reverse, `_s` to shift any map/cycle. Names ar case-insensitive.
- Explore interactively: `uplt.show_cmaps()`, `uplt.show_cycles()`, `uplt.show_channels('fire', 'dusk')` (check perceptual uniformity), `uplt.show_colors()`.

## Common mistakes to avoid

- Reaching for raw `matplotlib.pyplot` — stay in the axes-level `uplt` API.
- `jet`, `rainbow`, `hsv` for magnitude data (perceptually misleading).
- A diverging colormap on strictly-positive data, or a sequential one on signed data — the map type must match the data.
- Manual legend placement with `bbox_to_anchor` — use `loc='r'`/`'b'` for outer guides instead.
- Redundant encodings (colorbar *and* legend for the same variable).
- Fighting axis sharing: if shared limits/ticks are wrong for the data, pass `share=False`/`span=False` rather than overriding subplot-by-subplot.
- Setting figure size in pixels after rendering — size up front with `refwidth`/`figwidth` in inches (or `'55mm'` etc.).

## Verifying

Do not claim a figure "looks good" without rendering it. Save to PNG and open it, or run in a notebook. A quick smoke test:

```python
import ultraplot as uplt
fig, ax = uplt.subplots()
ax.plot([0, 1, 2], [0, 1, 4])
fig.save("/tmp/uplt_check.png")
```

## Reference files (load as needed)
- `references/api.md` — plotting-command menu, `format()` keywords, layout (subplots/gridspec/panels/insets), maps, statistical plots.
- `references/color.md` — choosing, building, and modifying colormaps & cycles.
- `references/recipes.md` — copy-paste "good default" figures for common cases.
- if there exists an environment listed as `ultraplot-dev` use that (check with micromamba, mamba or conda) unless the user specifies otherwise.
