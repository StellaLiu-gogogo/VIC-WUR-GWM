#%%
import os 
import flopy
import numpy as np
import subprocess  # for calling shell commands
from datetime import datetime, timedelta
import calendar
#%%

cwd = '/Users/sidaliu/Documents/github_repo/VIC-WUR-GWM-1910/vic_online'
os.chdir(cwd)
filepath = os.path.join(cwd, 'python', 'VIC_config_file_template_pyread.txt')

#%% ask a startdate and calculate enddate, and generate a vic config file
#start simple, no loop. just do one timestep. 

startdate = '1968-01-01'
year,month,day = startdate.split('-')
year,month,_ = startdate.split('-')
_, lastday = calendar.monthrange(int(year), int(month))
enddate = f'{year}-{month}-{lastday}'

with open(filepath, 'r') as file:
    lines = file.readlines()

lines[13] = f"STARTYEAR               {year}\n"
lines[14] = f"STARTMONTH              {month}\n"
lines[15] = f"STARTDAY                {day}\n"
lines[16] = f"ENDYEAR                 {year}\n"
lines[17] = f"ENDMONTH                {month}\n"
lines[18] = f"ENDDAY                  {lastday}\n"   

with open(filepath, 'w') as file:
    file.writelines(lines)
#%% run vic
#%% report gwrecharge and discharge

#%% process gwrecharge and discharge to modflow

#%% run modflow

#%% report gwl and baseflow

#%% identify condition 1 2 3? and update soil moisture and add baseflow as extra discharge for next time step's riverrouting

#%% update vic state file

#%% loop to next timestep

