from flask import Flask, jsonify, render_template
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_strava_data():
    access_token = "0c8b63a4a9554bbca441d52cfe2137cb751b7996"
    before_epoch = 1731330329
    after_epoch = 1728259200
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "after": after_epoch,
        "before": before_epoch,
        "page": 1,
        "per_page": 200
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        activities = response.json()

        weekly_data = {}

        for activity in activities:
            distance = activity.get("distance", 0)
            start_date_str = activity.get('start_date_local')
            if isinstance(start_date_str, str):
                start_date = datetime.fromisoformat(start_date_str)
            else:
                start_date = datetime.fromtimestamp(activity['start_date_local'])

            start_of_week = start_date - timedelta(days=start_date.weekday())
            week_str = start_of_week.strftime('%Y-%m-%d')

            if week_str not in weekly_data:
                weekly_data[week_str] = []


            weekly_data[week_str].append(distance)


        labels = list(weekly_data.keys())
        stacked_data = [weekly_data[week] for week in labels]

        # Pad shorter weeks to have the same number of activities (stacked bars will need the same length for each group)
        max_activities = max(len(activities) for activities in stacked_data)
        for i in range(len(stacked_data)):
            stacked_data[i] += [0] * (max_activities - len(stacked_data[i]))  # Pad with 0 if a week has fewer activities

        chart_data = {
            "labels": labels,
            "datasets": []
        }

        # Create a dataset for each activity within a week
        for i in range(max_activities):
            dataset = {
                "label": f"Activity {i + 1}",
                "data": [week[i] for week in stacked_data],
                "backgroundColor": f"rgba({75 + (i * 30)}, 192, 192, 0.6)",
                "borderColor": "rgba(75, 192, 192, 1)",
                "borderWidth": 1
            }
            chart_data["datasets"].append(dataset)

        return jsonify(chart_data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
