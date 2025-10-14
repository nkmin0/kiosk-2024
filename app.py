from flask import Flask, render_template, Response, redirect, url_for, jsonify
import serial
import cv2

app = Flask(__name__)

# 시리얼 포트를 초기에 한 번만 설정
arduino = None
try:
    arduino = serial.Serial(port='COM14', baudrate=9600, timeout=.1)
    print("Serial connection established.")
except serial.SerialException as e:
    print(f"Failed to connect to Arduino: {e}")

last_rfid_data = ''
camera = cv2.VideoCapture(0)  # 기본 카메라를 사용

# RFID 데이터를 읽는 함수
def read_rfid_once():
    global last_rfid_data
    if arduino and arduino.is_open:
        if arduino.in_waiting > 0:
            try:
                rfid_data = arduino.readline().decode('utf-8').strip()
                if rfid_data:
                    last_rfid_data = rfid_data
                    print(f"RFID Data: {rfid_data}")
            except serial.SerialException as e:
                print(f"Failed to read from Arduino: {e}")
    return last_rfid_data

def generate_video():
    """웹캠으로부터 프레임을 가져와 스트리밍하는 함수"""
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/info_page')
def info_page():
    """RFID 인식 페이지. 필요한 경우 RFID 데이터를 읽습니다."""
    read_rfid_once()  # 이 페이지에 들어올 때마다 RFID를 확인
    return render_template('info.html', rfid_scanned=bool(last_rfid_data))

@app.route('/video_feed')
def video_feed():
    """비디오 피드를 제공하는 라우트"""
    return Response(generate_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_rfid')
def get_rfid():
    """RFID 데이터를 가져오는 API"""
    rfid_data = read_rfid_once()
    return jsonify({"rfid_data": rfid_data})

@app.route('/loading_page')
def loading_page():
    return render_template('loading.html')

@app.route('/rental_page')
def rental_page():
    return render_template('rental.html')

@app.route('/rental_complete_page')
def rental_complete():
    return render_template('rental_complete.html')

@app.route('/return_page')
def return_page():
    return render_template('return.html')

@app.route('/return_complete_page')
def return_complete():
    return render_template('return_complete.html')

@app.route('/error')
def error_page():
    return render_template('error.html')

if __name__ == '__main__':
    try:
        app.run(debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print("Server stopped")
    finally:
        # 애플리케이션 종료 시 카메라와 시리얼 포트 닫기
        camera.release()
        if arduino and arduino.is_open:
            arduino.close()
