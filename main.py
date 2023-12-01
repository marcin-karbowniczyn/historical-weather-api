from flask import Flask, render_template, jsonify
import pandas as pd

# Template engine Flaska domyślnie nie renderuje HTML, a jako plain string, żeby pozwolić mu na renderowanie HTML,
# musimy dodać |safe za zmienną w pliku html (tutaj jest w home.html)
app = Flask(__name__)

stations = pd.read_csv('data_small/stations.txt', skiprows=17)
stations['LOCATION'] = stations['STANAME                                 ']
stations_to_display = stations[['STAID', 'LOCATION', 'CN']]


@app.route('/')
def home():
    # Flask will look for html files inside templates folder by default.
    return render_template('home.html', data=stations_to_display.to_html())


# <> -> special Flask syntax, denotes that users can enter values for these 2 parameters
# If I return a dictionary, Flask will automatically convert it to JSON, therefore I don't need to use jsonify().
# Although it's good to be aware of how does it work behin the scenes.
@app.route('/api/v1/<station>/<date>')
def station_on_day_data(station, date):
    try:
        # Funckja zfill() bierze string i dopełnia go zerami na podaną długość -> station = 10 -> station.zfill(6) = '000010'
        filename = f"data_small/TG_STAID{station.zfill(6)}.txt"
        df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
        temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10

        # Nie muszę wpisywać jsonify(), Flask zrobi to automatycznie jak zobaczy obiekt którzy jest JSON serializable, ale wolałem sobie tak wpisać, żeby pamiętać
        return jsonify({"station": station, "date": date, "temperature": temperature})
    except TypeError:
        return {"error": "TypeError",
                "description": "Wrong date or index format. Make sure index is an integer, and a date is in format YYYY-MM-DD"}


# All results from one station
@app.route('/api/v1/<station>')
def all_data(station):
    filename = f"data_small/TG_STAID{station.zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    # Opcja records tworzy list of dicts (konwertuje dataframe w list of dicts), gdzie każdy dict to jeden row/rekord
    return df.to_dict(orient="records")


# All results from one staton in a specific year
@app.route('/api/v1/yearly/<station>/<year>')
def yearly(station, year):
    filename = f"data_small/TG_STAID{station.zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return result


# debug=True will allow us to see errors on the webpage.
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Port is set default to 5000, but we can explecitly specify it to something else, like 5001.
