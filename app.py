import streamlit as st
import pandas as pd
from data_loader import load_data
from map_view import make_map
from network_view import make_network
from hydraulic_model import route_mainstem, MAINSTEM_ORDER, CAPACITY, KNOWN_TRAVEL_TIME_NOTE
from coordinates import summary_counts as _coord_summary_counts

st.set_page_config(page_title='Pakistan Rivers & Irrigation Explorer', page_icon='🌊', layout='wide')

st.title('🌊 Pakistan Rivers, Dams, Barrages & Link Canals Explorer')
st.caption('Interactive reference for the major Indus Basin water system and selected river systems of Pakistan.')

DATA = load_data()
PROVINCES = [
    'Gilgit-Baltistan', 'Khyber Pakhtunkhwa (KPK)', 'Punjab', 'Sindh',
    'Balochistan', 'Azad Jammu & Kashmir (AJK)', 'Islamabad Capital Territory (ICT)'
]

with st.sidebar:
    st.header('Filters')
    province = st.selectbox('Province / Region', ['All'] + PROVINCES)
    types = st.multiselect(
        'Show asset types',
        ['River', 'Dam', 'Barrage', 'Link Canal', 'Confluence'],
        default=['River', 'Dam', 'Barrage', 'Link Canal', 'Confluence']
    )
    search = st.text_input('Search', placeholder='Tarbela, Chenab, Taunsa...')
    labels = st.checkbox('Show map labels', True)
    st.divider()
    st.markdown('### App scope')
    _cc = _coord_summary_counts()
    st.write(
        f"Map coordinates: {_cc['verified']} verified against official/structural sources, "
        f"{_cc['approximate']} approximate (nearest sourced reference point), "
        f"{_cc['representative']} still unverified placeholders — see the Map tab for which is which."
    )
    st.write(
        'The Hydraulic Model tab adds a simplified, sourced capacity/routing check for the '
        'Indus mainstem — see that tab for its assumptions and limits.'
    )
    st.write(
        '**Not included:** a cadastral (land-parcel) inventory. Parcel-level ownership and '
        'survey records (khasra numbers, mauza boundaries) are held by each province\'s land-revenue '
        'authority, not published as open data, so this app cannot compile or estimate that data. '
        'For actual land-parcel records, go to the source: '
        '[Punjab Land Records Authority](https://www.punjab-zameen.gov.pk/), '
        '[Sindh Board of Revenue](https://bor.sindh.gov.pk/) / '
        '[Sindh land record portal](https://sindhzameen.gos.pk/), '
        'or the Board of Revenue for Khyber Pakhtunkhwa, Balochistan, Gilgit-Baltistan or AJK.'
    )

assets = DATA['assets'].copy()
if province != 'All':
    # regex=False: several province names contain literal parentheses (e.g. "(KPK)"),
    # which pandas would otherwise interpret as regex grouping syntax and match nothing.
    assets = assets[assets['province_region'].str.contains(province, case=False, na=False, regex=False)]
if types:
    assets = assets[assets['asset_type'].isin(types)]
else:
    assets = assets.iloc[0:0]
if search.strip():
    q = search.strip()
    mask = assets.apply(lambda r: r.astype(str).str.contains(q, case=False, na=False, regex=False).any(), axis=1)
    assets = assets[mask]

c = st.columns(5)
for i, t in enumerate(['River', 'Dam', 'Barrage', 'Link Canal', 'Confluence']):
    c[i].metric(t + 's', int((assets.asset_type == t).sum()))

overview_tab, map_tab, river_tab, structure_tab, link_tab, network_tab, hydraulic_tab, data_tab, sources_tab = st.tabs([
    '🇵🇰 Provinces & Regions', '🗺️ Map', '🏞️ Rivers', '🏗️ Dams & Barrages', '🔗 Link Canals', '🔄 Network',
    '🧮 Hydraulic Model', '📊 Data', '📚 Sources'
])

with overview_tab:
    st.subheader('Pakistan Provinces / Regions Covered')
    overview = pd.DataFrame({
        'Province / Region': PROVINCES,
        'Included water-system examples': [
            'Indus, Gilgit, Shyok, Shigar; Diamer Basha',
            'Indus, Kabul, Swat, Kurram, Gomal; Tarbela, Warsak, Mohmand',
            'Jhelum, Chenab, Ravi, Sutlej, Panjnad; major barrages and link canals',
            'Indus, Hub; Guddu, Sukkur, Kotri and associated lower-Indus system',
            'Hub, Hingol, Dasht, Mula; Naulong and other project references',
            'Jhelum, Neelum, Poonch; Mangla system',
            'Soan, Korang and Haro regional river relationships'
        ]
    })
    st.dataframe(overview, use_container_width=True, hide_index=True)
    st.info('The province/region selector is an administrative filter. River basins and water infrastructure often cross provincial or regional boundaries.')


