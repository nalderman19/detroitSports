# Nicholas Alderman - Assignment 4
# Examining the relationship between win% and attendance for different sports teams
# Research Question:
# How does the attendance of a Detroit Sports Team relate to the Win Percentage of that team over the last 40 years?
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------------------------
#    Cleaning Data Funcions - I use the csv files I generated from the following dataframes
# --------------------------------------------------------------------------------------------
# 1: getting attendance data
# returns dataframes containting the season year and the average attendance
def getAttendance():
    # manually get Red Wings Data - https://www.hockeydb.com/nhl-attendance/att_graph.php?tmi=5492
    redwings = pd.read_csv('redwingsattendance.csv')

    # scrape Tigers Data - https://www.baseball-almanac.com/teams/detatte.shtml
    r = req.get('https://www.baseball-almanac.com/teams/detatte.shtml').text
    soup = bs(r,'lxml')
    table = soup.find('table',{'class':'boxed'})
    elements = table.findAll('td',{'class':'datacolBox'})[2].text
    tigersTemp = elements.split('\n\n')
    tigersTemp = [i.lstrip().replace(',','') for i in tigersTemp]
    tigersTemp = [int(i) for i in tigersTemp if i.isalnum()]
    yearsTigers = np.arange(1901,2020,1)
    tigers = pd.DataFrame({'Season': yearsTigers,'Avg_Attendance': tigersTemp})
    tigers = tigers.drop(tigers[tigers.Season < 1970].index).reset_index(drop=True)
    return redwings, tigers


# 2: getting win% data
def getWinPercent():
    # get red wings data off wikipedia - https://en.wikipedia.org/wiki/List_of_Detroit_Red_Wings_seasons
    redwingsTemp = pd.read_html('https://en.wikipedia.org/wiki/List_of_Detroit_Red_Wings_seasons', attrs={"class": "wikitable"})[2]
    redwings = pd.DataFrame({'Season': redwingsTemp['NHL season', 'NHL season'],
                             'W': redwingsTemp['Regular season[3][6][7][8]','W'],
                             'GP': redwingsTemp['Regular season[3][6][7][8]','GP']})
    redwings['Season'] = redwings['Season'].str[0:4]
    redwings = redwings[:-3]
    redwings = redwings.replace('—',np.NaN)
    redwings = redwings.dropna()
    redwings = redwings.astype('int')
    redwings = redwings.drop(redwings[redwings.Season < 1970].index).reset_index(drop=True)
    redwings['Win_Percentage'] = redwings['W'] / redwings['GP']
    redwings = redwings.drop(columns=['W','GP'])
    # tigers data off wikipedia - https://en.wikipedia.org/wiki/List_of_Detroit_Tigers_seasons
    tigersTemp = pd.read_html('https://en.wikipedia.org/wiki/List_of_Detroit_Tigers_seasons', attrs={"class": "wikitable plainrowheaders"})[0]
    tigers = pd.DataFrame({'Season': tigersTemp['Season'],
                           'Win_Percentage': tigersTemp['Win%']})
    tigers = tigers.drop(tigers[tigers.Season < 1970].index).reset_index(drop=True)
    # fix 1981 strike
    tigers = tigers.groupby(['Season']).agg('mean').reset_index()
    return redwings, tigers
# get combined dataframes for each team
def getDf():
    redAtt, tigAtt = getAttendance()
    redWin, tigWin = getWinPercent()
    redwings = pd.merge(redWin,redAtt, on='Season')
    tigers = pd.merge(tigWin,tigAtt, on='Season')
    # save them as their own csv Files for manual editing (it was easier to add in stadium capacity by hand off the wikipedia pages for each team)
    # redwings.to_csv('redwings.csv', index=False)
    # tigers.to_csv('tigers.csv', index=False)
    return redwings, tigers

