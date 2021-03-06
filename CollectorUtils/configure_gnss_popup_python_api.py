"""
   Copyright 2017 Esri
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.​    
"""
import arcpy
import argparse
import sys
import json
import arcgis
from arcgis.gis import GIS


# Parse Command-line arguments
def parseArguments():
    parser = argparse.ArgumentParser(
        usage='Configure GNSS metadate fields visibility and popup')

    arcpy.AddMessage("Parsing Arguments..")

    parser.add_argument('url', help='Organization url')
    parser.add_argument('username', help='Organization username')
    parser.add_argument('password', help='Organization password')
    parser.add_argument('webmap_Name', type=str, help='Webmap Name')
    parser.add_argument('layerIndex', type=int, help='Feature Layer index. If not specified use 0 as index')

    args_parser = parser.parse_args()
    arcpy.AddMessage("Done parsing arguments..")
    return args_parser


# Search for a Webmap and update GNSS Metadata fields popup info
def searchItems_UpdateGNSSMetadataFieldsPopup(args_parser):
    # Search ItemIds
    gis = GIS(args_parser.url, args_parser.username, args_parser.password)
    arcpy.AddMessage("Signed into organization..")
    
    itemId = args_parser.webmap_Name
   
    try:
        arcpy.AddMessage("Started configuring popup and visibility..")
        
        # Iterate through each ItemId and update the popup info for the specified feature layer
        webmapItem = gis.content.search(itemId, item_type="Web Map")  # create a Webmap object from the search result
        webmap = arcgis.mapping.WebMap(webmapItem[0])
        
        # Configure popup and set visibility on the GNSSMetadata fields.
        fieldInfos = webmap['operationalLayers'][args_parser.layerIndex]['popupInfo']['fieldInfos'] if args_parser.layerIndex else \
                     webmap['operationalLayers'][0]['popupInfo']['fieldInfos']

        for field_info in fieldInfos:
            # Configure popup and visibility for GNSSMetadata fields
            if field_info['fieldName'].upper() == 'ESRIGNSS_H_RMS':
                field_info['format']['places'] = 2
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_V_RMS':
                field_info['format']['places'] = 2
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_LATITUDE':
                field_info['format']['places'] = 8
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_LONGITUDE':
                field_info['format']['places'] = 8
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_ALTITUDE':
                field_info['format']['places'] = 2
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_PDOP':
                field_info['format']['places'] = 2
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_HDOP':
                field_info['format']['places'] = 2
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_VDOP':
                field_info['format']['places'] = 2
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_CORRECTIONAGE':
                field_info['format']['places'] = 0
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_FIXDATETIME':
                field_info['format']['dateFormat'] = 'shortDateShortTime'
                field_info['format']['timezone'] = 'utc'
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_AVG_H_RMS':
                field_info['format']['places'] = 2
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_AVG_V_RMS':
                field_info['format']['places'] = 2
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_H_STDDEV':
                field_info['format']['places'] = 3
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_RECEIVER' or field_info[
                'fieldName'].upper() == 'ESRIGNSS_STATIONID' or \
                            field_info['fieldName'].upper() == 'ESRIGNSS_FIXTYPE' or field_info[
                'fieldName'].upper() == 'ESRIGNSS_NUMSATS' or \
                            field_info['fieldName'].upper() == 'ESRIGNSS_AVG_POSITIONS':
                field_info['visible'] = True
                field_info['isEditable'] = False

        # Set Webmap fieldInfos property
        if args_parser.layerIndex:
            webmap['operationalLayers'][args_parser.layerIndex]['popupInfo']['fieldInfos'] = fieldInfos
        else:
            webmap['operationalLayers'][0]['popupInfo']['fieldInfos'] = fieldInfos

        # Update Webmap
        webmap.update()
        arcpy.AddMessage("Siccessfully configured popup and visibility..")
    
    
    except Exception as e:
        arcpy.AddMessage(e)
        print(e)


if __name__ == '__main__':
    args_parser = parseArguments()
    searchItems_UpdateGNSSMetadataFieldsPopup(args_parser)
