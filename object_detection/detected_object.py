class DetectedObject:
    def __init__(self, name, ymin,xmin,ymax,xmax, confidence):
        self.name = name
        self.ymin = ymin
        self.xmin = xmin
        self.ymax = ymax
        self.xmax = xmax
        self.confidence = confidence

    