# ---------------------------------------------------------------------------------------------------------
#    Now Have full dataset that includes win%, average attendance, capacity, attendance% for each season
# ---------------------------------------------------------------------------------------------------------
# 2: Plotting data
redwings = pd.read_csv('redwingsData.csv')
tigers = pd.read_csv('tigersData.csv')


fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(redwings['Win_Percentage'], redwings['Avg_Attendance'], alpha=0.5, c='firebrick')
ax.set_xlim([0,1])
ax.set_ylim([0,23000])
ax.set_xlabel('Win Percentage')
ax.set_ylabel('Average Season Attendance')
ax.set_title('Red Wings')
ax.grid(which='major', axis='both', alpha=0.5)
for s in ax.spines.values():
    s.set_visible(False)
fig.savefig('images/redwings.png')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(tigers['Win_Percentage'], tigers['Avg_Attendance'], alpha=0.5, c='royalblue')
ax.set_xlim([0,1])
ax.set_ylim([0,40000])
ax.set_xlabel('Win Percentage')
ax.set_ylabel('Average Season Attendance')
ax.set_title('Tigers')
ax.grid(which='major', axis='both', alpha=0.5)
for s in ax.spines.values():
    s.set_visible(False)
fig.savefig('images/tigers.png')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(redwings['Season'], redwings['Win_Percentage'], color='firebrick', lw=3)
ax.plot(redwings['Season'], redwings['Avg_Percentage'],color='peru', lw=3)
ax.set_xlim([1970,2020])
ax.set_yticks(np.arange(0,1.1,0.1))
ax.yaxis.tick_right()
ax.yaxis.set_label_position("right")
ax.set_xlabel('Season')
ax.set_ylabel('Percentage')
ax.set_title('Attendance and Win Percentage for Red Wings')
ax.legend(['Win %','Attendance %'])
ax.grid(which='major', axis='y', alpha=0.5)
for s in ax.spines.values():
    s.set_visible(False)
fig.savefig('images/redwingsattwin%.png')

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(tigers['Season'], tigers['Win_Percentage'], color='royalblue', lw=3)
ax.plot(tigers['Season'], tigers['Avg_Percentage'],color='lightsteelblue', lw=3)
ax.set_xlim([1970,2020])
ax.set_yticks(np.arange(0,1.1,0.1))
ax.yaxis.tick_right()
ax.yaxis.set_label_position("right")
ax.set_xlabel('Season')
ax.set_ylabel('Percentage')
ax.set_title('Attendance and Win Percentage for Tigers')
ax.legend(['Win %','Attendance %'])
ax.grid(which='major', axis='y', alpha=0.5)
for s in ax.spines.values():
    s.set_visible(False)
fig.savefig('images/tigerssattwin%.png')




""" Attempt at plotting multiple charts in one gridspec, not enough room so doing one at a time
    still good code though
fig = plt.figure(constrained_layout=True)
# create gridspec
gs = fig.add_gridspec(ncols=3,
                      nrows=2,
                      width_ratios=[7,7,7],
                      height_ratios=[5,5])
# add plots
# f_ax1 is red wings scatter
# f_ax2 is red wings bar
# f_ax3 is tigers scatter
# f_ax4 is tigers bar
f_ax1 = fig.add_subplot(gs[:,0])
f_ax1.scatter(redwings['Win_Percentage'], redwings['Avg_Attendance'], alpha=0.5, c='firebrick')
f_ax1.scatter(tigers['Win_Percentage'], tigers['Avg_Attendance'], alpha=0.5, c='royalblue')
f_ax1.set_xlim([0,1])
f_ax1.set_ylim([0,40000])

f_ax2 = fig.add_subplot(gs[1,1:])
f_ax2.bar(redwings['Season']+0.25, redwings['Avg_Percentage'], color='firebrick', align='center')
f_ax2.bar(tigers['Season']-0.25, tigers['Avg_Percentage'], color='royalblue', align='center')
f_ax2.set_xlim([1970,2019])
f_ax2.set_ylim([0,1.15])
f_ax2.yaxis.tick_right()
"""