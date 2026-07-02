from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("score_rfc3.pkl")


team_map = {
    "Rajasthan Royals":1,
    "Royal Challengers Bengaluru":0.9,
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

    try:
        batting_name = request.form["batting_team"]
        bowling_name = request.form["bowling_team"]
        if batting_name == bowling_name:
            return render_template(
                   "index.html",
                   teams=team_map.keys(),
                   cities=city_map.keys(),
                   error="Batting team and Bowling team cannot be the same."
            )

        batting_team = team_map[batting_name]
        bowling_team = team_map[bowling_name]
            
        city = city_map[request.form["city"]]

        curr_run = float(request.form["curr_run"])
        ball_number = float(request.form["balls"])
        curr_wick = float(request.form["wicket"])
        partnership = float(request.form["partnership"])
    except (KeyError, ValueError):
        return render_template(
            "index.html",
            teams=team_map.keys(),
            cities=city_map.keys(),
            error="Something in the form was missing or invalid. Please check your inputs and try again."
        )


    if ball_number <= 0:
        return render_template(
            "index.html",
            teams=team_map.keys(),
            cities=city_map.keys(),
            error="Please bowl at least 1 ball (set the Overs/Ball dial) before predicting."
        )


    balls_left = 120 - ball_number

    cr = curr_run / ball_number


    rpw = curr_run / curr_wick if curr_wick != 0 else 0


    est_score = cr * 20

    rratr = est_score - curr_run


    data = np.array([[
        city,
        batting_team,
        bowling_team,
        curr_run,
        ball_number,
        balls_left,
        curr_wick,
        cr,
        rpw,
        est_score,
        rratr,
        partnership
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
