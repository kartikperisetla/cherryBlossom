class DetectedObjects:
    def __init__(self, name, ymin,xmin,ymax,xmax, confidence):
        self.name = name
        self.boundary = [ ymin, xmin, ymax, xmax]
        self.confidence = confidence

    