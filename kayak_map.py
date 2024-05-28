#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 19:10:10 2024

@author: dellud
"""

import geopandas as gpd
import folium
from folium.plugins import TimestampedGeoJson

# Charger le fichier GPX
gpx_path = 'stockholm_archipielago.gpx'
gpx_data = gpd.read_file(gpx_path, layer='tracks')

# Créer une carte centrée sur le point starts_coord (à modifier) 
start_coords = [59.154326, 18.663476]
map = folium.Map(location=start_coords, zoom_start=10.5)

# Traiter chaque ligne dans le fichier GPX
folium.GeoJson(gpx_data).add_to(map)

# Sauvegarder la carte en HTML
map.save('map.html')

