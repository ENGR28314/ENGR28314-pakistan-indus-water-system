import plotly.graph_objects as go

def make_network(df):
    nodes = {
        'Upper Indus':(35.9,74.58),'Tarbela':(34.08,72.70),'Kabul':(33.99,72.24),'Jhelum':(33.15,73.65),'Chenab':(32.67,74.46),'Ravi':(31.22,73.84),'Sutlej':(30.66,73.08),'Panjnad':(29.35,71.05),'Lower Indus':(28.43,69.74),'Arabian Sea':(25.38,68.31)
    }
    edges=[('Upper Indus','Tarbela'),('Kabul','Tarbela'),('Tarbela','Lower Indus'),('Jhelum','Chenab'),('Chenab','Panjnad'),('Ravi','Panjnad'),('Sutlej','Panjnad'),('Panjnad','Lower Indus'),('Lower Indus','Arabian Sea')]
    fig=go.Figure()
    for a,b in edges:
        y1,x1=nodes[a]; y2,x2=nodes[b]
        fig.add_trace(go.Scatter(x=[x1,x2],y=[y1,y2],mode='lines',line={'width':3},showlegend=False,hoverinfo='skip'))
    fig.add_trace(go.Scatter(x=[p[1] for p in nodes.values()],y=[p[0] for p in nodes.values()],mode='markers+text',text=list(nodes.keys()),textposition='top center',marker={'size':14},name='River nodes',hovertemplate='%{text}<extra></extra>'))
    fig.update_layout(height=580,margin={'l':20,'r':20,'t':20,'b':20},xaxis_title='Longitude',yaxis_title='Latitude',yaxis={'scaleanchor':'x','scaleratio':1})
    return fig
