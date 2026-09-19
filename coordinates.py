"""
Coordinate data for map markers, replacing the original "representative
visualization points" with verified/sourced coordinates wherever a citable
figure was found.

Each entry is (lat, lon, status, source). status is one of:
  - "verified"     : matches an official/structural-infobox coordinate
                      (Wikipedia infobox sourced from survey/engineering data,
                      or a government document) for the structure itself.
  - "approximate"  : sourced, but for the nearest named settlement/reference
                      point rather than a survey-grade fix on the structure
                      itself (typically within a few km).
  - "representative": no citable coordinate was found this pass; retains the
                      original placeholder value pending verification.

This still is not a substitute for as-built engineering/GIS coordinates
(centerline surveys, structure drawings) - for that, the responsible agency
(WAPDA for dams/barrages, provincial Irrigation Department for headworks)
should be consulted directly. But every "verified"/"approximate" point here
is now tied to a real citation instead of being an arbitrary placement.
"""

POINTS = {
    # --- Dams ---
    'Tarbela Dam': (34.0897, 72.6983, 'verified', 'Wikipedia infobox (Tarbela Dam)'),
    'Diamer Basha Dam': (35.5195, 73.7392, 'verified', 'Wikipedia infobox (Diamer-Bhasha Dam)'),
    'Dasu Hydropower Project': (35.3173, 73.1933, 'verified', 'Wikipedia infobox (Dasu Dam)'),
    'Mohmand Dam': (34.3532, 71.5330, 'verified', 'Wikipedia infobox (Mohmand Dam)'),
    'Warsak Dam': (34.1639, 71.3581, 'verified', 'Wikipedia infobox (Warsak Dam)'),
    'Mangla Dam': (33.1421, 73.6450, 'verified', 'Wikipedia infobox (Mangla Dam)'),
    'Kurram Tangi Dam Project': (33.1706, 70.3997, 'verified', 'Wikipedia infobox (Kurram Tangi Dam)'),
    'Nai Gaj Dam': (26.8756, 67.3206, 'verified', 'Wikipedia infobox (Nai Gaj Dam)'),
    'Naulong Storage Dam': (29.18, 67.90, 'representative', 'No citable structure-level coordinate found; original placeholder retained'),

    # --- Barrages / Headworks ---
    'Nowshera Head Works': (34.0153, 71.9747, 'approximate', 'Wikipedia (Nowshera town center) — headworks itself not separately geotagged in sources checked'),
    'Chashma Barrage': (32.4339, 71.3789, 'verified', 'Wikipedia infobox (Chashma Barrage)'),
    'Jinnah Barrage': (32.9185, 71.5219, 'verified', 'Wikipedia infobox (Jinnah Barrage)'),
    'Rasul Barrage': (32.6803, 73.5208, 'verified', 'Wikipedia infobox (Rasul Barrage)'),
    'Marala Barrage / Headworks': (32.6733, 74.4639, 'verified', 'Wikipedia infobox (Marala Headworks)'),
    'Khanki Barrage': (32.4625, 74.0239, 'approximate', "Punjab Irrigation Dept. Flood Fighting Plan (Jhelum Canal Division) — Chenab outfall point immediately upstream of Khanki Barrage"),
    'Qadirabad Barrage': (32.2975, 73.5019, 'approximate', 'Wikipedia (Qadirabad village center, ~5 km from the barrage on the Chenab)'),
    'Trimmu Barrage': (31.1443, 72.1464, 'verified', 'Wikipedia infobox (Trimmu Barrage), matches Punjab Irrigation Dept. Flood Fighting Plan coordinates'),
    'Balloki Barrage / Headworks': (31.2222, 73.8591, 'verified', 'Wikipedia infobox (Balloki Headworks)'),
    'Sidhnai Barrage': (30.49, 72.21, 'representative', 'No citable structure-level coordinate found; original placeholder retained'),
    'Sulemanki Barrage': (30.3775, 73.8667, 'verified', 'Wikipedia infobox (Sulemanki Headworks)'),
    'Islam Barrage': (29.8264, 72.5492, 'verified', 'Wikipedia infobox (Islam Headworks)'),
    'Panjnad Barrage': (28.9500, 70.5000, 'approximate', 'Wikipedia (Panjnad area, where the five Punjab rivers merge) — not a survey fix on the barrage itself'),
    'Taunsa Barrage': (30.5128, 70.8492, 'verified', 'Wikipedia infobox (Taunsa Barrage)'),
    'Guddu Barrage': (28.4186, 69.7132, 'verified', 'Wikipedia infobox (Guddu Barrage)'),
    'Sukkur Barrage': (27.6806, 68.8453, 'verified', 'Wikipedia infobox (Sukkur Barrage)'),
    'Kotri Barrage': (25.4422, 68.3167, 'verified', 'Wikipedia infobox (Kotri Barrage)'),

    # --- Confluences ---
    'Indus + Kabul': (33.9167, 72.2322, 'verified', 'Wikipedia (Kabul River infobox — river mouth near Attock/Kund Park)'),
    'Neelum + Jhelum': (34.37, 73.47, 'representative', 'No citable confluence coordinate found; original placeholder retained'),
    'Swat + Kabul': (34.1225, 71.7114, 'verified', 'Wikipedia (Swat River infobox — river mouth near Charsadda)'),
    'Jhelum + Chenab': (31.1443, 72.1464, 'verified', 'Punjab Irrigation Dept. Flood Fighting Plan / Wikipedia — Trimmu Barrage sits just below this confluence'),
    'Ravi + Chenab system': (30.70, 71.60, 'representative', 'No citable confluence coordinate found; original placeholder retained'),
    'Sutlej + Chenab': (29.35, 71.05, 'representative', 'No citable confluence coordinate found; original placeholder retained'),
    'Panjnad + Indus': (28.97, 70.50, 'representative', 'No citable confluence coordinate found; original placeholder retained'),
}


def summary_counts():
    """Return counts of points by verification status, for display."""
    counts = {'verified': 0, 'approximate': 0, 'representative': 0}
    for _, _, status, _ in POINTS.values():
        counts[status] += 1
    return counts
