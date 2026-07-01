import joblib
import numpy as np

class PatientPredictor:
    def __init__(self):
        self.model = joblib.load('patient_model.pkl')
        self.scaler = joblib.load('scaler.pkl')
    
    def predict(self, spo2, heart, sys, dia, ecg, mmhg):
        """
        Predict if patient is Normal or Abnormal
        Returns: (status, confidence)
        """
        features = np.array([[spo2, heart, sys, dia, ecg, mmhg]])
        features_scaled = self.scaler.transform(features)
        
        # Prediction
        prediction = self.model.predict(features_scaled)[0]
        confidence = self.model.predict_proba(features_scaled)[0]
        
        # Get probability
        if prediction == 'Normal':
            prob = confidence[list(self.model.classes_).index('Normal')] * 100
        else:
            prob = confidence[list(self.model.classes_).index('Abnormal')] * 100
        
        return prediction, prob
    
    def analyze_patient(self, spo2, heart, sys, dia, ecg, mmhg):
        """
        Detailed analysis with rules
        """
        status, confidence = self.predict(spo2, heart, sys, dia, ecg, mmhg)
        
        # Rule-based warnings
        warnings = []
        if spo2 < 95 or spo2 > 100:
            warnings.append(f"⚠️ SpO2 abnormal: {spo2}%")
        if heart < 60 or heart > 100:
            warnings.append(f"⚠️ Heart rate abnormal: {heart} BPM")
        if sys < 90 or sys > 140:
            warnings.append(f"⚠️ Systolic pressure abnormal: {sys}")
        if dia < 60 or dia > 90:
            warnings.append(f"⚠️ Diastolic pressure abnormal: {dia}")
        if ecg > 700:
            warnings.append(f"⚠️ ECG abnormal: {ecg}")
        if mmhg < 3 or mmhg > 5:
            warnings.append(f"⚠️ mmHg abnormal: {mmhg}")
        
        return {
            'status': status,
            'confidence': confidence,
            'warnings': warnings,
            'critical': len(warnings) >= 3
        }
