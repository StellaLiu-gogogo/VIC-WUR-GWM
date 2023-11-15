from os.path import join
import os
import subprocess
from datetime import datetime, timedelta
import config_module

def prepare_vic(startyear, startmonth, startday, endyear, endmonth, endday, 
            stateyear, statemonth, stateday, init_date, init_datestr,
            config):
    print("startyear,month, day is {},{},{}".format(startyear, startmonth, startday))
    print("end year, month, day is {},{},{}".format(endyear, endmonth, endday))
    print("statefile wll be save for {},{},{}".format(stateyear, statemonth, stateday))
    prefixes_firststep = {
    "STARTYEAR": startyear,    "STARTMONTH": startmonth,    "STARTDAY": startday,
    "ENDYEAR": endyear,    "ENDMONTH": endmonth,    "ENDDAY": endday,
    "STATENAME":  os.path.join(config.statefile_dir, "state_file_"),
    "STATEYEAR": stateyear,    "STATEMONTH": statemonth,    "STATEDAY": stateday, 
    # Add other prefixes and their corresponding values here later if necessary
    }
    prefixes = {
    "STARTYEAR": startyear,    "STARTMONTH": startmonth,    "STARTDAY": startday,
    "ENDYEAR": endyear,    "ENDMONTH": endmonth,    "ENDDAY": endday,
    "INIT_STATE": os.path.join(config.statefile_dir, f"state_file_.{init_datestr}_00000.nc"),
    "STATENAME":  os.path.join(config.statefile_dir, "state_file_"),
    "STATEYEAR": stateyear,    "STATEMONTH": statemonth,    "STATEDAY": stateday,
    # Add other prefixes and their corresponding values here later if necessary
    }
    current_date = datetime(startyear, startmonth, startday)
    # Determine which prefixes to use
    if current_date ==  config.startstamp:
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
    current_prefixes["STATENAME"] = os.path.join(config.statefile_dir, "state_file_")
    current_prefixes["STATEYEAR"] = stateyear
    current_prefixes["STATEMONTH"] = statemonth
    current_prefixes["STATEDAY"] = stateday
    if "INIT_STATE" in current_prefixes:
        current_prefixes["INIT_STATE"] = os.path.join(config.statefile_dir, f"state_file_.{init_datestr}_00000.nc")
    
    with open(config.template_dir, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        for prefix, value in current_prefixes.items():
            if prefix in line:
                lines[i] = f"{prefix}               {value}\n"
                break    
    # Write the modified lines back to the file
    config_file = os.path.join(config.configfile_dir, f"config_{startyear}_{startmonth}.txt")
    with open(config_file, 'w') as file:
        file.writelines(lines)
        
    return config_file


def run_vic(config, config_file, startyear, startmonth):
    vic_executable = config.vic_executable
    # first load the netcdf module
    #command0 = ['module load netcdf']
    #command = [vic_executable, '-g', config_file]
    #process = subprocess.Popen(command0, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Get the output and errors
    #stdout, stderr = process.communicate()

    #if process.returncode != 0:
    #    print(f'Error: {stderr.decode()}')
    #else:
    #    print(f'Success: {stdout.decode()}')
    
    
    
    try:
        command = 'bash -c "module load netcdf; {} -g {}"'.format(vic_executable, config_file)
        subprocess.run(command, check=True, shell=True)
        print("VIC-WUR run successfully for time step [{}-{}]".format(startyear, startmonth))
    except subprocess.CalledProcessError:
        raise SystemExit("Stopping the simulation due to failure in VIC execution.")
    
