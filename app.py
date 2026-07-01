from flask import Flask, render_template, jsonify
import requests
from ml_predictor import PatientPredictor
import pandas as pd
from datetime import datetime

app = Flask(__name__)

PHP_LATEST_URL = "http://esskay-012024.live/abulance1/get_data.php"
PHP_ALL_URL = "http://esskay-012024.live/abulance1/get_data.php?action=all"

# Initialize ML predictor
predictor = PatientPredictor()


@app.route('/')
def index():
    return render_template('index.html')


# ------------------- LATEST DATA -------------------
@app.route('/api/latest')
def get_latest():
    print("🔍 Fetching LATEST...")
    try:
        response = requests.get(PHP_LATEST_URL, timeout=10)
        data = response.json()
        result = data[0] if isinstance(data, list) else data

        # Read sensor values
        spo2 = int(result.get('spo2', 0))
        heart = int(result.get('heart', 0))
        sys = int(result.get('sys', 0))
        dia = int(result.get('dia', 0))
        ecg = int(result.get('ecg', 0))
        mmhg = float(result.get('mmhg', 0))
        tilt = float(result.get('tilt', 0))
        gas = float(result.get('gas', 0))

        # GPS
        latitude = float(result.get('latitude', 0))
        longitude = float(result.get('longitude', 0))

        # Servo Box Status
        box1 = result.get('box1', 'closed')
        box2 = result.get('box2', 'closed')

        # ML Prediction
        analysis = predictor.analyze_patient(spo2, heart, sys, dia, ecg, mmhg)

        result['prediction'] = analysis['status']
        result['confidence'] = round(analysis['confidence'], 2)
        result['warnings'] = analysis['warnings']
        result['critical'] = analysis['critical']

        # Add extra values
        result['tilt'] = tilt
        result['gas'] = gas
        result['latitude'] = latitude
        result['longitude'] = longitude
        result['box1'] = box1
        result['box2'] = box2

        print(f"🤖 Prediction: {analysis['status']} ({analysis['confidence']:.1f}%)")
        return jsonify(result)

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500


# ------------------- ALL DATA -------------------
@app.route('/api/data')
def get_data():
    print("🔍 Fetching ALL data...")
    try:
        response = requests.get(PHP_ALL_URL, timeout=10)
        data = response.json()

        for row in data:
            spo2 = int(row.get('spo2', 0))
            heart = int(row.get('heart', 0))
            sys = int(row.get('sys', 0))
            dia = int(row.get('dia', 0))
            ecg = int(row.get('ecg', 0))
            mmhg = float(row.get('mmhg', 0))

            tilt = float(row.get('tilt', 0))
            gas = float(row.get('gas', 0))
            latitude = float(row.get('latitude', 0))
            longitude = float(row.get('longitude', 0))
            box1 = row.get('box1', 'closed')
            box2 = row.get('box2', 'closed')

            analysis = predictor.analyze_patient(spo2, heart, sys, dia, ecg, mmhg)

            row['prediction'] = analysis['status']
            row['confidence'] = round(analysis['confidence'], 2)
            row['critical'] = analysis['critical']

            row['tilt'] = tilt
            row['gas'] = gas
            row['latitude'] = latitude
            row['longitude'] = longitude
            row['box1'] = box1
            row['box2'] = box2

        print(f"✅ Got {len(data)} rows with predictions!")
        return jsonify(data)

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500


# ------------------- EXPORT REPORT -------------------
@app.route('/api/export-report')
def export_report():
    print("📊 Exporting report...")
    try:
        response = requests.get(PHP_ALL_URL, timeout=10)
        data = response.json()

        for row in data:
            spo2 = int(row.get('spo2', 0))
            heart = int(row.get('heart', 0))
            sys = int(row.get('sys', 0))
            dia = int(row.get('dia', 0))
            ecg = int(row.get('ecg', 0))
            mmhg = float(row.get('mmhg', 0))

            analysis = predictor.analyze_patient(spo2, heart, sys, dia, ecg, mmhg)

            row['prediction'] = analysis['status']
            row['confidence'] = round(analysis['confidence'], 2)

        df = pd.DataFrame(data)

        filename = f"patient_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(filename, index=False)

        print(f"✅ Report exported: {filename}")
        return jsonify({'success': True, 'file': filename})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("🚀 Flask with ML starting...")
    app.run(debug=True, host='0.0.0.0', port=5000)