import osmnx as ox
import matplotlib.pyplot as plt
import geopandas as gpd

# turn off cache
ox.settings.use_cache = False

# Define the address and distance
address = "Tufts University, Medford, MA, USA"
point = ox.geocode(address)
distance = 1000
scale = 1 / distance
bbox = ox.utils_geo.bbox_from_point(point, distance)

# Create a plot and add a background
fig, ax = plt.subplots(figsize=(6, 6))
background = ox.utils_geo.bbox_to_poly(bbox)
p = gpd.GeoSeries(background)
p.plot(ax=ax, color="linen", zorder=0)

# features and styles
features = {
    "buildings": {
        "tags": {"building": True},
        "plot_settings": {"color": "lightgrey"}
    },
    "parks": {
        "tags": {"leisure": "park", "landuse": "grass"},
        "plot_settings": {"color": "#3cb371"}
    },
    "sports": {
        "tags": {"leisure": ["pitch", "golf_course"], "landuse": "recreation_ground"},
        "plot_settings": {"color": "#10a674"}
    },
    "woods": {
        "tags": {"natural": "wood", "landuse": "forest"},
        "plot_settings": {"color": "forestgreen"}
    },
    # "bus_stops": {
    #     "tags": {"highway": "bus_stop"},
    #     "plot_settings": {"color": "orange", "markersize": round(scale * 10000), "edgecolor": "none"}
    # },
    "highways": {
        "tags": {"highway": "motorway"},
        "plot_settings": {"color": "dimgrey", "linewidth": round(scale * 2000, 2)}
    },
    "large_roads": {
        "tags": {"highway": ["trunk", "primary", "secondary"]},
        "plot_settings": {"color": "dimgrey", "linewidth": round(scale * 1500, 2)}
    },
    "small_roads": {
        "tags": {"highway": ["residential", "tertiary", "unclassified", "service"]},
        "plot_settings": {"color": "dimgrey", "linewidth": round(scale * 1000, 2)}
    },
    "sidewalks": {
        "tags": {"highway": ["footway", "pedestrian", "path", "steps"]},
        "plot_settings": {"color": "grey", "linewidth": round(scale * 500, 2), "linestyle": "dashed"}
    },
    "cycleways": {
        "tags": {"highway": "cycleway", "biycle": True},
        "plot_settings": {"color": "green", "linewidth": round(scale * 250, 2)}
    },
    "water": {
        "tags": {"natural": ["water", "bay", "strait", "wetland"], "waterway": ["river", "canal"], "maritime": "yes", "sea": "yes", "landuse": "reservoir", "leisure": "marina"},
        "plot_settings": {"color": "royalblue"}
    },
    "beaches": {
        "tags": {"natural": ["beach", "sand"]},
        "plot_settings": {"color": "#edd0b1"}
    },
    "parking": {
        "tags": {"parking": "surface"},
        "plot_settings": {"color": "darkgrey"}
    },
    "rail": {
        "tags": {"railway": ["funicular", "light_rail", "rail", "tram", "monorail"]},
        "plot_settings": {"color": "dimgrey", "linewidth": round(scale * 1000, 2), "linestyle": (0, (5, 5))}
    },
    # "underground": {
    #     "tags": {"railway": "subway"},
    #     "plot_settings": {"color": "dimgrey", "linewidth": round(scale * 500, 2)}
    # },
    "track": {
        "tags": {"leisure": "track"},
        "plot_settings": {"color": "#904436"}
    },
    "heath": {
        "tags": {"natural": ["heath", "moor", "scrub"]},
        "plot_settings": {"color": "#D7D99F"}
    },
    "rock": {
        "tags": {"natural": "scree"},
        "plot_settings": {"color": "#B0B0B0"}
    }
}

for feature in features:
    try:
        data = ox.features_from_bbox(
            bbox, tags=features[feature]["tags"])
        data.plot(ax=ax, **features[feature]["plot_settings"])
        print(f'Plotted {len(data)} {feature}')
    except ox._errors.InsufficientResponseError:
        print(f'No {feature} found')

ax.set_axis_off()
ax.set_xlim(bbox[0], bbox[2])
ax.set_ylim(bbox[1], bbox[3])
plt.tight_layout()
# plt.title(address, loc="left", fontdict={"fontsize": 20, "fontweight": "bold"}, y=2)
fig.savefig(f"images/{address.split(',')[0].lower().replace(" ", "-")}-{distance / 1000}k.png", dpi=600, pad_inches=0.5)
plt.show()
