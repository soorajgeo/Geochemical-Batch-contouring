import arcpy
from arcpy import env
from arcpy import sa

# Ask user input
user_data = arcpy.GetParameterAsText(0)
user_col = int(arcpy.GetParameterAsText(1))
output_loc = arcpy.GetParameterAsText(2)
env.extent = arcpy.GetParameterAsText(3)
radius = int(arcpy.GetParameterAsText(4))

#Set workspace environment
env.overwriteOutput = True
env.workspace = output_loc

# Select user data column
field_names = [f.name.encode('ascii') for f in arcpy.ListFields(user_data)]
sel_fields = field_names[user_col-1:]
sel_fields.remove("Shape")

# Set local variables
lagSize = 0.000921
majorRange = 0.03
partialSill = 0.03
nugget = 0
cellSize = 9.21111112000062E-04


# Set complex variables
kmodel = sa.KrigingModelOrdinary("EXPONENTIAL", lagSize, majorRange, partialSill, nugget)
kradius = sa.RadiusVariable(radius,"")

#Execute Krigging
for field in sel_fields:

    try:
        rast_file = field + "_raster.tif"
        out_raster = arcpy.sa.Kriging(user_data,field, kmodel, cellSize, kradius)
        out_raster.save(output_loc+"\\"+ rast_file)

    except:
        print arcpy.GetMessages(2)

print "Executed successfully"