"""
2023.04.03 v000

"""
import numpy as np
import pandas as pd
import time
from datetime import datetime
import os
import fnmatch
import xlsxwriter
from MyPlot import *


##### SETTINGS #####
filedir = r"C:\Users\II-ILS\Desktop\temporary\temperature\20230328埃対策\data"
dir_exp = filedir + "\\export"
extension = 'xls'
col_j = {'外気': 'open air', 'Unnamed: 3': 'datetime'}  # column names to be changed
show_rawplot = True  # Plot raw data
show_deltaTplot = True  # Plot fragmented data
show_deltaTtable = False  # Show fragmented data table


# File
files = os.listdir(filedir)
files = fnmatch.filter(files, '*.' + extension)

# Create a directory if the path does not exist
if not os.path.exists(dir_exp):
    os.mkdir(dir_exp)


# Apply calculation on multiple columns of dataframe
def get_deltaT(df):
    max_value = df.max(axis=1)
    min_value = df.min(axis=1)
    delta = max_value - min_value

    return delta


# # Plot saturated temperature
# def deltaTplot(data):
#
#     x = [1, 2, 3, 4, 5]
#     plt.figure()
#     plt.plot(x, fragmented_mean_offset[['LED1-1', 'LED1-2', 'LED1-3', 'LED1-4', 'LED1-5']].values, label='LED1', marker='o')
#     plt.plot(x, fragmented_mean_offset[['LED2-1', 'LED2-2', 'LED2-3', 'LED2-4', 'LED2-5']].values, label='LED2', marker='o')
#     plt.plot(x, fragmented_mean_offset[['LED3-1', 'LED3-2', 'LED3-3', 'LED3-4', 'LED3-5']].values, label='LED3', marker='o')
#     plt.plot(x, fragmented_mean_offset[['LED4-1', 'LED4-2', 'LED4-3', 'LED4-4', 'LED4-5']].values, label='LED4', marker='o')
#     plt.xlabel("Time (sec)")
#     plt.ylabel("Temperature (℃)")
#     plt.xlim(1, 5)
#     plt.ylim(20, 60)
#     plt.legend(loc='upper left', ncol=2, fontsize=8)
#     plt.savefig(dir_exp + datapath.split(".")[0] + "_delta.png")
#
#     return fragmented_mean_offset


# Convert selected df into datetime.datetime
def ConvertDatetime(df):
    print('EXECUTE - ConvertDatetime')

    if type(df[0]) == str:
        datetime.strptime(data.index[0], '%H:%M:%S').time()

    date_l = []
    date_tmp = datetime.min  # In order to convert datetime.time to datetime.datetime

    print('type(df[0]) =', type(df[0]))
    for i in range(len(df)):
        if type(df[0]) == datetime.time:
            date_l.append(datetime.combine(date_tmp, df[i]))
        elif type(df[0]) == str:
            date_l.append(datetime.combine(date_tmp, datetime.strptime(data.index[i], '%H:%M:%S').time()))
        else:
            raise Exception('type(df[0]) is equal to neither of "datetime.time" and "str"')


    print('DONE - ConvertDatetime')
    return date_l


# Get timedelta (min)
def gettimedelta(df):
    print('EXECUTE - gettimedelta')

    timedelta_l = []
    for i in range(len(df)):
        timedelta_l.append((df[i] - df[0]).total_seconds() / 60)  # min

    print('DONE - gettimedelta')
    return timedelta_l


# Create a new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook(dir_exp + '\\graph.xlsx')
worksheet = workbook.add_worksheet()

# Start iteration
write_col = 2
for i in range(len(files)):
    write_row = 2
    datapath = filedir + "\\" + files[i]
    outpath = filedir + "\\export\\" + files[i]
    print('FILE IMPORTED:', filedir + "\\" + files[i])

    ##### Processing data #####
    data = pd.read_excel(datapath, skiprows=24, index_col=2)
    data = data.drop(data.columns[[0, 1, 2]], axis=1)  # drop unwanted columns
    data = data.drop(data.index[[0]], axis=0)  # drop unwanted rows
    data = data.rename(col_j, axis=1)  # rename column names

    data.index = ConvertDatetime(data.index)
    # d = gettimedelta(data.index)
    data.index = gettimedelta(data.index)


    ##### Plot raw data #####
    if show_rawplot:

        # Plot
        mypyplot(data, xlab='Time (min)', ylab='Temperature (℃)', ylim=(20, 40), color=1, save=(1, outpath.split(".")[0] + "_raw.png"))
        print('FILE SAVED:', outpath.split('.')[0] + '_raw.png')

        # Sleep
        time.sleep(1)

        # Export to excel
        worksheet.write(write_row, write_col, files[i])
        worksheet.insert_image(write_row + 1, write_col, outpath.split(".")[0] + "_raw.png",
                               {'x_scale': 0.6, 'y_scale': 0.6})
        write_row += 16


    ##### Plot deltaT #####
    if show_deltaTplot:

        data['LED1'] = get_deltaT(data[['LED1-1', 'LED1-2', 'LED1-3', 'LED1-4', 'LED1-5']])
        data['LED2'] = get_deltaT(data[['LED2-1', 'LED2-2', 'LED2-3', 'LED2-4', 'LED2-5']])
        data['LED3'] = get_deltaT(data[['LED3-1', 'LED3-2', 'LED3-3', 'LED3-4', 'LED3-5']])
        data['LED4'] = get_deltaT(data[['LED4-1', 'LED4-2', 'LED4-3', 'LED4-4', 'LED4-5']])

        # Plot
        mypdplot(data[['LED1', 'LED2', 'LED3', 'LED4']], xlab='Time (min)', ylab='Delta T (℃)', ylim=(0, 10), save=(1, outpath.split(".")[0] + "_delta.png"))
        print('FILE SAVED:', outpath.split('.')[0] + '_delta.png')

        # Sleep
        time.sleep(1)

        # Export to excel
        worksheet.write(write_row, write_col, files[i].split('.')[0]+'_delta.png')
        worksheet.insert_image(write_row + 1, write_col, outpath.split(".")[0] + "_delta.png",
                               {'x_scale': 0.6, 'y_scale': 0.6})


        ##### Show fragmented data table #####
        if show_deltaTtable:

            fragmented = data.iloc[-50:, :]  # Get each mean value
            fragmented_mean = fragmented.mean(
                numeric_only=None)  # FutureWarning: The default value of numeric_only in DataFrame.mean is deprecated.
            ofst = 32 - fragmented_mean['atmosphere']  # Offset by atmosphere
            fragmented_mean_offset = fragmented_mean.add(ofst)

            led1 = fragmented_mean_offset[0:5]
            led2 = fragmented_mean_offset[5:10]
            led3 = fragmented_mean_offset[10:15]
            led4 = fragmented_mean_offset[15:20]

            fragmenteddata_l = [data.columns[1:].to_list(),  # columns
                                fragmented_mean_offset.values.tolist()]  # values

            led_l = [
                list(led1.index),
                list(led1.values),
                list(led2.index),
                list(led2.values),
                list(led3.index),
                list(led3.values),
                list(led4.index),
                list(led4.values),
            ]

            write_row += 16

            # add_table options
            options = {
                'data': led_l,
                'header_row': 0,
            }

            # Add a table to the worksheet.
            worksheet.add_table(write_row, write_col, write_row+7, write_col+4, options)

    write_col += 6

# Close excel
workbook.close()

# Save data table
data.to_csv(outpath.split('.')[0] + '_table.csv')
print('FILE SAVED:', outpath.split('.')[0] + '_table.csv')





