from detector import Detector
import cv2


def main():
    annotator = Detector('weights/best.pt')

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break 
        
        _ = annotator.draw_threshold(frame)
        annotated_frame, detections = annotator.predict_and_annotate(frame)

        if len(detections['XYXY']) != 0:
            _, y1, _, y2 = detections["XYXY"][0]
            center_y = (y1 + y2) // 2

            action = annotator.apply_threashold(frame, center_y)
            print(f'{action=}')

        cv2.imshow('Frame', annotated_frame)

        key = cv2.waitKey(1)
        
        if key == ord('q'):
            break

if __name__ == "__main__":
    main()
