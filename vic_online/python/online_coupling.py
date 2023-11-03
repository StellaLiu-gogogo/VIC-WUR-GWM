#%%
import os 
import flopy
import numpy as np
import subprocess  # for calling shell commands
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
#%%

cwd = '/home/sliu/Documents/gitversion/VIC-WUR-GWM-1910/vic_online'
os.chdir(cwd)
filepath = os.path.join(cwd, 'python', 'VIC_config_file_template_pyread.txt')
statefile_dir = os.path.join(cwd, 'python', 'statefile')  #may change later 
configfile_dir = os.path.join(cwd, 'python', 'configfile')  #may change later

vic_executable = '/home/sliu/Documents/vic_indus/99SourceCode/VIC-WUR-GWM-1910/vic_offline/drivers/image/vic_image_gwm_offline.exe'

#%%
startstamp = datetime(1968, 1, 1)
current_date = startstamp
finishdate = datetime(1969, 1, 31)

# Loop over the dates
while current_date <= finishdate:
    startyear, startmonth, startday = current_date.year, current_date.month, current_date.day
    _, lastday = calendar.monthrange(startyear, startmonth)  # to get the last day of the month
    # startdate = datetime(year, month, day) # to get the startdate as a datetime object
  
    statedate = datetime(startyear, startmonth, lastday) # to get the state as a datetime object
    stateyear,statemonth,stateday = statedate.year, statedate.month, statedate.day #to specify config file
    
    init_date = current_date - relativedelta(days = 1)
    init_datestr = init_date.strftime('%Y%m%d')  #for generating statefile name  

    enddate = datetime(startyear,startmonth,startday) + relativedelta(months=1) # Add one month to the end date to get the new start date
    endyear, endmonth, endday = enddate.year, enddate.month, enddate.day
    prefixes_firststep = {
    "STARTYEAR": startyear,
    "STARTMONTH": startmonth,
    "STARTDAY": startday,
    "ENDYEAR": endyear,
    "ENDMONTH": endmonth,
    "ENDDAY": endday,
    "STATENAME":  os.path.join(statefile_dir, "state_file_"),
    "STATEYEAR": stateyear,
    "STATEMONTH": statemonth,
    "STATEDAY": stateday,
    # Add other prefixes and their corresponding values here
    }
    prefixes = {
    "STARTYEAR": startyear,
    "STARTMONTH": startmonth,
    "STARTDAY": startday,
    "ENDYEAR": endyear,
    "ENDMONTH": endmonth,
    "ENDDAY": endday,
    "INIT_STATE": os.path.join(statefile_dir, f"state_file_.{init_datestr}_00000.nc"),
    "STATENAME":  os.path.join(statefile_dir, "state_file_"),
    "STATEYEAR": stateyear,
    "STATEMONTH": statemonth,
    "STATEDAY": stateday,
    # Add other prefixes and their corresponding values here
    }
    # Determine which prefixes to use
    if current_date ==  startstamp:
        current_prefixes = prefixes_firststep
    else:
        current_prefixes = prefixes

    # Update the prefixes with the current date
    current_prefixes["STARTYEAR"] = startyear
    current_prefixes["STARTMONTH"] = startmonth
    current_prefixes["STARTDAY"] = startday
    current_prefixes["ENDYEAR"] = endyear
    current_prefixes["ENDMONTH"] = endmonth
    current_prefixes["ENDDAY"] = endday
    current_prefixes["STATENAME"] = os.path.join(statefile_dir, "state_file_")
    current_prefixes["STATEYEAR"] = stateyear
    current_prefixes["STATEMONTH"] = statemonth
    current_prefixes["STATEDAY"] = stateday
    if "INIT_STATE" in current_prefixes:
        current_prefixes["INIT_STATE"] = os.path.join(statefile_dir, f"state_file_.{init_datestr}_00000.nc")
        
    with open(filepath, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        for prefix, value in current_prefixes.items():
            if prefix in line:
                lines[i] = f"{prefix}               {value}\n"
                break

    # Write the modified lines back to the file
    parameter_file = os.path.join(configfile_dir, f"config_{startyear}_{startmonth}.txt")
    with open(parameter_file, 'w') as file:
        file.writelines(lines)

    # Run VIC
    command = [vic_executable, '-g', parameter_file]
    try:
        subprocess.run(command, check=True, shell=False)
        print("VIC-WUR run successfully for time step [{}-{}]".format(startyear, startmonth))
    except subprocess.CalledProcessError:
        print("VIC模型运行失败")
        raise SystemExit("Stopping the loop due to failure in VIC execution.")
        # Move to the next date
    
    current_date += relativedelta(months=1)
    

# %%