with map_tab:
    st.subheader('Interactive Water-System Map')
    st.plotly_chart(make_map(assets, show_labels=labels), use_container_width=True, config={'scrollZoom': True, 'displaylogo': False})
    _cc = _coord_summary_counts()
    st.info(
        f"Marker coordinates: **{_cc['verified']} verified** against an official source or structural "
        f"infobox (e.g. WAPDA, Punjab Irrigation Dept., Wikipedia infoboxes citing survey data), "
        f"**{_cc['approximate']} approximate** (nearest sourced settlement/reference point, typically "
        f"within a few km of the actual structure), and **{_cc['representative']} still unverified "
        f"placeholders** pending a citable source. Hover any marker to see its status and source. "
        f"River-line paths remain illustrative, not a surveyed centerline — for engineering/GIS "
        f"production use, confirm every point against the responsible agency regardless of status shown here."
    )

with river_tab:
    df = assets[assets.asset_type == 'River'].copy()
    st.dataframe(df[['name','river_system','province_region','upstream','downstream','confluences','notes']], use_container_width=True, hide_index=True)
    if not df.empty:
        name = st.selectbox('Inspect river', df.name.tolist())
        r = df[df.name == name].iloc[0]
        a,b = st.columns(2)
        with a:
            st.markdown(f'### {r.name}')
            st.write('**River system:**', r.river_system)
            st.write('**Province/region:**', r.province_region)
            st.write('**Upstream:**', r.upstream)
        with b:
            st.write('**Downstream:**', r.downstream)
            st.write('**Confluences:**', r.confluences)
            st.write('**Notes:**', r.notes)

with structure_tab:
    st.subheader('Dams and Barrages / Headworks')

    def _with_capacity(df):
        df = df.copy()
        df['design_capacity_cusecs'] = df['name'].map(
            lambda n: f"{CAPACITY[n]['capacity_cusecs']:,}" if n in CAPACITY else '—'
        )
        return df

    a,b = st.columns(2)
    with a:
        st.markdown('#### Dams')
        st.dataframe(
            _with_capacity(assets[assets.asset_type == 'Dam'])[
                ['name','river_system','province_region','status','design_capacity_cusecs','upstream','downstream','notes']]
            .rename(columns={'river_system': 'river', 'design_capacity_cusecs': 'design capacity (cusecs)'}),
            use_container_width=True, hide_index=True)
    with b:
        st.markdown('#### Barrages / Headworks')
        st.dataframe(
            _with_capacity(assets[assets.asset_type == 'Barrage'])[
                ['name','river_system','province_region','status','design_capacity_cusecs','upstream','downstream','notes']]
            .rename(columns={'river_system': 'river', 'design_capacity_cusecs': 'design capacity (cusecs)'}),
            use_container_width=True, hide_index=True)
    st.caption(
        "'design capacity (cusecs)' is populated only for the mainstem structures sourced in the "
        "Hydraulic Model tab; '—' means not yet verified/entered for this app."
    )

with link_tab:
    st.subheader('Major Link Canals')
    st.dataframe(
        assets[assets.asset_type == 'Link Canal'][['name','river_system','province_region','status','upstream','downstream','notes']]
        .rename(columns={'river_system': 'source → receiving river', 'upstream': 'offtake', 'downstream': 'outfall'}),
        use_container_width=True, hide_index=True)
    st.caption('The link-canal relationships follow the major Indus Basin irrigation-system schematic; exact alignments should be supplied from authoritative GIS layers for detailed engineering use.')

with network_tab:
    st.subheader('Conceptual River Connectivity')
    st.plotly_chart(make_network(assets), use_container_width=True, config={'displaylogo': False})
    st.markdown('### Example upstream → downstream chains')
    chains = {
        'Indus': 'Upper Indus → Tarbela → Kabul/Attock system → Chashma → Taunsa → Guddu → Sukkur → Kotri → Indus Delta → Arabian Sea',
        'Jhelum': 'Upper Jhelum → Mangla → Rasul → Trimmu/Jhelum-Chenab system → Panjnad',
        'Chenab': 'Upper Chenab → Marala → Khanki → Qadirabad → Trimmu → Panjnad',
        'Ravi': 'Upper Ravi → Balloki/Sidhnai system → lower Ravi → Chenab/Panjnad system',
        'Sutlej': 'Upper Sutlej → Sulemanki/Islam → Panjnad → Indus system',
        'Kabul': 'Kabul basin → Nowshera/Charsadda → Attock → Indus',
        'Swat': 'Upper Swat → Swat valley → Kabul → Indus'
    }
    selected = st.selectbox('Select chain', list(chains))
    st.success(chains[selected])

