"""
Simplified steady-state hydraulic capacity/routing model for the Indus mainstem.

Scope and honesty note:
This is NOT a full unsteady hydraulic simulation (e.g. HEC-RAS / MIKE 11) and it is
NOT a cadastral inventory. It is a planning-level capacity check: given an assumed
inflow at Tarbela and an assumed reach transmission-loss percentage, it propagates
flow down the main Indus-stem structures and flags whether each structure's design
discharge capacity would be exceeded. Tributary inflows (Kabul at Nowshera, the
Punjab rivers joining near Panjnad/Mithankot, etc.) are NOT added along the way, so
real observed discharges at downstream barrages are normally higher than this model's
single-thread propagation would suggest. Travel time / storage routing is not modeled.

Capacity figures are published DESIGN discharge capacities (not live telemetry) drawn
from WAPDA, the Federal Flood Forecasting Division/Flood Fighting Plans, and press
reporting that cites official figures. Sources are listed per structure below and
should be re-verified against the responsible agency before any engineering use.
"""

import pandas as pd

# Ordered main-stem chain (Indus River only). Names must match data_loader.ROWS.
MAINSTEM_ORDER = [
    'Tarbela Dam',
    'Jinnah Barrage',
    'Chashma Barrage',
    'Taunsa Barrage',
    'Guddu Barrage',
    'Sukkur Barrage',
    'Kotri Barrage',
]

# Published design discharge capacities (cusecs = cubic feet per second).
CAPACITY = {
    'Tarbela Dam': {
        'capacity_cusecs': 1_500_000,
        'source': 'Federal Flood Forecasting Division (FFD), Pakistan — design discharge table',
    },
    'Jinnah Barrage': {
        'capacity_cusecs': 950_000,
        'source': 'WAPDA / FFC Kalabagh Flood Fighting Plan 2025 — design 950,000 cusecs '
                  '(ultimate capacity cited as 1,100,000 cusecs; max discharge passed: 1,087,000 cusecs on 30-07-2010)',
    },
    'Chashma Barrage': {
        'capacity_cusecs': 950_000,
        'source': 'WAPDA official salient features (wapda.gov.pk) — max design discharge 950,000 cusecs',
    },
    'Taunsa Barrage': {
        'capacity_cusecs': 1_000_000,
        'source': 'Federal Flood Forecasting Division (FFD), Pakistan — design discharge table',
    },
    'Guddu Barrage': {
        'capacity_cusecs': 1_200_000,
        'source': 'Dawn (2013) reporting official design capacity; consistent with FFD design-discharge table',
    },
    'Sukkur Barrage': {
        'capacity_cusecs': 900_000,
        'source': 'Sindh Irrigation Dept / WAPDA — reduced from an original 1,500,000 cusecs after 10 gates '
                  'were permanently closed following a 1941-42 model study',
    },
    'Kotri Barrage': {
        'capacity_cusecs': 875_000,
        'source': 'Federal Flood Forecasting Division (FFD), Pakistan — design discharge table',
    },
}

# One real, citable travel-time data point (not used in the calculation, shown as context).
KNOWN_TRAVEL_TIME_NOTE = (
    "Reported average lag time from Taunsa Barrage to Guddu Barrage is about 3 days "
    "(travel time varies with discharge and is not modeled here)."
)


def route_mainstem(inflow_cusecs: float, reach_loss_pct: float = 0.0) -> pd.DataFrame:
    """
    Propagate a single assumed inflow (at Tarbela) down the main Indus-stem structures.

    For each downstream structure, an assumed uniform reach transmission loss
    (reach_loss_pct, user-set — an illustrative assumption, not measured data) is
    applied to the incoming flow before checking it against that structure's
    published design discharge capacity. Flow passed downstream is capped at the
    structure's capacity (a rough proxy for what would otherwise overtop / require
    emergency breaching sections upstream).

    No tributary inflows are added. No storage or travel-time routing is modeled.
    """
    rows = []
    flow = float(inflow_cusecs)
    for i, name in enumerate(MAINSTEM_ORDER):
        cap = CAPACITY[name]['capacity_cusecs']
        flow_in = flow if i == 0 else flow * (1 - reach_loss_pct / 100.0)
        pct = (flow_in / cap * 100) if cap else float('nan')
        if pct >= 100:
            status = '🚨 Exceeds design capacity'
        elif pct >= 85:
            status = '⚠️ Near capacity'
        else:
            status = '✅ Within capacity'
        flow_out = min(flow_in, cap)
        rows.append({
            'Structure': name,
            'Design capacity (cusecs)': cap,
            'Flow in (cusecs)': round(flow_in),
            'Flow out (cusecs)': round(flow_out),
            '% of capacity': round(pct, 1),
            'Status': status,
            'Capacity source': CAPACITY[name]['source'],
        })
        flow = flow_out
    return pd.DataFrame(rows)
