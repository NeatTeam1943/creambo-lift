from detector import Detector


def main():
    annotator = Detector('weights/best.pt')
    annotated_image = annotator.predict_and_annotate(r'test\cream1.jpg')

    annotator.show("Frame", annotated_image)


if __name__ == "__main__":
    main()
