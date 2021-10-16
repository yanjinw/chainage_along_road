'''
File: putting_chainage_point_on_multiline.py
Project: Chainage breakdown
Created Date: 16-10-2021
Author: Yanjin Wang
-----
Last Modified: 16-10-2021
Modified By: Yanjin Wang
-----
Copyright (c) 2021 - Yanjin Wang- AXO Consulting
-----
Program details:
This program produces sets of points at 10 m interval along the feature

Requisite: 
1. There should be Asset_ID field with integer value on the table that has road datasets;
2. There should be Road_Name field with string value on the table that has road datasets;
3. There should be from field on the table that has road datasets;
4. The dataset should be in EPSG:28354 projectionAcronym
5. Sometime the direction of verticies could be opposite; it is important that the multiline is 
swapped before using this tool.argparse
6. Sometime, the line are not fully connected; it is important that line segments are fully connected

Editability:
1. With minimal knowledge of Pyqgis, the above requirements can be modified. For example:
    - If the data is on another projection, and location is in different zone, this can be changed. However,
      all projections should be in cartesian co-oridnates
    - If the road datasets are structured differently; the program can be edited
    - Instead of 10 m chainage, if we would like to procude 5 m chainage or 20 m chainage, all '10' in the program 
      need to be edited to that figure.

Output file:
- The program will produce output file called 'output'. There will be following attributes on the output file
   a) Asset_ID ( it will be taken from original multiline layer)
   b) Road_Name ( it will be taken from original multiline layer)
   c) Chainage in m
   d) Primary_Location ( at present it will keep the Road Name as primary location)
   e) Location ( at present it will keep the 'from' information from the original layer)

----------	---	---------------------------------------------------------
'''
from qgis.core import *
from qgis.gui import *
import processing

#input the location of the vector file in the following path or edit

infn2="C:\Yanjin\Mod04AssessedEx\Mod04AssessedEx\\road_renamed.shp"
vlayer1= iface.addVectorLayer(infn2,'','ogr')

#Extracting Asset_ID, Road_Name, from information from the input layer

# create fields for the output table
layerFields = QgsFields()
layerFields.append(QgsField('Road_Name', QVariant.String))
layerFields.append(QgsField('Chainage', QVariant.Double))
layerFields.append(QgsField('Primary_Location', QVariant.String))
layerFields.append(QgsField('Asset_ID', QVariant.Int))
layerFields.append(QgsField('Location', QVariant.String))

# create file name for output

fn = 'C:\Yanjin\Module3PracExv2\Module3PracEx\output7.shp'
writer = QgsVectorFileWriter(fn, 'UTF-8', layerFields,\
QgsWkbTypes.Point,\
QgsCoordinateReferenceSystem('EPSG:28354'),\
'ESRI Shapefile')
feat =[]
feat = QgsFeature()

iter = vlayer1.getFeatures()
e=0
for feature in iter:
    AssetID=feature['Asset_ID']
    PrimaryLocation=feature['Road_Name']
    RoadName=feature['Road_Name']
    Location=feature['from']
    geom=feature.geometry()
    length=geom.length()
    n=int(length/10)
    d=length-n*10                               # checking if the total length is exact multiple of 10
    
    if d==0:
        n=n                                 # the iteraction cycle is 1 less if exact multiple of 10
    else:
        n=n+1
      
    for j in range (n):
        c=length-j*10
        if c>=10:
            point=geom.interpolate(10*j)
#        Writing data of chainage onto the output file
            feat.setGeometry(point)    
            feat.setAttributes([RoadName,e+10*j,PrimaryLocation,AssetID,Location])
            writer.addFeature(feat)
        else:                                               # for last portion which is less than 10 m
            point=geom.interpolate(length)
            feat.setGeometry(point)    
            feat.setAttributes([RoadName,e+length,PrimaryLocation,AssetID,Location])
            writer.addFeature(feat)
            e=e+length
        
# output file displaying on canvas
layer = iface.addVectorLayer(fn, '', 'ogr')


del(writer)                     # removing the writer


