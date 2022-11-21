# trying out steamlit folium, since this already seems to have bi-directionality implemented.
# using folium with a geojson significantly imporved perfomance
# it seems very promising, however it turns out that styling of streamlit is extremely difficult.
# if i want to switch to dash, here's a nice forum answer on this:
# https://community.plotly.com/t/dash-and-folium-integration/5772

import streamlit as st
import pandas as pd
import numpy as np
# https://github.com/randyzwitch/streamlit-folium
from streamlit_folium import st_folium 
import folium
import plotly.express as px
import plotly.graph_objects as go

#st.set_page_config(layout="wide")


#with open("style.css") as f:
# st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_data(nrows):
    """
    Load the excel data into memory. Todo: update the excelfile to contain only necessary data (save ram) 
    and also turn into csv (or maybe just load the json?)
    """
    #with st.spinner(f"Loading max. {nrows} rows of data"):
    data = pd.read_excel("Grassland_ALLEMA-BDM-WBS_v.5.xlsx", "Data file", nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data.rename(columns={"länge": "lon", "breite": "lat"}, inplace=True)
    data["sömmerung"] = data["sömmerung"].apply(lambda x: x == 1)   
    st.success('Done!', icon="✅")
    return data

def get_bb_drawings(drawings):
    """
    Get the bounding box of all the drawings on the folium map. Input mus be the "all_drawings" dict from st_folium().
    Return value is a dict of bounding boxes, similar to get_bb_mapextent()
    """
    if(drawings):
        bbs = {}
        for idx, feature in enumerate(drawings):
            coords = feature["geometry"]["coordinates"][0]
            lng = [x[0] for x in coords]
            lat = [x[1] for x in coords]
            bb = {"minx": min(lng), "miny": min(lat), "maxx": max(lng), "maxy": max(lat)}
            bbs[idx] = bb
        return(bbs)

def get_bb_mapextent(map_extent):
    """
    Get the bounding box of the map extent of a foium map. Input must be the "bounds" dict of a folium map.
    Output is a dict 
    """
    bb = {"minx":map_extent["_southWest"]["lng"],"miny":map_extent["_southWest"]["lat"],"maxx":map_extent["_northEast"]["lng"],"maxy":map_extent["_northEast"]["lat"]}
    return(bb)

def filter_df(df,bb, x = "lon", y = "lat"):
    """
    Filter a dataframe (df) by a bounding box (bb, a dict with the entries xmin, xmax, ymin, ymax)). x and y specifiy the 
    column names of the lon (x) and lat (y) columns
    """
    df_filtered = df.loc[(data[y] > bb["miny"] ) & (data[x] > bb["minx"]) & (data[y] < bb["maxy"] ) & (data[x] < bb["maxx"]) ]
    return(df_filtered)


# Load 10,000 rows of data into the dataframe.
data = load_data(10000)

m = folium.Map(location=[46.89599, 8.31787], zoom_start=8,width="100%")
folium.plugins.Draw(draw_options={"polyline": False, "marker": False, "circlemarker": False, "polygon": False, "circle": False, 
"rectangle": {"repeatMode": False}}).add_to(m)

mark = folium.CircleMarker(radius = 3,weight = 0, fill_color = '#000000', fill_opacity = 1)
folium.GeoJson("geojson.json", marker = mark).add_to(m)

#folium.Polygon([[[46.976505, 7.580566,],[47.260592,7.580566],[47.260592, 8.4375],[46.976505,8.4375],[46.976505,7.580566]]]).add_to(m)
st.title("Biodiversitätsmonitor")


with st.sidebar:
	st.write("hello")

col1, col2 = st.columns([1, 1])

with col1:
    st_data = st_folium(m)


bb_mapextent = get_bb_mapextent(st_data["bounds"])
bb_drawings = get_bb_drawings(st_data["all_drawings"])

data_filter_mapextent = filter_df(data, bb_mapextent)

fig = go.Figure()

fig.add_trace(go.Box(y = data["artenreichtum"], name = "All Data",hoverinfo= "skip"))
fig.add_trace(go.Box(y = data_filter_mapextent["artenreichtum"],name = "Data in Extent",hoverinfo= "skip"))
fig.update_yaxes(title_text="Species Richness")

if bb_drawings:
    for idx, bb in bb_drawings.items():
        data_filterd_drawing = filter_df(data, bb)
        fig.add_trace(go.Box(y = data_filterd_drawing["artenreichtum"],name = f"Data in selection {idx+1}",hoverinfo= "skip"))

fig2 = go.Figure()

fig2.add_trace(go.Box(y = data["artenreichtum.neophyten"], name = "All Data",hoverinfo= "skip"))
fig2.add_trace(go.Box(y = data_filter_mapextent["artenreichtum.neophyten"],name = "Data in Extent",hoverinfo= "skip"))
fig2.update_yaxes(title_text="Species Richness Neophyten")



if bb_drawings:
    for idx, bb in bb_drawings.items():
        data_filterd_drawing = filter_df(data, bb)
        fig2.add_trace(go.Box(y = data_filterd_drawing["artenreichtum"],name = f"Data in selection {idx+1}",hoverinfo= "skip"))


with col2:
    st.plotly_chart(fig)
    st.plotly_chart(fig2)
