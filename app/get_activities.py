from flask import Flask, jsonify, render_template
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_strava_data():
    access_token = "0b72f3e423e28dea22f07dbb7447312d4197699e"
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
            distance = round(activity.get("distance", 0) / 1000, 1)

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

        sorted_weekly_data = sorted(weekly_data.items())
        labels = [week for week, distances in sorted_weekly_data]
        stacked_data = [distances for week, distances in sorted_weekly_data]

        # Pad shorter weeks to have the same number of activities (stacked bars will need the same length for each group)
        max_activities = max(len(activities) for activities in stacked_data)
        for i in range(len(stacked_data)):
            stacked_data[i] += [0] * (max_activities - len(stacked_data[i]))  # Pad with 0 if a week has fewer activities

        chart_data = {
            "labels": labels,
            "datasets": []
        }

        color_palette = [
            "rgba(153, 102, 255, 0.6)",  # Light Purple
            "rgba(255, 99, 132, 0.6)",  # Light Red/Pink
            "rgba(75, 192, 192, 0.6)",  # Light Turquoise
            "rgba(255, 206, 86, 0.6)"  # Light Yellow
        ]

        border_palette = [
            "rgba(153, 102, 255, 1)",
            "rgba(255, 99, 132, 1)",
            "rgba(75, 192, 192, 1)",
            "rgba(255, 206, 86, 1)"
        ]

        # Create a dataset for each activity within a week
        for i in range(max_activities):
            dataset = {
                "label": f"Activity {i + 1}",
                "data": [week[i] for week in stacked_data],
                "backgroundColor": color_palette[i % 4],  # Cycle through 4 colors
                "borderColor": border_palette[i % 4],
                "borderWidth": 1
            }
            chart_data["datasets"].append(dataset)

        return jsonify(chart_data)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
