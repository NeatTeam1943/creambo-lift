from ultralytics import YOLO
import supervision as sv
import cv2
import numpy as np


class Detector:
    """
    A class for performing object detection and annotation using YOLO model.

    Attributes:
    - model_weights (str): Path to the YOLO model weights.
    """

    def __init__(self, model_weights):
        """
        Initializes the Detector class.

        Args:
        - model_weights (str): Path to the YOLO model weights.
        """
        self.model = YOLO(model_weights)

        self.box_annotator = sv.BoxAnnotator(
            thickness=2,
            text_thickness=1,
            text_scale=0.35
        )

    def predict_and_annotate(self, img: np.ndarray, confidence_threshold=0.6):
        """
        Performs object detection and annotation on the specified image.

        Args:
        - img (np.ndarray): Image frame captured from the camera.
        - confidence_threshold (float): Confidence threshold for object detection.

        Returns:
        - Annotated image (np.ndarray): Annotated image with bounding boxes and labels.
        - dict<str, any>: dict that contains the xyxy, conf, class and the lable of the detected object 
        """
        results = self.model.predict(img, conf=confidence_threshold, verbose=False)

        detections = sv.Detections.from_yolov8(results[0])

        labels = [
            f'Creambo:{confidence:.2f}'
            for _, confidence, _, _
            in detections
        ]

        annotated_img = self.box_annotator.annotate(
            scene=img,
            detections=detections,
            labels=labels,
        )

        return annotated_img, {"XYXY": detections.xyxy, "CONFIDENCE": detections.confidence, "CLASS": detections.class_id, "LABEL": labels}

    def draw_threshold(self, frame, line_delta: int = 200):
        """
        Draws 2 lines which show the safe distance in which the creambo needs to be at.

        Args:
        - frame (np.ndarray): Input frame to draw lines on.
        - line_delta (int): The delta distance between the lines. Default is 200.

        Returns:
        - frame (np.ndarray): Frame with drawn lines.
        """
        height, width, _ = frame.shape

        middle_height = height // 2
        added_distance = line_delta // 2

        cv2.line(frame, (0, middle_height - added_distance),
                 (width, middle_height - added_distance), (0, 255, 0), 2)
        cv2.line(frame, (0, middle_height + added_distance),
                 (width, middle_height + added_distance), (255, 0, 0), 2)

        return frame

    def __threashold_check(self, frame, center_y: int, line_delta: int = 200):
        """
        Checks if the creambo is in the safe distance.

        Args:
        - frame (np.ndarray): Input frame to check.
        - center_y (int): The y coordinate of the creambo center.
        - line_delta (int): The delta distance between the lines. Default is 200.

        Returns:
        - bool: True if the creambo is in the safe distance, False otherwise.
        - float: The difference between the safe distance middle point and the creambo's current position.
        """
        height, _, _ = frame.shape

        middle_height = height // 2
        added_distance = line_delta // 2

        lower_line_height = middle_height + added_distance
        upper_line_height = middle_height - added_distance

        distance_from_middle = center_y - middle_height

        if lower_line_height < center_y < upper_line_height:
            return True, distance_from_middle

        return False, distance_from_middle

    def apply_threashold(self, frame, center_y, line_delta=200, move_distance=50, font=cv2.FONT_HERSHEY_SIMPLEX,
                         font_scale=0.7, font_thickness=2):
        """
        Determines and displays the action needed based on the detected object's position.

        Args:
        - frame (np.ndarray): Input frame to check.
        - center_y (int): The y coordinate of the creambo center.
        - line_delta (int): The delta distance between the lines. Default is 200.
        - move_distance (int): Desired distance to move up/down. Default is 50.
        - font (int): Font type for cv2.putText. Default is cv2.FONT_HERSHEY_SIMPLEX.
        - font_scale (float): Font scale for cv2.putText. Default is 0.7.
        - font_thickness (int): Font thickness for cv2.putText. Default is 2.

        Returns:
        - str: Action message based on the detected object's position.
        """
        is_safe, distance = self.__threashold_check(
            frame, center_y, line_delta)

        action = ""
        if is_safe:
            action = "Creambo is within the safe distance!"
        else:
            if distance > 0:
                action = f"Move Creambo up by {abs(distance)} pixels"
            else:
                action = f"Move Creambo down by {abs(distance)} pixels"

        cv2.putText(frame, action, (20, 50), font, font_scale,
                    (255, 255, 255), font_thickness)

        return action
