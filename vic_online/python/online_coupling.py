#%%
import os 
import flopy
import numpy as np
import subprocess  # for calling shell commands
from datetime import datetime, timedelta
import calendar
#%%

cwd = '/home/sliu/Documents/gitversion/VIC-WUR-GWM-1910/vic_online'
os.chdir(cwd)
filepath = os.path.join(cwd, 'python', 'VIC_config_file_template_pyread.txt')
statefile_dir = os.path.join(cwd, 'python', 'statefile')  #may change later 
configfile_dir = os.path.join(cwd, 'python', 'configfile')  #may change later

#%% ask a startdate and calculate enddate, and generate a vic config file
startdate = '1968-04-01' 
year, month, day = startdate.split('-')
year, month, day = int(year), int(month), int(day)
_, lastday = calendar.monthrange(year, month) # to get the last day of the month
startdate = datetime(year, month, day) # to get the startdate as a datetime object
enddate = datetime(year, month, lastday) # to get the enddate as a datetime object

statedate = startdate - timedelta(days=1) # to get the statefile date as a datetime object
statedate_str = statedate.strftime('%Y%m%d')

# Add one day to the end date to get the new start date


#%%
prefixes = {
    "STARTYEAR": year,
    "STARTMONTH": month,
    "STARTDAY": day,
    "ENDYEAR": year,
    "ENDMONTH": month,
    "ENDDAY": lastday,
    "INIT_STATE": os.path.join(statefile_dir, f"state_file_.{statedate_str}_00000.nc"),
    "STATENAME":  os.path.join(statefile_dir, "state_file_"),
    "STATEYEAR": year,
    "STATEMONTH": month,
    "STATEDAY": lastday,
    # Add other prefixes and their corresponding values here
}

with open(filepath, 'r') as file:
    lines = file.readlines()

for i, line in enumerate(lines):
    for prefix, value in prefixes.items():
        if line.startswith(prefix):
            lines[i] = f"{prefix}               {value}\n"
            break

# Write the modified lines back to the file
parameter_file = os.path.join(configfile_dir, f"config_{year}_{month}.txt")
with open(parameter_file, 'w') as file:
    file.writelines(lines)
#%% run vic
#call subprocess to run vic

vic_executable = '/home/sliu/Documents/vic_indus/99SourceCode/VIC-WUR-GWM-1910/vic_offline/drivers/image/vic_image_gwm_offline.exe'
command = [vic_executable, '-g', parameter_file]

try:
    subprocess.run(command, check=True, shell=False)
    print("VIC-WUR run successfully for time step [{}-{}]".format(year, month))
except subprocess.CalledProcessError:
    print("VIC模型运行失败")




#%% process gwrecharge and discharge to modflow
# Haochen is taking care of this part
#%% run modflow
modflowmodel = 'mf.py'
command = ['python', modflowmodel]
try:
    subprocess.run(command, check=True, shell=False)
    print("MODFLOW模型运行成功")
except subprocess.CalledProcessError:
    print("MODFLOW模型运行失败")
#%% report gwl and baseflow

#%% identify condition 1 2 3? and update soil moisture and add baseflow as extra discharge for next time step's riverrouting

#%% update vic state file

#%% loop to next timestep
new_startdate = enddate + timedelta(days=1)
