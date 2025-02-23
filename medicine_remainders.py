from flask import Flask, request, jsonify
import schedule
import time
import threading
from datetime import datetime
from plyer import notification

app = Flask(__name__)
users = {}
medicines = {}

@app.route('/add_user', methods=['POST'])
def add_user():
    user_id = request.json['user_id']
    name = request.json['name']
    users[user_id] = name
    return jsonify({'message': 'User added'})

@app.route('/add_medicine', methods=['POST'])
def add_medicine():
    user_id = request.json['user_id']
    med_name = request.json['med_name']
    time = request.json['time']
    medicines[user_id] = {'med_name': med_name, 'time': time}
    schedule.every().day.at(time).do(show_notification, user_id, med_name)
    return jsonify({'message': 'Medicine reminder set'})

def show_notification(user_id, med_name):
    user_name = users.get(user_id, 'User')
    notification.notify(title='Medicine Reminder', message=f'{user_name}, take {med_name}', timeout=5)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_scheduler, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)
