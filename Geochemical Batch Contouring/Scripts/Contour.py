import arcpy
import os
import numpy as np
from arcpy import env
from arcpy.sa import *

# Ask user input
sel_raster = arcpy.GetParameterAsText(0)
sel_data = arcpy.GetParameterAsText(1)
start = int(arcpy.GetParameterAsText(2))
tun_para = int(arcpy.GetParameterAsText(3))

#Set workspace environment
env.overwriteOutput = True
env.workspace = sel_raster

#Set contour interval
field_names = [f.name.encode('ascii') for f in arcpy.ListFields(sel_data)]
sel_fields = field_names[start-1:]
sel_fields.remove("Shape")

## Append contour intervals in values list
i = 0
values = []

while i < len(sel_fields):
    array = arcpy.da.FeatureClassToNumPyArray(sel_data, sel_fields[i])
    a = np.asarray(array).astype(np.float32)
    std = np.std(a)
    new_std = std/tun_para
    i+=1
    values.append(new_std)

# Set dictionary with key as element name and value as element concentration
keys = sel_fields
dicts = {keys[i]:values[i] for i in range(len(keys))}

# Calculate Contour Intervals
raster_names = [field.encode('ascii') for field in arcpy.ListRasters("*", "All")]
contourInterval = [dicts[k.replace("_raster.tif","")] for k in raster_names]

# Set contour parameter
baseContour = 0

# Execute Contour
for raster in arcpy.ListRasters("*", "All"):

    try:
        j = 0
        st = raster.replace("_raster.tif","")
        contor_file = st + "_cnt.shp"
        out_name = os.path.join(sel_raster,contor_file)
        Contour(raster, contor_file, contourInterval[j], baseContour)
        j+=1

    except:
        print arcpy.GetMessages(2)

print "Executed successfully"