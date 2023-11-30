#%%
import os
os.chdir('/lustre/nobackup/WUR/ESG/liu297/gitrepo/VIC-WUR-GWM-1910/vic_online/python')
%env LD_LIBRARY_PATH=/shared/legacyapps/netcdf/gcc/64/4.6.1/lib:$LD_LIBRARY_PATH   # for netcdf
import numpy as np
import flopy
import pandas as pd
import netCDF4 as nc
import xarray as xr
import subprocess  # for calling shell commands
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import support_function as sf
from config_module import config_indus_ubuntu
from osgeo import gdal
from netCDF4 import Dataset, date2num
from matplotlib import pyplot as plt
#%%










#%% loop for mfrun
# layer2_head = {} # top
layer1_head = {} # top
# layer1_head = {} # bot
layer2_head = {} # bot

for stress_period,date in zip(sp, sp_date):
    if (stress_period==0):
        print('assign steady-state computed head as the starting head for stress period 0')
        startinghead = initial_head()
    else:
        startingheadl2 = layer2_head[stress_period-1] # bot
        startingheadl1 = layer1_head[stress_period-1] # top
        # startinghead = [startingheadl2,startingheadl2]
        startinghead = [startingheadl1,startingheadl2]
        print(f"start assigning the variables for stress period {stress_period}...\n")
    Nlay,Nrow,Ncol,delrow,delcol,topl1,botm = dis_ic_parameter()
    k_hor,k_ver,stor = npf_parameter()
    RCHstress_period_data = rch_input(ts_gwrecharge[stress_period])
    RIVstress_period_data = riv_input(ts_discharge[stress_period],qbank)
    CHDstress_period_data = chd_input(stress_period)
    idomain1 = [idomain,idomain]
    name = '2Ltrans_off'
    print('finish assigning variables \n')
    print(f"writing the flopy variables for stress period {stress_period}...\n")
    sim = flopy.mf6.MFSimulation(
        sim_name=name,version='mf6', sim_ws=workspace, exe_name = exedir,
        verbosity_level = 1, continue_ = False, nocheck = True,
        memory_print_option = None, write_headers = True)
    tdis = flopy.mf6.ModflowTdis(
        sim,time_units= "DAYS", start_date_time = None,nper= 1,                     
        perioddata= [(perioddata[stress_period][0],perioddata[stress_period][1],perioddata[stress_period][2])]
        )
    rclose = 1000
    ims = flopy.mf6.ModflowIms(
        sim, complexity='COMPLEX', print_option="SUMMARY",
            outer_dvclose=50, inner_dvclose=50, under_relaxation="simple",
            under_relaxation_gamma=0.9, relaxation_factor=0,
            linear_acceleration="bicgstab", outer_maximum = 100, 
            inner_maximum = 500, rcloserecord="{} strict".format(rclose) )
    model_nam_file = f"{name}.nam"   
    gwf = flopy.mf6.ModflowGwf(
        sim, modelname = name, model_nam_file = model_nam_file,
        exe_name = exedir, model_rel_path = '.', list= None,
        print_input = False, print_flows = False, save_flows = True)
    dis = flopy.mf6.ModflowGwfdis(
        gwf,length_units = "METERS",nogrb = True, xorigin = 0,yorigin = 0,
        angrot = 0,nlay=Nlay, nrow=Nrow, ncol=Ncol,
        idomain = idomain1, delr=delrow,delc=delcol,top=topl1, botm=botm)
    npf = flopy.mf6.ModflowGwfnpf(
        gwf, save_flows = False, print_flows = False, save_specific_discharge =False,
        save_saturation = False, perioddata = None, dev_no_newton = False,
        icelltype = 0,  k = k_hor, k33 = k_ver)
    sto = flopy.mf6.ModflowGwfsto(
        gwf, save_flows=None, storagecoefficient=True, 
        ss_confined_only=None, iconvert=0,ss=stor, #steady_state=None,
        transient=True)
    chd = flopy.mf6.ModflowGwfchd(
        gwf,  print_input = False, print_flows = False, save_flows = True,
        stress_period_data=CHDstress_period_data)
    ic = flopy.mf6.ModflowGwfic(
        gwf, strt = startinghead)
    rch = flopy.mf6.ModflowGwfrch(
        gwf,stress_period_data=RCHstress_period_data)
    riv = flopy.mf6.ModflowGwfriv(
        gwf,stress_period_data= RIVstress_period_data)
    saverecord = [("HEAD", "ALL"), ("BUDGET", "ALL")]
    printrecord = [("HEAD", "ALL"), ("BUDGET", "ALL")]
    headfile = "{}_{}.hds".format(name,date)
    head_filerecord = [headfile]
    budgetfile = "{}.cbb".format(name)
    budget_filerecord = [budgetfile]
    
    oc = flopy.mf6.modflow.mfgwfoc.ModflowGwfoc(
        gwf,saverecord=saverecord,head_filerecord=head_filerecord,
        budget_filerecord=budget_filerecord)
    print('finish writing the flopy variables \n')
    print(f"writing the simulation for stress period {stress_period}...\n")
    sim.write_simulation()
    print('finish writing the simulation \n')
    print(f"running the simulation for stress period {stress_period}...\n")
    success, buff = sim.run_simulation()
    if not success:
        raise Exception(f"MODFLOW 6 did not terminate normally for stressperiod: {stress_period}\n")
    else:
        print(f"MODFLOW 6 terminated normally for stressperiod: {stress_period}\n")
        print(f"extracting the head and budget files for stress period {stress_period}...\n")
        head = flopy.utils.binaryfile.HeadFile(outputdir+headfile)
        layer1_head[stress_period] = head.get_data()[0] # top
        layer2_head[stress_period] = head.get_data()[1] # bot

