from flask import Flask, jsonify, render_template, request
import requests
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def get_strava_data():
    access_token = "44f011e26cbdcb8c0889774bd6a2a662f21d3dc4"
    after_epoch = 1728259200
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "after": after_epoch,
        "page": 1,
        "per_page": 200
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        activities = response.json()

        chart_type = request.args.get('chart_type', 'weekly_distance')

        if chart_type == 'weekly_distance':
            return jsonify(get_weekly_distance_data(activities))
        elif chart_type == 'pace':
            return jsonify(get_pace_data(activities))
        elif chart_type == 'calendar':
            return jsonify(get_calendar_data(activities))
        else:
            return jsonify({"error": "Unsupported chart type"}), 400
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        return jsonify({"error": "Failed to retrieve data"}), 500


def get_weekly_distance_data(activities):
    weekly_data = {}

    for activity in activities:
        distance = round(activity.get("distance", 0) / 1000, 1)

        start_date_str = activity.get('start_date_local')
        start_date = datetime.fromisoformat(start_date_str)
        start_of_week = start_date - timedelta(days=start_date.weekday())
        week_str = start_of_week.strftime('%Y-%m-%d')

        if week_str not in weekly_data:
            weekly_data[week_str] = []

        weekly_data[week_str].append(distance)

    sorted_weekly_data = sorted(weekly_data.items())
    labels = [week for week, distances in sorted_weekly_data]
    stacked_data = [distances for week, distances in sorted_weekly_data]

    max_activities = max(len(activities) for activities in stacked_data)
    for i in range(len(stacked_data)):
        stacked_data[i] += [0] * (max_activities - len(stacked_data[i]))

    chart_data = {
        "labels": labels,
        "datasets": []
    }

    color_palette = [
        "rgba(153, 102, 255, 0.6)",
        "rgba(255, 99, 132, 0.6)",
        "rgba(75, 192, 192, 0.6)",
        "rgba(255, 206, 86, 0.6)"
    ]
    border_palette = [
        "rgba(153, 102, 255, 1)",
        "rgba(255, 99, 132, 1)",
        "rgba(75, 192, 192, 1)",
        "rgba(255, 206, 86, 1)"
    ]

    for i in range(max_activities):
        dataset = {
            "label": f"Activity {i + 1}",
            "data": [week[i] for week in stacked_data],
            "backgroundColor": color_palette[i % 4],
            "borderColor": border_palette[i % 4],
            "borderWidth": 1
        }
        chart_data["datasets"].append(dataset)

    return chart_data


def get_pace_data(activities):
    weekly_data = {}

    for activity in activities:
        distance = round(activity.get("distance", 0) / 1000, 1)
        moving_time = round(activity.get("moving_time", 0) / 60, 1)
        pace = moving_time / distance if distance != 0 else 0

        start_date_str = activity.get('start_date_local')
        start_date = datetime.fromisoformat(start_date_str)
        start_of_week = start_date - timedelta(days=start_date.weekday())
        week_str = start_of_week.strftime('%Y-%m-%d')

        if week_str not in weekly_data:
            weekly_data[week_str] = []

        weekly_data[week_str].append(pace)

    sorted_weekly_data = sorted(weekly_data.items())
    labels = [week for week, paces in sorted_weekly_data]
    speeds = [paces for week, paces in sorted_weekly_data]

    chart_data = {
        "labels": labels,
        "datasets": [{
            "label": 'Max Speed (km/h)',
            "data": speeds,
            "borderColor": 'rgba(75, 192, 192, 1)',
            "backgroundColor": 'rgba(75, 192, 192, 0.2)',
            "fill": False,
            "borderWidth": 1
        }]
    }

    return chart_data


def get_calendar_data(activities):
    daily_data = defaultdict(float)

    for activity in activities:
        distance = round(activity.get("distance", 0) / 1000, 1)

        start_date_str = activity.get('start_date_local')
        start_date = datetime.fromisoformat(start_date_str)

        date_str = start_date.strftime('%Y-%m-%d')
        daily_data[date_str] += distance

    chart_data = {
        "datasets": [{
            "label": 'Activity Distance',
            "data": []
        }]
    }

    print(f"Daily Data: {daily_data}")

    for date, distance in daily_data.items():
        chart_data["datasets"][0]["data"].append({
            "x": datetime.strptime(date, '%Y-%m-%d').timestamp() * 1000,
            "y": datetime.strptime(date, '%Y-%m-%d').month,
            "v": distance
        })

    return chart_data


if __name__ == '__main__':
    app.run(debug=True)
