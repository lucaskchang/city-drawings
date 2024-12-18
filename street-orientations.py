import matplotlib.pyplot as plt
import numpy as np
import osmnx as ox

weight_by_length = False

ox.__version__

# define the study sites as label : query
places = {
    "Bellmore": "Bellmore, NY, USA",
    "Derry": "Derry, NH, USA",
    "Hopkinton": "Hopkinton, MA, USA",
    "San Francisco": "San Francisco, CA, USA",
    "Cary": "Cary, NC, USA",
    "Gorham": "Gorham, ME, USA",
    "Guilderland": "Guilderland, NY, USA",
    "Philadelphia": "Philadelphia, PA, USA",
    "Walnut Creek": "Walnut Creek, CA, USA",
    "Harrison": "Harrison, NY, USA",
    "Newton": "Newton, MA, USA",
    "Edina": "Edina, MN, USA",
    "Amherst": "Amherst, MA, USA",
    "Burke": "Burke, VA, USA",
    "Louisville": "Louisville, KY, USA",
    "Colorado Springs": "Colorado Springs, CO, USA",
    "Craftsbury Common": "Craftsbury Common, VT, USA",
    "Weston": "Weston, CT, USA",
    "Wayne": "Wayne, PA, USA",
    "Dallas": "Dallas, TX, USA",
    "Charleston": "Charleston, SC, USA",
    "Brooklyn": "Brooklyn, NY, USA",
    "Montpelier": "Montpelier, VT, USA",
    "Wakefield": "Wakefield, MA, USA",
    "Redondo Beach": "Redondo Beach, CA, USA",
}


# verify OSMnx geocodes each query to what you expect (i.e., a [multi]polygon geometry)
gdf = ox.geocode_to_gdf(list(places.values()))
gdf

# Store orientation entropies for each city
entropy_list = []

for place in sorted(places.keys()):
    print(ox.utils.ts(), place)
    G = ox.graph_from_place(places[place], network_type="drive")
    Gu = ox.add_edge_bearings(ox.convert.to_undirected(G))
    entropy = ox.bearing.orientation_entropy(Gu)
    entropy_list.append((place, entropy, Gu))

# Sort by entropy
sorted_entropy = sorted(entropy_list, key=lambda x: x[1])

# Create figure and axes for sorted cities
n = len(places)
ncols = int(np.ceil(np.sqrt(n)))
nrows = int(np.ceil(n / ncols))
figsize = (ncols * 5, nrows * 5)
fig, axes = plt.subplots(nrows, ncols, figsize=figsize,
                         subplot_kw={"projection": "polar"})

# Plot each city's polar histogram in sorted order
for ax, (place, entropy, Gu) in zip(axes.flat, sorted_entropy):
    print(ox.utils.ts(), f"Plotting {place} with entropy {entropy:.4f}")
    fig, ax = ox.plot_orientation(Gu, ax=ax, title=f"{place}\nEntropy: {
                                  entropy:.4f}", area=True)

# Add figure title and save the image
suptitle_font = {
    "family": "DejaVu Sans",
    "fontsize": 60,
    "fontweight": "normal",
    "y": 1,
}
fig.suptitle(
    "City Street Network Orientation (Sorted by Entropy)", **suptitle_font)
fig.tight_layout()
fig.subplots_adjust(hspace=0.35)
fig.savefig("images/street-orientations-sorted-sorted.png",
            facecolor="w", dpi=100, bbox_inches="tight")
plt.close()
