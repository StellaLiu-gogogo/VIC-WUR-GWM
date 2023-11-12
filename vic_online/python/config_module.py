# config_module.py

import os
from datetime import datetime 
class config:
    def __init__(self):
        self.cwd = '/home/sliu/Documents/gitversion/VIC-WUR-GWM-1910/vic_online/'
        self.template_dir = os.path.join(self.cwd, 'python', 'VIC_config_file_naturalized_template_pyread_txt')
        self.statefile_dir = os.path.join(self.cwd , 'python', 'statefile')
        self.configfile_dir =  os.path.join(self.cwd , 'python', 'configfile')
        self.vic_executable = '/home/sliu/Documents/vic_indus/99SourceCode/VIC-WUR-GWM-1910/vic_offline/drivers/image/vic_image_gwm_offline.exe'
        self.startstamp =  datetime(1968, 1, 1)
        self.mfinput_dir = os.path.join(self.cwd, 'python', 'mfinput')
        self.output_dir = os.path.join(self.cwd, 'python', 'output')
    def set_cwd(self, cwd):
        self.cwd = cwd  
    def set_template_dir(self, template_dir):
        self.template_dir = template_dir
    def set_statefile_dir(self, statefile_dir):
        self.statefile_dir = statefile_dir
    def set_configfile_dir(self, configfile_dir):
        self.configfile_dir = configfile_dir
    def set_vic_executable(self, vic_executable):
        self.vic_executable = vic_executable
    def set_startstamp(self, startstamp):
        self.startstamp = startstamp
    def set_output_dir(self, output_dir):
        self.output_dir = output_dir
    def set_mfinput_dir(self, mfinput_dir):
        self.mfinput_dir = mfinput_dir


config_indus_ubuntu = config()
