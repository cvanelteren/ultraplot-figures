"""Multi-panel demo figure per prompt.md.

Layout (b and the top row span differently than the bottom row):

    | a  a  a  b  b  b |
    | c  c  d  d  e  e |

a) imshow with an inset scatter, b) network, c) scatter,
d) geo contour over Australia, e) grouped bars.
"""

import numpy as np
import networkx as nx
import ultraplot as uplt

rng = np.random.default_rng(7)

# ----------------------------------------------------------------- layout
layout = [
    [1, 1, 1, 2, 2, 2],
    [3, 3, 4, 4, 5, 5],
]
fig, axs = uplt.subplots(
    layout,
    refwidth=2.4,
    proj={4: "cyl"},
    share=False,
    left="4em",
)

# ------------------------------------------------- (a) imshow + inset scatter
axa = axs[0]
x = np.linspace(-3, 3, 200)
X, Y = np.meshgrid(x, x)
field = (
    np.exp(-((X - 1) ** 2 + (Y - 0.5) ** 2))
    + 0.8 * np.exp(-2 * ((X + 1.2) ** 2 + (Y + 1) ** 2))
    + 0.05 * rng.standard_normal(X.shape)
)
m = axa.imshow(field, cmap="fire", extent=[-3, 3, -3, 3], origin="lower")
axa.colorbar(m, loc="r", label="intensity (a.u.)")
ixa = axa.inset_axes([0.64, 0.07, 0.32, 0.32], zoom=False)
xs = rng.normal(1, 0.5, 80)
ys = rng.normal(0.5, 0.5, 80)
ixa.scatter(xs, ys, s=8, c="cyan7", alpha=0.7, ec="none")
ixa.format(
    title="peak samples", titlesize=7,
    xticklabelsize=6, yticklabelsize=6, grid=False,
)
axa.format(
    title="Emission field with sampled peak",
    xlabel="x (mm)", ylabel="y (mm)", grid=False,
)

# --------------------------------------------------------------- (b) network
axb = axs[1]
G = nx.watts_strogatz_graph(40, 4, 0.25, seed=7)
pos = nx.spring_layout(G, seed=7)
xy = np.array([pos[n] for n in G.nodes])
deg = np.array([G.degree(n) for n in G.nodes])
for u, v in G.edges:
    axb.plot(
        [pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]],
        color="gray6", lw=0.6, alpha=0.6, zorder=1,
    )
sc = axb.scatter(
    xy[:, 0], xy[:, 1], c=deg, s=25 * deg,
    cmap="marine", cmap_kw={"left": 0.25},
    ec="k", lw=0.4, zorder=2, values=np.unique(deg),
)
axb.colorbar(sc, loc="r", label="node degree")
axb.format(
    title="Small-world interaction network",
    xticks=[], yticks=[], grid=False,
)

# --------------------------------------------------------------- (c) scatter
axc = axs[2]
n = 150
conc = rng.uniform(0, 10, n)
resp = 2.5 * np.log1p(conc) + rng.normal(0, 0.4, n)
axc.scatter(conc, resp, c="ocean blue", s=14, alpha=0.7, ec="none")
cf = np.polyfit(conc, resp, 2)
cx = np.linspace(0, 10, 100)
axc.plot(cx, np.polyval(cf, cx), color="red7", lw=2, ls="--", label="quadratic fit")
axc.legend(loc="lr", frame=False)
axc.format(
    title="Dose–response",
    xlabel="dose (mg/kg)", ylabel="response (a.u.)",
)

# --------------------------------------------- (d) geo contour over Australia
axd = axs[3]
lon = np.linspace(105, 160, 80)
lat = np.linspace(-45, -8, 60)
LON, LAT = np.meshgrid(lon, lat)
temp = (
    32
    - 0.55 * np.abs(LAT + 25)
    - 4 * np.exp(-((LON - 147) ** 2 / 40 + (LAT + 37) ** 2 / 20))
    + 3 * np.sin(np.radians(3 * LON))
)
cf = axd.contourf(LON, LAT, temp, cmap="fire", levels=12, extend="both")
cl = axd.contour(LON, LAT, temp, color="k", lw=0.4, levels=6, labels=True)
axd.colorbar(cf, loc="b", label="surface temperature (°C)")
axd.format(
    title="Summer temperature, Australia",
    lonlim=(110, 156), latlim=(-45, -9),
    coast=True, land=False, ocean=True,
    lonlabels="b", latlabels="l", gridlabelsize="x-small",
)

# ----------------------------------------------------------- (e) grouped bars
axe = axs[4]
sites = ["North", "East", "South", "West"]
species = ["A. robustus", "B. gracilis", "C. velox"]
counts = np.array([
    [42, 30, 18],
    [35, 44, 22],
    [28, 25, 38],
    [50, 20, 30],
]) + rng.integers(-4, 5, (4, 3))
axe.bar(counts, cycle="qual1", labels=species, edgecolor="k", lw=0.4)
axe.legend(loc="ur", frame=False, ncols=1, fontsize="x-small")
axe.format(
    title="Species abundance by site",
    xticks=range(4), xticklabels=sites,
    xlabel="site", ylabel="count", ylim=(0, 60),
)

# ------------------------------------------------------------------ figure
fig.format(
    abc="(a)", abcloc="ul",
    suptitle="Synthetic multi-panel demonstration figure",
    titleloc="c",
)
fig.save("/home/casper/ultraplot-figures/examples/complex_layout_figure.png", dpi=200)
fig.save("/home/casper/ultraplot-figures/examples/complex_layout_figure.pdf")
print("saved")