## save head to nc
indus_simhead_path = '/lustre/nobackup/WUR/ESG/yuan018/domain_Indus.nc' # prepare a indus domain nc file, put somewhere as indus_simhead_path
nc_indus_simhead = nc.Dataset(indus_simhead_path, 'a')
lon = nc_indus_simhead.variables['lon'][:]
lat = nc_indus_simhead.variables['lat'][:]
mask = nc_indus_simhead.variables['mask'][:]
mask = mask.mask

# create time dim and variable
start_date = datetime(1968, 1, 1)
end_date = datetime(2000, 12, 31)
num_time_steps = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1
time_dim = nc_indus_simhead.createDimension('time', num_time_steps)
time_var = nc_indus_simhead.createVariable('time', np.float64, ('time',))
time_var.units = 'days since 1968-01-01'  # set time unit

# create time step
time_steps = [start_date + relativedelta(months=i) for i in range(0, (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1)]
time_data = date2num(time_steps, units=time_var.units, calendar='gregorian')
time_var[:] = time_data

# create water level variable, add it to time dim
# l2_gw_head = nc_indus_simhead.createVariable('bothead', np.float32, ('time','lat', 'lon'))# top layer water head
# l2_gw_head.units = 'meters'
# l1_gw_head = nc_indus_simhead.createVariable('tophead', np.float32, ('time','lat', 'lon'))
# l1_gw_head.units = 'meters'

l1_gw_head = nc_indus_simhead.createVariable('tophead', np.float32, ('time','lat', 'lon'))# top layer water head
l1_gw_head.units = 'meters'
l2_gw_head = nc_indus_simhead.createVariable('bothead', np.float32, ('time','lat', 'lon'))# bot layer water head
l2_gw_head.units = 'meters'

for key in range(9999): # write a big number
    if key in layer1_head: # layer1_head: dict
        layer1_head_2d_array = layer1_head[key] # key: month
        rows, cols = len(layer1_head_2d_array), len(layer1_head_2d_array[0])
        layer1_head_3d_array = layer1_head_2d_array.reshape(1, rows, cols) # reshape to a 3D array
        l1_gw_head[key, :, :] = layer1_head_3d_array

for key in range(9999): # write a big number
    if key in layer2_head: # layer2_head: dict
        layer2_head_2d_array = layer2_head[key] # key: month
        rows, cols = len(layer2_head_2d_array), len(layer2_head_2d_array[0])
        layer2_head_3d_array = layer2_head_2d_array.reshape(1, rows, cols) # reshape to a 3D array
        l2_gw_head[key, :, :] = layer2_head_3d_array


topl1_gwl.close()
topl2_gwl.close()