with hydraulic_tab:
    st.subheader('Indus Mainstem — Capacity / Routing Check')
    st.info(
        'This is a **simplified, steady-state capacity check**, not a full unsteady hydraulic '
        'simulation (e.g. HEC-RAS / MIKE 11) and not a cadastral inventory. It propagates one '
        'assumed inflow at Tarbela down the main Indus-stem structures and flags whether each '
        "structure's published *design* discharge capacity would be exceeded. It does **not** "
        'add tributary inflows (e.g. Kabul at Nowshera, the Punjab rivers joining near Panjnad) '
        'and does **not** model travel time or reservoir storage — so real observed discharges '
        'at downstream barrages are normally higher than a single-thread propagation implies.'
    )

    col1, col2 = st.columns(2)
    with col1:
        inflow = st.slider(
            'Assumed inflow at Tarbela (cusecs)', min_value=50_000, max_value=1_200_000,
            value=400_000, step=10_000,
            help='400,000 cusecs is a typical mid-Kharif order-of-magnitude figure; adjust to explore scenarios.'
        )
    with col2:
        loss_pct = st.slider(
            'Assumed reach transmission loss per structure (%)', min_value=0, max_value=20,
            value=0, step=1,
            help='Illustrative, user-set assumption — not measured loss data. Real reach losses vary '
                 'by discharge, season and channel condition; set to 0 to see capacity-only routing.'
        )

    routed = route_mainstem(inflow, reach_loss_pct=loss_pct)

    st.plotly_chart(
        {
            'data': [
                {'type': 'bar', 'name': 'Flow in (cusecs)', 'x': routed['Structure'], 'y': routed['Flow in (cusecs)']},
                {'type': 'bar', 'name': 'Design capacity (cusecs)', 'x': routed['Structure'], 'y': routed['Design capacity (cusecs)']},
            ],
            'layout': {'barmode': 'group', 'height': 420, 'margin': {'l': 0, 'r': 0, 't': 10, 'b': 0},
                       'legend': {'orientation': 'h', 'y': 1.1}},
        },
        use_container_width=True, config={'displaylogo': False}
    )

    st.dataframe(
        routed[['Structure', 'Design capacity (cusecs)', 'Flow in (cusecs)', 'Flow out (cusecs)', '% of capacity', 'Status']],
        use_container_width=True, hide_index=True
    )

    exceeded = routed[routed.Status.str.contains('Exceeds')]
    if not exceeded.empty:
        st.warning(f"At this inflow, {', '.join(exceeded.Structure)} would exceed published design capacity.")
    else:
        st.success('At this inflow (and loss assumption), no mainstem structure exceeds its published design capacity.')

    st.caption(KNOWN_TRAVEL_TIME_NOTE)

    with st.expander('Capacity data sources (per structure)'):
        for name in MAINSTEM_ORDER:
            st.markdown(f"- **{name}** — {CAPACITY[name]['capacity_cusecs']:,} cusecs. {CAPACITY[name]['source']}")

    st.markdown('#### Limitations')
    st.markdown(
        '- Capacities are published **design** figures, not live telemetry — verify against IRSA/WAPDA/FFD before engineering use.\n'
        '- Tributary inflows and off-take losses to canals/link canals are not netted out.\n'
        '- No unsteady flow, storage, or travel-time routing (e.g. flood-wave attenuation) is modeled.\n'
        '- Covers the Indus mainstem only, not the Jhelum/Chenab/Ravi/Sutlej system.\n'
        '- This does not constitute, and is not a substitute for, a cadastral (land-parcel) survey.'
    )

with data_tab:
    st.subheader('Filtered Data')
    st.download_button('⬇️ Download filtered CSV', assets.to_csv(index=False).encode('utf-8'), 'pakistan_water_assets_filtered.csv', 'text/csv')
    st.dataframe(assets, use_container_width=True, hide_index=True)
    st.markdown('### Add your own data')
    uploaded = st.file_uploader('Upload CSV or XLSX', type=['csv','xlsx'])
    if uploaded:
        try:
            user_df = pd.read_csv(uploaded) if uploaded.name.lower().endswith('.csv') else pd.read_excel(uploaded)
            st.success(f'Loaded {len(user_df):,} rows × {len(user_df.columns):,} columns.')
            st.dataframe(user_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f'Could not read the file: {e}')

with sources_tab:
    st.subheader('Authoritative references used to structure this app')
    st.markdown('- **WAPDA:** major dams, hydropower and water-development projects.')
    st.markdown('- **IRSA:** river flows, reservoirs, barrages and Indus-system water management.')
    st.markdown('- **Ministry of Water Resources:** major river maps and water-sector documents.')
    st.markdown('- **Government of Pakistan / Indus Water Treaty map:** major link canals and barrages.')
    st.markdown('#### Online references')
    st.markdown('- https://wapda.gov.pk/')
    st.markdown('- https://wapda.gov.pk/wapda-projects/')
    st.markdown('- https://pakirsa.gov.pk/')
    st.markdown('- https://www.mowr.gov.pk/')
    st.markdown('- https://ncc.gov.pk/SiteImage/Misc/files/Indus%20Water%20Treaty%20Map%20English%282%29.pdf')
    st.markdown('- https://www.pcrwr.gov.pk/water-body-inventory/')
    st.warning('Asset status can change. Verify current project status and exact engineering attributes against the responsible government agency before using the app for design, operations or formal reporting.')

st.divider()
st.caption(
    'Pakistan Rivers & Irrigation Explorer • Streamlit • Designed for educational, engineering '
    'visualization, GIS-data extension, and a sourced planning-level hydraulic capacity check '
    '(Hydraulic Model tab). Not a cadastral survey.'
)
