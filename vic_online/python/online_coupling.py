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

prefixes_firststep = {
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
# Define the start and end dates
current_date = datetime(1968, 1, 1)
enddate = datetime(1975, 1, 1)

# Loop over the dates
while current_date < enddate:
    year, month, day = current_date.year, current_date.month, current_date.day
    _, lastday = calendar.monthrange(year, month) # to get the last day of the month

    statedate = current_date - timedelta(days=1) # to get the statefile date as a datetime object
    statedate_str = statedate.strftime('%Y%m%d')

    # Determine which prefixes to use
    if current_date == datetime(1968, 1, 1):
        current_prefixes = prefixes_firststep
    else:
        current_prefixes = prefixes

    # Update the prefixes with the current date
    current_prefixes["STARTYEAR"] = year
    current_prefixes["STARTMONTH"] = month
    current_prefixes["STARTDAY"] = day
    end_date = current_date + relativedelta(months=1)
    current_prefixes["ENDYEAR"] = end_date.year
    current_prefixes["ENDMONTH"] = end_date.month
    current_prefixes["ENDDAY"] = end_date.day - 1
    current_prefixes["STATENAME"] = os.path.join(statefile_dir, "state_file_")
    current_prefixes["STATEYEAR"] = year
    current_prefixes["STATEMONTH"] = month
    current_prefixes["STATEDAY"] = lastday
    if "INIT_STATE" in current_prefixes:
        current_prefixes["INIT_STATE"] = os.path.join(statefile_dir, f"state_file_.{statedate_str}_00000.nc")
        
    with open(filepath, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        for prefix, value in current_prefixes.items():
            if line.startswith(prefix):
                lines[i] = f"{prefix}               {value}\n"
                break

    # Write the modified lines back to the file
    parameter_file = os.path.join(configfile_dir, f"config_{year}_{month}.txt")
    with open(parameter_file, 'w') as file:
        file.writelines(lines)

    # Run VIC
    command = [vic_executable, '-g', parameter_file]
    try:
        subprocess.run(command, check=True, shell=False)
        print("VIC-WUR run successfully for time step [{}-{}]".format(year, month))
    except subprocess.CalledProcessError:
        print("VIC模型运行失败")
        raise SystemExit("Stopping the loop due to failure in VIC execution.")
        # Move to the next date
    current_date += timedelta(month=1)       
