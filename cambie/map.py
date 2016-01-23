import folium

VANCOUVER = (49.2511587, -123.1344104)

def vancouver():
    m = folium.Map(location=VANCOUVER, zoom_start=12)
