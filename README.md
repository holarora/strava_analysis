Work in progress...
## Strava Analysis Helper 📈  ##
This personal project is a handy tool that summarizes your activities on Strava.<br>
As a long time Strava user, I often found it challenging to track my activities and visualize my progress effectively. That is what inspired me to create this project.<br>
By toggling the Chart Type option, you can choose to view your stats in the following three formats: 
1. Distance🏃: A bar graph showing the total distance covered each week, perfect for tracking progress over time.
<img width="70%" alt="Screenshot 2024-11-16 at 23 23 14" src="https://github.com/user-attachments/assets/1099eac6-5248-45dc-a619-c30041d9f8bc">

2. Pace🕒: A line graph tracing your activities' speeds. We always want to stay on pace! (unlike me during week 4) 
<img width="70%" alt="Screenshot 2024-11-16 at 23 25 32" src="https://github.com/user-attachments/assets/bdb32d0c-fa42-403e-8b7e-a56ce78c8874">

3. Heatmap📅 : A calendar highlighting the days when an activity was recorded. The darker the shade, the greater the distance covered on that day.

### Tech Stack ###
- Strava API
- Python
- Chart.js
- JSON

### How to use ###
1. Clone this repository to your local machine.
2. Create a file client_secrets.txt, containing your Strava Client ID and Client Secret. ([ref for steps 2-5](https://developers.strava.com/docs/getting-started/))
3. Run the app/auth.py file, click Authenticate, and obtain authorization code in URL.
4. Paste authorization code in designated field in app/getToken.py file. Run the file and obtain access token in terminal. 
5. Paste access code in app/main.py. Run the file and access your local server. 
6. Enjoy your neatly presented stats!

### PRs are welcome! ###
If you run into any problems, feel free to make a pull request or contact me (@holarora). <br>
As I intend to use this project for my daily strava activities, they are currently tailored to my running plan. Therefore, this project assumes only activities with one category is uploaded. 

### To do ###
- [x] rendering
- [x] pace diagram: change distance to pace
- [ ] calendar: import actual data
- [x] calendar: x axis date
- [x] distance: title (marked as done for now)
- [ ] miles/km conversion
- [ ] automate authorization process




