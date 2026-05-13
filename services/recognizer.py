import cv2
import mediapipe as mp
from typing import List, Dict

class GestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7
        )
        self.gesture_map = {
            "THUMBS_UP": " موافق",
            "OPEN_PALM": " توقف",
            "POINTING": " إشارة"
        }

    def recognize(self, frame) -> Dict:
        """يتعرف على الحركات في إطار الفيديو"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        output = {
            "gestures": [],
            "landmarks": []
        }

        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                output["landmarks"].append(landmarks)
                gesture = self._classify_gesture(landmarks)
                if gesture:
                    output["gestures"].append(gesture)
        
        return output

    def _classify_gesture(self, landmarks) -> str:
        """يصنف الحركة بناءً على معالم اليد"""
        thumb_tip = landmarks.landmark[4]
        index_tip = landmarks.landmark[8]
        
        # تحليل الحركات (يمكن توسيعها)
        if thumb_tip.y < index_tip.y:
            return self.gesture_map["THUMBS_UP"]
        elif abs(thumb_tip.x - index_tip.x) > 0.1:
            return self.gesture_map["POINTING"]
        return None
