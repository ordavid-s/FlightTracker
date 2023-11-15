from flask import Flask, render_template, session, url_for
import folium

app = Flask(__name__)
app.secret_key = 'veryyy_secret'  # Change this to a secret key for your application



@app.route('/')
def index():
    if 'selected_networks' not in session:
        session['selected_networks'] = []
    sidebar_width = 200
    # Create a map centered at a specific location
    tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
    m = folium.Map(location=[31.425133, 34.382742],
                   zoom_start=15,
                   tiles=tiles,
                   attr='Esri',
                   name='Esri Satellite',
                   )

    # Add a marker
    for loc in session['selected_networks']:
        folium.Marker(location=loc, popup='Center').add_to(m)

    ess_list = ["Location 1 ", "Location 2", "Location 3"]
    bss_list = ["a", "b", "c"]

    # Save the map as an HTML string
    map_html = m._repr_html_()

    # Render the template with the map
    return render_template('index.html',
                           map_html=map_html,
                           ess_list=ess_list,
                           bss_list=bss_list,
                           sidebar_width=sidebar_width)


@app.route('/update_networks', methods=['POST'])
def update_networks():
    session['selected_networks'].append([31.425133, 34.382742])


if __name__ == '__main__':
    app.run(debug=True)
