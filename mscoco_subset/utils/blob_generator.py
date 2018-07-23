import os
import base64
import glob
import datetime
import json
import uuid
import exifread
import urllib.request
import certifi
import json
import ast

# Helper class for geo-encoding and reverse geo-encoding 
class GeoEnodingHelper:
    def __init__(self):
        self.GEO_API_KEY = "AIzaSyBDvkEwnaH_ePorXvJOlnCTk1smpmIwBmk"
        self.endpoint = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyBDvkEwnaH_ePorXvJOlnCTk1smpmIwBmk&latlng="

    def dms_to_dd(self, d, m):
        dd = d + float(m)/60
        return dd

    def get_address(self, lat, lon):
        lat = str(lat).split(",")[:2]
        lat = ",".join(lat)[1:]

        lon = str(lon).split(",")[:2]
        lon = ",".join(lon)[1:]
        
        lat = [int(x) for x in str(lat).split(",")]
        lon = [int(x) for x in str(lon).split(",")]

        lat_d = self.dms_to_dd(lat[0], lat[1])
        lon_d = self.dms_to_dd(lon[0], lon[1])

        _url = self.endpoint + str(lat_d)+ ",-" + str(lon_d)
        contents = urllib.request.urlopen(_url, cafile=certifi.where()).read().decode("utf-8")

        _json = json.loads(contents)
        # print(_json["results"][0]["formatted_address"])

        if "results" in _json:
            if len(_json["results"]) > 0 :
                return _json["results"][0]["formatted_address"]


# Class to generate blob for blob storage to feed in search index
class BlobGenerator:
    def __init__(self):
        self.g = GeoEnodingHelper()
        self.date = datetime.datetime.now().strftime("%Y%m%d")

    def _get_image_base64(self, img_path):
        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return encoded_string.decode("utf-8") 

    def _create_blob(self, base64img, caption, annotationlist, op_filename, location, datetime, device):
        # this is schema for blob storage for azure search index
        _json = {"id" : str(uuid.uuid4()),
                 "datetime" : datetime,
                 "annotationlist" : annotationlist,
                 "location" : location,
                 "device" : device,
                 "caption" : caption,
                 "image" : base64img
                }
        
        with open(op_filename, "w") as fp:
            json.dump(_json, fp)
        
    def _get_image_tags(self, filename, op_tags):
        result_tags = {}
        with open(filename, 'rb') as fh:
            tags = exifread.process_file(fh)
            for key in op_tags:
                if key in tags:
                    result_tags[key] = str(tags[key])
            return result_tags

    def _get_consumable_img_tags(self, tag_dict):
        result_dict = {"location":"", "datetime":"", "device":""}
        # get address using lat-lon
        lat = tag_dict["GPS GPSLatitude"]
        lon = tag_dict["GPS GPSLongitude"]

        result_dict["location"] = self.g.get_address(lat, lon)

        # get device info
        result_dict["device"] = str(tag_dict["Image Model"])
        # convert into month-name, year
        result_dict["datetime"] = str(tag_dict["EXIF DateTimeOriginal"])

        return result_dict

    def process(self, path, output_dir):
        if not os.path.exists(path):
            print("path :'"+ path + "' doesn't exists.")
            return
        
        fip = open(path, "r", encoding="utf-8")
        cnt = 1
        for line in fip:
            items = line.split("\t")
            fname = items[0]
            caption = items[1]

            img_tag_keys = [ "EXIF DateTimeOriginal",
                             "GPS GPSLatitude",
                             "GPS GPSLongitude",
                             "Image Model"
                            ]

            img_tags = self._get_consumable_img_tags(self._get_image_tags(fname, img_tag_keys))
            base64_img = self._get_image_base64(fname)

            op_filename = output_dir + "/op" + str(cnt) + ".json"
            self._create_blob(base64_img, caption, "", op_filename, img_tags["location"], img_tags["datetime"], img_tags["device"])
            cnt+= 1
        print("Completely processed " + path)

if __name__ == "__main__":
    path = "/Users/kartik/pycook/tensorflow_models/models/research/im2txt/mscoco_subset/mscoco_subset_gen_captions.tsv"
    
    b = BlobGenerator()
    b.process(path, "blob_files")


    # using Reverse geo encoding using geo-encoder
    # g = GeoEnodingHelper()
    # g.get_address([47, 38, 777/20], [122, 7, 2711/100])