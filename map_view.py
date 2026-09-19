import plotly.graph_objects as go
from coordinates import POINTS as _SOURCED_POINTS

# (lat, lon) view, kept for the RIVER_LINES fallback logic below.
POINTS = {name: (lat, lon) for name, (lat, lon, _status, _source) in _SOURCED_POINTS.items()}

_STATUS_LABEL = {'verified': 'verified', 'approximate': 'approximate', 'representative': 'representative (unverified)'}

RIVER_LINES = {
'Indus':[(35.9,74.58),(34.08,72.70),(33.99,72.24),(32.44,71.39),(30.70,70.65),(28.43,69.74),(27.71,68.86),(25.38,68.31)],
'Jhelum':[(34.37,73.47),(33.15,73.65),(32.77,73.45),(31.24,72.12)],
'Chenab':[(32.67,74.46),(32.41,73.75),(32.22,73.75),(31.24,72.12),(29.35,71.05)],
'Ravi':[(32.67,74.2),(31.22,73.84),(30.49,72.21),(29.35,71.05)],
'Sutlej':[(30.66,73.08),(29.91,72.26),(29.35,71.05)],
'Kabul':[(34.15,71.78),(33.99,72.24)],
'Swat':[(35.0,72.35),(34.15,71.78)]
}

def make_map(df, show_labels=True):
    fig = go.Figure()
    wanted = set(df[df.asset_type=='River'].name)
    for name, pts in RIVER_LINES.items():
        if wanted and name not in wanted and name not in {'Indus','Jhelum','Chenab','Ravi','Sutlej','Kabul','Swat'}:
            continue
        fig.add_trace(go.Scattermapbox(lat=[x[0] for x in pts], lon=[x[1] for x in pts], mode='lines', name=name, line={'width':4}, hovertext=name, hoverinfo='text'))
    styles = {'Dam':('circle',11),'Barrage':('square',10),'Confluence':('diamond',11)}
    for typ,(symbol,size) in styles.items():
        sub=df[df.asset_type==typ]
        if sub.empty: continue
        lat=[]; lon=[]; text=[]; hover=[]
        for _,r in sub.iterrows():
            p=_SOURCED_POINTS.get(r['name'])
            if p:
                plat, plon, status, source = p
                lat.append(plat); lon.append(plon); text.append(r['name'])
                hover.append(f"{r['name']}<br>{_STATUS_LABEL.get(status, status)}<br><i>{source}</i>")
        fig.add_trace(go.Scattermapbox(lat=lat,lon=lon,mode='markers+text' if show_labels else 'markers',text=text if show_labels else None,textposition='top center',marker={'size':size,'symbol':symbol},name=typ,hovertext=hover,hoverinfo='text'))
    fig.update_layout(mapbox={'style':'open-street-map','center':{'lat':30.7,'lon':71.5},'zoom':4.8},height=700,margin={'l':0,'r':0,'t':10,'b':0},legend={'orientation':'h','y':0.01})
    return fig
