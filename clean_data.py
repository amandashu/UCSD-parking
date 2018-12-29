# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 15:43:03 2018

@author: Amanda
"""
# -*- coding: utf-8 -*-
# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from os.path import dirname, join, basename

def create_data():
    parking = pd.read_excel(join(dirname(__file__),'data', 'parking.xlsx'), sheet_name='Sheet1')
    
    # move time to row 2 and make row 2 the column names
    parking.iloc[2][7:] = parking.iloc[1][7:]
    
    # get the data without empty rows/columns
    parking.drop(columns='Unnamed: 5',inplace=True)
    parking_data = parking.iloc[4:,1:]
    
    # get structure/lot column names
    lots = list(parking.iloc[2][1:5])
    
    # get structure/lots data
    common_data = parking_data.iloc[:,0:4].reset_index().iloc[:,1:5]
    common_data.columns = lots
    
    xy = {'Hopkins':(600, 1040), 
                   'Oster':(715, 435),
                   'Pangea':(425,1060),
                   'Torrey Pines Center North':(450,1530),
                   'Torrey Pines Center South':(425,1425),
                   'P014':(37,162),
                   'P016':(37,30),
                   'P021':(240,130),
                   'P102':(440,315),
                   'P386':(330,1315),
                   'P401':(1060,760),
                   'P504':(935,910),
                   'P704':(1485,825),
                   'P705':(1540,860),
                   'P782':(1570,560)
                    }
    
    x_values = np.array([])
    y_values = np.array([])
    for x,y in xy.values():
        x_values = np.append(x_values, x)
        y_values = np.append(y_values, y)
    
    common_data['x'] = pd.Series(x_values)
    common_data['y'] = pd.Series(y_values)
    
    # create a array called structure_lot to replace Structure and Lot
    structure_lot = np.array([])
    for i in np.arange(len(common_data)):
        if isinstance(common_data.iloc[i,0], float) == False and isinstance(common_data.iloc[i,1], float) == True:
            structure_lot = np.append(structure_lot,common_data.iloc[i,0])
        elif isinstance(common_data.iloc[i,0], float) == True and isinstance(common_data.iloc[i,1], float) == False:
            structure_lot = np.append(structure_lot,common_data.iloc[i,1])
        else: 
             structure_lot = np.append(structure_lot,common_data.iloc[i,0] + ' (' + common_data.iloc[i,1] + ')')
    
    # drop Structure, Lot, and Type columns
    common_data = common_data.iloc[:,3:]
    
    # add new columnes Structure/Lot to dataframe
    common_data['Structure/Lot'] = structure_lot
    
    # reorder columns to Structure/Lot, Longitude Latitude, Total Spaces
    columns_to_reorder = common_data.columns
    reordered = np.array([columns_to_reorder[-1],columns_to_reorder[1], columns_to_reorder[2],columns_to_reorder[0]])
    common_data = common_data[reordered]
    
    # create array of times
    times = np.array(['8AM','10AM','12PM','2PM'])
    
    # create empty dataframe
    mon_parking = pd.DataFrame([])
    tues_parking = pd.DataFrame([])
    wed_parking = pd.DataFrame([])
    thurs_parking = pd.DataFrame([])
    days = [mon_parking, tues_parking, wed_parking, thurs_parking]
    
    # split parking_data into data by each day
    for i in range(4):
        start_index = 4+i*4
        end_index = 8+i*4
        days[i] = pd.DataFrame(parking_data.iloc[:,start_index:end_index].reset_index().iloc[:,1:])
        days[i].columns = times
    
    # create dataframes for each day    
    mon_parking = common_data.merge(days[0], left_index=True, right_index=True)
    tues_parking = common_data.merge(days[1], left_index=True, right_index=True)
    wed_parking = common_data.merge(days[2], left_index=True, right_index=True)
    thurs_parking = common_data.merge(days[3], left_index=True, right_index=True)
    
    # create list of each of the dataframes
    day_dataframes = [mon_parking, tues_parking, wed_parking, thurs_parking]
    
    # create columns for percentages of available spaces
    for df in day_dataframes:
        for i in np.arange(4,8):
            new_col_name = df.columns[i] + ' % Open Spaces'
            df[new_col_name] = df.iloc[:,i]/df.iloc[:,3]
            
    # add columns for colors by percentage of open spaces
    for df in day_dataframes:
        for i in np.arange(8,12):
            new_col_name = df.columns[i-4] + ' colors'
            colors=np.array([])
            for r in np.arange(16):
                if df.iloc[r,i] <= 0.05:
                    colors = np.append(colors,'darkred')
                elif df.iloc[r,i] <= 0.25:
                    colors = np.append(colors,'firebrick')
                elif df.iloc[r,i] <= 0.5:
                    colors = np.append(colors,'orange')
                elif df.iloc[r,i] <= 0.75:
                    colors = np.append(colors,'khaki')
                else:
                    colors = np.append(colors,'seagreen')
            df[new_col_name] = colors  
    
    # add a column of scaled total spaces for graphing
    for df in day_dataframes:
        df['Scaled Total Spaces'] = df['Total Spaces']/14
        
    return mon_parking, tues_parking, wed_parking, thurs_parking, day_dataframes