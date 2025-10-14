from flask import Flask, render_template, Response, redirect, url_for, request
import cv2  # For webcam integration
import serial  # For RFID integration
import time

app = Flask(__name__)

# Initialize webcam
camera = cv2.VideoCapture(0)

# Initialize RFID (COM12 포트 사용 예시)
try:
    arduino = serial.Serial(port='COM14', baudrate=9600, timeout=.1)
except serial.SerialException:
    print("error")
    arduino = None  # 에러 발생 시, 장치를 연결하지 않음

# Function to get RFID data
def get_rfid_data():
    if arduino:
        try:
            data = arduino.readline().decode('utf-8').strip()
            if data:
                print(data)
                return data
            else:
                None
        except:
            return None
    return None

# Function to stream video from the webcam
def gen_video():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Main Page - Rental/Return Selection
@app.route('/')
def main_page():
    return render_template('main.html')

# Info Confirmation Page - Confirm or Register User
@app.route('/info', methods=['GET', 'POST'])
def info_page():
    if request.method == 'POST':
        rfid_data = get_rfid_data()
        if rfid_data:  # if RFID is detected
            # Here you'd check if the user is registered, or proceed with registration
            return redirect(url_for('loading_page', action='rental'))
        else:
            # Manual registration logic here
            return render_template('info.html', error="No RFID detected. Register manually.")
    return render_template('info.html')

# Loading Page - Buffer for RFID/Webcam Activation
@app.route('/loading/<action>')
def loading_page(action):
    time.sleep(3)  # Simulate loading delay for RFID and webcam
    if action == 'rental':
        return redirect(url_for('rental_page'))
    elif action == 'return':
        return redirect(url_for('return_page'))

# Rental Page - Wait for object recognition (via webcam)
@app.route('/rental')
def rental_page():
    # Object recognition and other rental logic go here
    return render_template('rental.html')

# Rental Complete Page - Display rental details
@app.route('/rental_complete')
def rental_complete_page():
    rental_info = {"sensor": "Temperature Sensor", "return_date": "2024-10-25"}  # Example info
    return render_template('rental_complete.html', rental_info=rental_info)

# Return Page - Show remaining rental info and return items
@app.route('/return')
def return_page():
    # Logic to check borrowed items and remaining time
    borrowed_items = {"sensor": "Temperature Sensor", "remaining_time": "2 days"}
    return render_template('return.html', borrowed_items=borrowed_items)

# Return Complete Page - Confirm return and redirect to main
@app.route('/return_complete')
def return_complete_page():
    return render_template('return_complete.html')

# Error Handling Page
@app.route('/error')
def error_page():
    return render_template('error.html')

# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(gen_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route for RFID data
@app.route('/rfid_data')
def rfid_data():
    data = get_rfid_data()
    if data:
        print(data)
        return data
    else:
        return "No RFID data detected"

if __name__ == '__main__':
    app.run(debug=True)