import os
import pickle


class DetectedObjectUnpacker:
    def unpack(self, fname):
        if not os.path.exists(fname):
            print("file '" + fname + "' doesn't exists")
            return

        with open(fname, "rb") as f:
            _obj = pickle.load(f)
            return(_obj, self._get_entities_names(_obj), self._get_entities_metadata(_obj))

    # method to pack all the detected object names
    def _get_entities_names(self, detected_objects):
        buff = ""
        for item in detected_objects:
            buff += "(" + item.name + "),"
        return buff
    
    # method to pack all the detected object metadata as tuples
    def _get_entities_metadata(self, detected_objects):
        buff = ""
        for item in detected_objects:
            buff += "(" + item.name + "," + str(item.xmin) + "," + str(item.ymin) + "," + str(item.xmax) + "," + str(item.ymax) + "," + str(item.confidence) + "),"
        return buff


if __name__ == "__main__":
    fname = "COCO_train2014_000000000049.pkl"
    d = DetectedObjectUnpacker()
    o, n, m = d.unpack(fname)
    print("hello")
