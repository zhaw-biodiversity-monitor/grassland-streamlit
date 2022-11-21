
## Grassland explorer with streamlit

Trying out steamlit-folium, since this already seems to have bi-directionality implemented.

- using folium with a geojson significantly imporved perfomance
- it seems very promising, streamlit-folium has many out of the box solution (drawing, extent of canvas etc)
- however it turns out that styling of streamlit is extremely difficult.
- if i want to switch to dash, here's a nice forum answer on this: https://community.plotly.com/t/dash-and-folium-integration/5772



```
# creates a minimal environments.yml file, only from the packages installed explicitly.
# somehow, pandas is missing here..why?
conda env export --from-history > environment-minimal.yml

# creates a requirements.txt file.. 
pip list --format=freeze > requirements.txt 

```