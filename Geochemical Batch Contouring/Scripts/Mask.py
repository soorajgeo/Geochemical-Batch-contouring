import arcpy
import os

from arcpy import env

# Input user data
in_contour = arcpy.GetParameterAsText(0)
mask = arcpy.GetParameterAsText(1)

#Set workspace environment
env.overwriteOutput = True
env.workspace = in_contour

#Execute masking
for file in arcpy.ListFeatureClasses("*", "Polyline"):

    try:
        en_file = file.encode('ascii')
        mask_file = en_file.replace("_cnt.shp", "") + "_mask.shp"
        out_name = os.path.join(in_contour, mask_file)
        arcpy.Erase_analysis(file, mask, out_name)

    except:
        print arcpy.GetMessages(2)

print "Executed successfully"

