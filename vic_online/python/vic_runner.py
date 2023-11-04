from os.path import join
import os
import subprocess
from datetime import datetime, timedelta

def prepare_vic(startyear, startmonth, startday, endyear, endmonth, endday, 
            stateyear, statemonth, stateday, init_date, init_datestr,
            startstamp, filepath, statefile_dir, configfile_dir,vic_executable):
    print("startyear,month, day is {},{},{}".format(startyear, startmonth, startday))
    print("end year, month, day is {},{},{}".format(endyear, endmonth, endday))
    print("statefile wll be save for {},{},{}".format(stateyear, statemonth, stateday))
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
    current_date = datetime(startyear, startmonth, startday)
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
    config_file = os.path.join(configfile_dir, f"config_{startyear}_{startmonth}.txt")
    with open(config_file, 'w') as file:
        file.writelines(lines)
    return config_file


def run_vic(vic_executable, config_file, startyear, startmonth):
    command = [vic_executable, '-g', config_file]
    try:
        subprocess.run(command, check=True, shell=False)
        print("VIC-WUR run successfully for time step [{}-{}]".format(startyear, startmonth))
    except subprocess.CalledProcessError:
        print("VIC模型运行失败")
        raise SystemExit("Stopping the loop due to failure in VIC execution.")