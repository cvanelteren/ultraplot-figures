# UltraPlot API reference (for figure-making)
Everything below assumes `import ultraplot as uplt`. UltraPlot's axes are `PlotAxes`, a *superset* of matplotlib axes — every mpl method still works, plus the additions here. Feed pandas/xarray objects directly; UltraPlot reads their labels, coordinates, and units for you.

## Creating figures & subplots
```python
fig, ax  = uplt.subplot(...)              # figure + one subplot
fig, axs = uplt.subplots(ncols=3, nrows=2)# grid; returns a SubplotGrid
fig      = uplt.figure(refwidth=2)        # empty figure, fill later
ax       = fig.subplot(121)               # matlab-style, or fig.add_subplot
```

**Complex layouts** with a "picture" array (`0` = empty slot):
```python
fig, axs = uplt.subplots([[1, 1, 2],
                          [3, 4, 2]], refwidth=1.8)
```

Or an explicit gridspec: `gs = uplt.GridSpec(nrows=2, ncols=2, pad=1)` then
`fig.subplot(gs[:, 0])`.

**Sizing** (pick one; real units, not pixels):
- `refwidth` / `refheight` — size of the *reference* subplot (best default).
- `figwidth` / `figheight` — total figure size.
- `refaspect`, `hratios`, `wratios`, `wspace`, `hspace`, `pad`, `panelpad`.
- Units accept numbers (inches) or strings like `'55mm'`, `'8em'`, `'2cm'`.

**SubplotGrid** (`axs`) is list- and array-indexable and broadcasts methods:
`axs[0]`, `axs[:, 0]` (first column), `axs[1, 1:]`, `axs.format(...)` applies to
all. Singleton grids act like a scalar.

**Axis sharing** is ON by default (shared limits/ticks/labels within rows/cols
plus *spanning* labels). Turn off with `share=False`, `span=False`. Levels:
`share=True|False|'labels'|'limits'|0|1|2|3`.

## `format()` — the one-stop formatter
Call on a figure, axes, or subplotgrid; or pass the same kwargs straight into `subplots(...)`. Grouped kwargs:

- **Figure:** `suptitle`, `suptitlecolor`, `toplabels`, `leftlabels`,
  `rightlabels`, `bottomlabels`.
- **Axes/general:** `title`, `titleloc` (`'l'|'c'|'r'`), `ltitle`/`rtitle`/
  `ultitle`/`urtitle`/... (corner titles), `abc=True|'a.'|'A.'|'[a]'`,
  `abcloc='ul'`, `facecolor`/`fc`, `edgecolor`/`ec`, `linewidth`/`lw`, `grid`,
  `gridminor`.
- **Cartesian:** `xlabel`/`ylabel`, `xlim`/`ylim`, `xscale='log'`, `xticks`,
  `yticks`, `xticklabels`, `xtickloc`/`ytickloc` (`'both'`), `xtickminor`,
  `xtickdir='inout'`, `xrotation`, `xgridminor`, `xbounds`, `xformatter`.
- **Polar:** `rlim`, `thetalim`, ... (`PolarAxes`).
- **Geographic:** `lonlim`/`latlim`, `lonlabels`/`latlabels`, `coast`, `land`,
  `ocean`, `borders`, `rivers` (`GeoAxes`, see Maps below).
- **rc settings:** any rc key works as a kwarg (dotted keys with dots removed,
  e.g. `abcloc` for `abc.loc`, or `rc_kw={'abc.loc': 'right'}`).

Shorthand aliases are pervasive: `fc`, `ec`, `lw`, `ls`, `c`. Use `uplt.arange(-3, 3)` (inclusive endpoint) for tick lists.

## Plotting commands (axes-level)
**1D / relational:**
`plot`, `plotx`, `line`, `linex`, `scatter`, `scatterx`, `step`, `stem`,
`vlines`, `hlines`, `parametric` (color-encodes a third variable along a line),
`area`, `areax`, `fill_between`, `fill_betweenx`, `bar`, `barh`.

**Distributions / statistics:**
`hist`, `hist2d`, `hexbin`, `boxplot`/`box`, `violinplot`/`violin`. UltraPlot adds
support for shaded error/percentile ranges via `shadedata`/`fadedata` or
`mean=True`, `median=True`, `bars=True`, `boxes=True` keywords on 1D commands.

