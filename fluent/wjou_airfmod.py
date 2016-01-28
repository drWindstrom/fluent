import sys
sys.path.append('/home/winstroth/src/python/fluent/fluent')
import fluutils as futils

# Angles of attack for airfoil simulation
aoas = [-8.0, -6.0, -4.0, -2.0, 0.0, 2.0, 4.0, 6.0, 8.0,
        9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 16.0, 18.0, 20.0]

airfs_def = {}
airfs_def['e44r14100Alpha0.5LeRot'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100Alpha0.5TeRot'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100Alpha1.0LeRot'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100Alpha1.0TeRot'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100Alpha1.5LeRot'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100Alpha1.5TeRot'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100Alpha2.0LeRot'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100Alpha2.0TeRot'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.021ue0.22ampl0.0005p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.021ue0.22ampl0.0015p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.021ue0.22ampl0.003p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.021ue0.22ampl0.005p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.2ue0.4ampl0.0005p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.2ue0.4ampl0.0015p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.2ue0.4ampl0.003p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.2ue0.4ampl0.005p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.4ue0.6ampl0.0005p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.4ue0.6ampl0.0015p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.4ue0.6ampl0.003p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.4ue0.6ampl0.005p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.6ue0.8ampl0.0005p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.6ue0.8ampl0.0015p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.6ue0.8ampl0.003p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.6ue0.8ampl0.005p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.78ue0.98ampl0.0005p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.78ue0.98ampl0.0015p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.78ue0.98ampl0.003p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r14100us0.78ue0.98ampl0.005p2.0sineWave'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r19600Alpha0.5LeRot'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600Alpha0.5TeRot'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600Alpha1.0LeRot'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600Alpha1.0TeRot'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600Alpha1.5LeRot'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600Alpha1.5TeRot'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600Alpha2.0LeRot'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600Alpha2.0TeRot'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.02ue0.22ampl0.0005p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.02ue0.22ampl0.0015p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.02ue0.22ampl0.003p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.02ue0.22ampl0.005p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.2ue0.4ampl0.0005p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.2ue0.4ampl0.0015p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.2ue0.4ampl0.003p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.2ue0.4ampl0.005p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.4ue0.6ampl0.0005p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.4ue0.6ampl0.0015p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.4ue0.6ampl0.003p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.4ue0.6ampl0.005p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.6ue0.8ampl0.0005p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.6ue0.8ampl0.0015p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.6ue0.8ampl0.003p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.6ue0.8ampl0.005p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.78ue0.98ampl0.0005p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.78ue0.98ampl0.0015p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.78ue0.98ampl0.003p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r19600us0.78ue0.98ampl0.005p2.0sineWave'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}

# futils.write_journals(airfs_def, 'default_sst.jou', 'sst', 'st', 'output/jou')
# futils.write_shell_scripts(airfs_def, 'job.sh', 'sst', 'st', 'output/qsh')

futils.write_journals(airfs_def, 'default_reTheta.jou', 'reTheta', 'st', 'output/jou')
futils.write_shell_scripts(airfs_def, 'job.sh', 'reTheta', 'st', 'output/qsh')
