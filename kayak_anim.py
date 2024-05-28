#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 21:45:06 2024

@author: dellud
"""

import geopandas as gpd
import pandas as pd
import pydeck as pdk
from shapely.geometry import MultiLineString, LineString


# Charger le fichier GPX
gpx_path = 'stockholm_archipielago.gpx'
gpx_data = gpd.read_file(gpx_path, layer='tracks')

# Extraire les coordonnées des géométries
coords = []
for geom in gpx_data.geometry:
    if isinstance(geom, MultiLineString):
        for line in geom.geoms:
            coords.extend([[coord[0], coord[1]] for coord in line.coords])  # Longitude, Latitude
    elif isinstance(geom, LineString):
        coords.extend([[coord[0], coord[1]] for coord in geom.coords])  # Longitude, Latitude

#définiti
timestamps = pd.date_range(start='2023-01-01', periods=len(coords), freq='S').astype(int) / 10**9

data = [
        { 
        "name" : "Stockholm Archipelago", 
        "path" : coords,
        "timestamp" : timestamps.tolist()
        }
        ]
# Créer un DataFrame des coordonnées
df = pd.DataFrame(data)

# Ajouter un timestamp pour chaque point pour l'animation
# df['timestamp'] = pd.date_range(start='2023-01-01', periods=len(coords), freq='S').astype(int) / 10**9


# Configurer la couche d'animation
animated_layer = pdk.Layer(
    type="TripsLayer",
    data=df,
    get_timestamps='timestamp',
    get_color=[255, 0, 0],
    get_path="path",
    width_scale=1,
    width_min_pixels=2,
    widthMaxPixels=1, 
    get_width=5,
    trail_length=len(coords),  # Longueur de la traînée en secondeslen(coords) - 1
    current_time=df['timestamp'][0][len(coords)-1] # Temps initial
)

# layer = pdk.Layer(
#     type="PathLayer",
#     data=df,
#     widthUnits='meters',
#     widthScale=1,
#     # widthMinPixels=5,
#     widthMaxPixels=1, 
#     pickable=True,
#     get_color=[255, 0, 0],
#     get_path="path",
#     # width_scale=20,
#     get_width=5
# )


# Configurer la vue de la carte
start_coords = [59.154326, 18.663476]

view_state = pdk.ViewState(
    latitude=start_coords[0],
    longitude=start_coords[1],
    zoom=10.5
)

# Créer la carte
r = pdk.Deck(
    layers=[animated_layer],
    initial_view_state=view_state,
    map_style='dark',
    tooltip={"text": "Longitude: {lon}\nLatitude: {lat}"}
)

# Afficher la carte
r.to_html('animated_map.html', notebook_display=False)