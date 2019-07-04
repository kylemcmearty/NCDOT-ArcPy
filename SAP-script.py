# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# SAP-script.py
# Created on: 2019-03-04 11:54:35.00000
# Usage: SAP-script <NCRoutes_shp> <SAP_script_csv> 
# Description: Parses RouteID string data from NCRoutes.shp into SAP database format
# ---------------------------------------------------------------------------

# Import arcpy module and set environment to import and export files
import arcpy
arcpy.env.workspace = "C:/Users/kamcmearty/Desktop/SAP-script"
arcpy.env.overwriteOutput = True 

# Input NCRoute shapefile parameter
NCRoutes_shp = arcpy.GetParameterAsText(0)
if NCRoutes_shp == '#' or not NCRoutes_shp:
    NCRoutes_shp = "NCRoutes.shp" # provide a default value if unspecified

# Export SAP format to csv parameter
SAP_script_csv = arcpy.GetParameterAsText(1)
if SAP_script_csv == '#' or not SAP_script_csv:
    SAP_script_csv = "SAP-script.csv" # provide a default value if unspecified

# Local variables:
NCSQL = "NCSQL.shp"
NCRin = NCSQL
SQLcounty = NCRin
SQLPREPRE = SQLcounty
NCSQLL = SQLPREPRE
NCPFXX = NCSQLL
NCPFX2 = NCPFXX
NCPREFX = NCPFX2
NCRTNM = NCPREFX
NCSFX = NCRTNM
NCSuffix = NCSFX
NCSX3 = NCSuffix
NCSX4 = NCSX3
NCSAP = NCSX4
sapStr = NCSAP
SAP_script = "C:/Users/kamcmearty/Desktop/SAP-script"

# Select Route Class and Inventory number
arcpy.Select_analysis(
NCRoutes_shp, NCSQL,
"\"RouteClass\" IN ('1', '2', '3', '4') AND \"RouteInven\" IN ( '0' , '8' )")

# Add Field to hold county numbers
arcpy.AddField_management(
NCSQL, "counties",
"TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Parse county numbers from RouteID and store in "counties" field
arcpy.CalculateField_management(
NCRin, "counties",
"right(\"000\" + [RouteID],3)", "VB", "")

# Add Field to hold Class data to convert to prefix
arcpy.AddField_management(
SQLcounty, "FAKEprefix", 
"TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Get Class number and store in fied
arcpy.CalculateField_management(
SQLPREPRE, "FAKEprefix", 
"Left([RouteID],1)", "VB", "")

# Add new prefix field to convert data from FAKEprefix
arcpy.AddField_management(
NCSQLL, "prefix", 
"TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Convert Class number into prefix
arcpy.CalculateField_management(
NCPFXX, "prefix", "val", "VB",
"if [FAKEprefix] = \"1\" Then\
\nval = \"I-\"\
\nelseif [FAKEprefix] = \"2\" Then\
\nval =\"US\"\
\nelseif [FAKEprefix] = \"3\" Then\
\nval = \"NC\"\
\nelseif [FAKEprefix] = \"4\" Then\
\nval = \"SR\"\
\nend if")

# Add field to hold Route Number
arcpy.AddField_management(
NCPFX2, "RouteNum", 
"TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Select Route Number from RouteID field
arcpy.CalculateField_management(
NCPREFX, "RouteNum", 
"Mid([RouteID],4, 5)", "VB", "")

# Add Field to hold  data to convert to prefix
arcpy.AddField_management(
NCRTNM, "presuffix", 
"TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field (4)
arcpy.CalculateField_management(
NCSFX, "presuffix", 
"Mid([RouteID],2,1)", "VB", "")

# Process: Add Field (7)
arcpy.AddField_management(
NCSuffix, "suffix", 
"TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Process: Calculate Field (7)
arcpy.CalculateField_management(NCSX3, "suffix", "val", "VB", 
"if [presuffix] = \"0\" Then\\nval = \"\"\
\nelseif [presuffix] = \"1\" Then\\nval = \"ALT\"\
\nelseif [presuffix] = \"2\"Then\\nval = \"BYP\"\
\nelseif [presuffix] = \"5\" Then\\nval = \"EAST\"\
\nelseif [presuffix] = \"6\" Then\\nval = \"WEST\"\
\nelseif [presuffix] = \"7\" Then\\nval = \"CNCTR\"\
\nelseif [presuffix] = \"8\" Then\\nval = \"TRCK\"\
\nelseif [presuffix] = \"9\" Then\\nval = \"BUS\"\
\nend if")

# Create field to hold SAP string
arcpy.AddField_management(
NCSX4, "sapString", 
"TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

# Concatenate fields into required SAP string format
arcpy.CalculateField_management(
NCSAP, "sapString", 
"[counties] & \" \" & [prefix] & \"\" & [RouteNum] & \" \" & [suffix]", "VB", "")

# Export "sapString" to .csv
arcpy.TableToTable_conversion(sapStr, SAP_script, "SAP-script.csv", "",
"sapString \"sapString\" true true false 255 Text 0 0 ,First,#,
C:\\Users\\kamcmearty\\Documents\\ArcGIS\\Default.gdb\\NCSQL,sapString,-1,-1", "")