**2D fields:**
`pcolormesh`, `pcolor`, `pcolorfast`, `imshow`, `heatmap` (labeled cells), `contour`, `contourf`, `tricontour`. Key kwargs: `cmap`, `cmap_kw`, `levels` (int count or explicit edges via `uplt.arange`), `values` (level *centers* — use to pin a diverging midpoint), `norm`, `vmin`/`vmax`, `extend='both'|'min'|'max'`,`labels=True` (inline contour/cell labels), `discrete`.

**Vector fields:** `quiver`, `streamplot`, `barbs`.
All accept on-the-fly guides: `colorbar='r'`, `legend='b'`, plus `colorbar_kw`,`legend_kw`, `cycle`, `cycle_kw`, `labels`.

## Colorbars & legends
**Locations** (`loc`/`location`): outer side = `'l'`, `'r'`, `'t'`, `'b'`; inset =`'ul'`, `'ur'`, `'ll'`, `'lr'`, or full words (`'upper right'`). Outer guides allocate a new gridspec row/column — they don't steal subplot space or distort aspect ratios. Multiple guides on one side stack.

```python
ax.colorbar(m, loc="r", label="...", length=0.8, extend="both", tickminor=True)
ax.legend(handles, loc="b", ncols=3, center=True, frame=False, order="C")
fig.colorbar(m, loc="b", col=1)          # figure-wide, aligned to column 1
fig.legend(hs, loc="r", rows=(1, 2))     # span specific rows/cols
```

- **On-the-fly:** pass `colorbar='b'` / `legend='ul'` straight to a plot command.
- **Colorbar from lines/artists or colors:** `ax.colorbar(lines, values=[...])` or `ax.colorbar('Blues', values=range(10))`.
- **Ticks:** `locator`/`ticks`, `minorlocator`/`minorticks`, `formatter`/ `ticklabels`, `tickloc`. Width/length are in physical units.
- **Legend extras:** auto-infer handles/labels; `labels=` for 2D-array columns; `center=True` for centered rows; `alphabetize=True`; restyle handles by passing `lw`, `color`, `markersize`, or `handle_kw`.
- **Decouple content/location:** `fig.legend(ax=axs[1, :], ref=axs[0, :],
  loc='b')` builds from one group's handles, places by another.

**Semantic legends** (describe an *encoding*, no exemplar artist needed):
`ax.catlegend(names, colors={...}, markers={...})`,
`ax.sizelegend([10, 50, 200], labels=[...])`,
`ax.numlegend(vmin=0, vmax=1, n=5, cmap='viko')`,
`ax.entrylegend([{...}, {...}])`, `ax.geolegend([...])`. All exist on `fig` too
and accept `add=False` to return `(handles, labels)` for composition.

## Panels & insets
```python
px = ax.panel_axes("r", width="4em")     # marginal panel (share axis)
ix = ax.inset_axes([0.6, 0.6, 0.3, 0.3]) # inset; zoom indicators available
axt = ax.altx()   # twin x with independent scale;  ax.alty(), ax.dualx()
```
`panel_axes`/`inset_axes`/`altx`/`alty` also exist on the SubplotGrid.

## Maps (GeoAxes)
```python
fig, axs = uplt.subplots(proj="robin", ncols=2)   # or proj="cyl","ortho",...
axs.format(coast=True, land=True, ocean=True, borders=True,
           lonlim=(-60, 60), latlim=(0, 80),
           lonlabels="b", latlabels="l", grid=True)
ax.pcolormesh(lon, lat, data, cmap="batlow")       # data in lon/lat
```
Backends: cartopy (default) or basemap via `backend=`. Pass projection kwargs with `proj_kw`. Requires cartopy in the env.

## rc / styling

```python
uplt.rc.cycle = "colorblind"                  # global color cycle
uplt.rc.update({"fontname": "Source Sans Pro", "fontsize": 11})
uplt.rc["figure.facecolor"] = "white"
with uplt.rc.context({"suptitle.size": 13}):  # scoped block
    ...
uplt.rc.reset()                               # back to defaults
```
`uplt.rc` spans both matplotlib rcParams and UltraPlot-only settings. Switch mpl
stylesheets per-axes with `ax.format(style="ggplot")`.

## Saving
`fig.save("~/fig.pdf")` or `fig.savefig(...)`. Default is vector PDF at high DPI; `~` is expanded. For raster, use `.png` (DPI defaults to 1000).
