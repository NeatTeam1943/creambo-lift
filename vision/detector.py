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

    def predict_and_annotate(self, name: str, confidence_threshold=0.6):
        """
        Performs object detection and annotation on the specified image.

        Args:
        - name (str): Path to the image file.
        - confidence_threshold (float): Confidence threshold for object detection.

        Returns:
        - Annotated image (np.ndarray): Annotated image with bounding boxes and labels.
        """
        results = self.model.predict(name, conf=confidence_threshold)

        img = cv2.imread(name)

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

        return annotated_img

    def show(self, name: str, img: np.ndarray):
        """
        Displays the annotated image.

        Args:
        - name (str): Name of the window to display.
        - img (np.ndarray): Annotated image to display.

        Returns:
        - Annotated image (np.ndarray): The input annotated image.
        """
        cv2.imshow(name, img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return img
