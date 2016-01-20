import sys
sys.path.append('/home/winstroth/src/python/fluent/fluent')
import fluutils as futils

# Angles of attack for airfoil simulation
aoas = [-4.0, -2.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0,
        11.0, 12.0]

airfs_def = {}
airfs_def['e44r11200'] = {'mach': 0.1232, 'reno': 4.72E+06, 'aoas': aoas}
airfs_def['e44r12700'] = {'mach': 0.1386, 'reno': 4.78E+06, 'aoas': aoas}
airfs_def['e44r14100'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
airfs_def['e44r15600'] = {'mach': 0.1687, 'reno': 4.60E+06, 'aoas': aoas}
airfs_def['e44r16900'] = {'mach': 0.1823, 'reno': 4.38E+06, 'aoas': aoas}
airfs_def['e44r18500'] = {'mach': 0.1990, 'reno': 4.00E+06, 'aoas': aoas}
airfs_def['e44r19600'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
airfs_def['e44r20500'] = {'mach': 0.2200, 'reno': 3.30E+06, 'aoas': aoas}
airfs_def['e44r21500'] = {'mach': 0.2305, 'reno': 2.59E+06, 'aoas': aoas}
airfs_def['e44r22000'] = {'mach': 0.2358, 'reno': 1.91E+06, 'aoas': aoas}

futils.write_journals(airfs_def, 'default_sst.jou', 'sst', 'st', 'output/jou')
futils.write_shell_scripts(airfs_def, 'job.sh', 'sst', 'st', 'output/qsh')
