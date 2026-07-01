from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("final_score_predictor2.pkl")


team_map = {
    "Rajasthan Royals":1,
    "Royal Challengers Bengaluru":0.9,
    "Royal Challengers Bangalore":0.9,
    "Gujarat Titans":0.8,
    "Punjab Kings":0.7,
    "Mumbai Indians":0.6,
    "Sunrisers Hyderabad":0.5,
    "Lucknow Super Giants":0.4,
    "Chennai Super Kings":0.3,
    "Delhi Capitals":0.2,
    "Kolkata Knight Riders":0.1
}


city_map = {
    "Dharamsala":1,
    "Visakhapatnam":0.93,
    "New Chandigarh":0.81,
    "Delhi":0.87,
    "Kolkata":0.75,
    "Bengaluru":0.69,
    "Hyderabad":0.63,
    "Jaipur":0.57,
    "Ahmedabad":0.49,
    "Mumbai":0.43,
    "Guwahati":0.37,
    "Mohali":0.30,
    "Lucknow":0.24,
    "Pune":0.18,
    "Chennai":0.12,
    "Navi Mumbai":0.06
}


@app.route("/")
def home():
    return render_template(
        "index.html",
        teams=team_map.keys(),
        cities=city_map.keys()
    )


@app.route("/predict", methods=["POST"])
def predict():

    batting_team = team_map[request.form["batting_team"]]
    bowling_team = team_map[request.form["bowling_team"]]
    city = city_map[request.form["city"]]


    curr_run = float(request.form["curr_run"])
    ball_number = float(request.form["balls"])
    curr_wick = float(request.form["wicket"])


    cr = curr_run / ball_number


    rpw = curr_run / curr_wick if curr_wick != 0 else 0


    est_score = cr * 20


    data = np.array([[
        city,
        batting_team,
        bowling_team,
        curr_run,
        ball_number,
        curr_wick,
        cr,
        rpw,
        est_score
    ]])


    prediction = model.predict(data)[0]


    prediction = round(prediction)

    low = prediction - 2
    high = prediction + 2


    return render_template(
        "result.html",
        score=f"{low} - {high}"
    )


if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
