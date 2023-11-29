from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    # Flask will look for html files inside templates folder by default.
    return render_template('home.html')


# <> -> special Flask syntax, denotes that users can enter values for these 2 parameters
@app.route('/api/v1/<station>/<date>')
def about(station, date):
    temperature = 23
    return {"station": station, "date": date, "temperature": temperature}


# debug=True will allow us to see errors on the webpage.
if __name__ == '__main__':
    app.run(debug=True)
