import sys
sys.path.append('/home/winstroth/src/python/fluent/fluent')
import fluutils as futils

# Angles of attack for airfoil simulation
# aoas = [-8.0, -6.0, -4.0, -2.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0,
#         9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]

aoas = [-8.0, -6.0, -4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 4.0, 6.0, 8.0,
        9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 16.0, 18.0, 20.0]

airfs_def = {}
airfs_def['e44r02000'] = {'mach': 0.0387, 'reno': 2.20E+06, 'aoas': aoas}
airfs_def['e44r02800'] = {'mach': 0.0439, 'reno': 2.45E+06, 'aoas': aoas}
airfs_def['e44r04200'] = {'mach': 0.0551, 'reno': 2.94E+06, 'aoas': aoas}
airfs_def['e44r05500'] = {'mach': 0.0667, 'reno': 3.41E+06, 'aoas': aoas}
airfs_def['e44r07100'] = {'mach': 0.0815, 'reno': 3.90E+06, 'aoas': aoas}
airfs_def['e44r08400'] = {'mach': 0.0949, 'reno': 4.27E+06, 'aoas': aoas}
airfs_def['e44r09900'] = {'mach': 0.1100, 'reno': 4.56E+06, 'aoas': aoas}
# airfs_def['e44r11200'] = {'mach': 0.1232, 'reno': 4.72E+06, 'aoas': aoas}
# airfs_def['e44r12700'] = {'mach': 0.1386, 'reno': 4.78E+06, 'aoas': aoas}
# airfs_def['e44r14100'] = {'mach': 0.1531, 'reno': 4.74E+06, 'aoas': aoas}
# airfs_def['e44r15600'] = {'mach': 0.1687, 'reno': 4.60E+06, 'aoas': aoas}
# airfs_def['e44r16900'] = {'mach': 0.1823, 'reno': 4.38E+06, 'aoas': aoas}
# airfs_def['e44r18500'] = {'mach': 0.1990, 'reno': 4.00E+06, 'aoas': aoas}
# airfs_def['e44r19600'] = {'mach': 0.2106, 'reno': 3.65E+06, 'aoas': aoas}
# airfs_def['e44r20500'] = {'mach': 0.2200, 'reno': 3.30E+06, 'aoas': aoas}
# airfs_def['e44r21500'] = {'mach': 0.2305, 'reno': 2.59E+06, 'aoas': aoas}
# airfs_def['e44r22000'] = {'mach': 0.2358, 'reno': 1.91E+06, 'aoas': aoas}

# # SST turbulence model with coupled solver
# futils.write_journals(airfs_def, 'default_sst.jou', 'sst', 'st', 'output/sst/jou')
# futils.write_shell_scripts(airfs_def, 'job.sh', 'sst', 'st', 'output/sst/qsh')

# # ReTheta transition model with coupled solver
# futils.write_journals(airfs_def, 'default_reTheta.jou', 'reTheta', 'st', 'output/reTheta/jou')
# futils.write_shell_scripts(airfs_def, 'job.sh', 'reTheta', 'st', 'output/reTheta/qsh')

# # SST turbulence model with SIMPLE segregated solver
# futils.write_journals(airfs_def, 'default_sstSimple.jou', 'sstSimple', 'st', 'output/sstSimple/jou')
# futils.write_shell_scripts(airfs_def, 'job.sh', 'sstSimple', 'st', 'output/sstSimple/qsh')

# # ReTheta transition model with SIMPLE segregated solver
# futils.write_journals(airfs_def, 'default_reThetaSimple.jou', 'reThetaSimple', 'st', 'output/reThetaSimple/jou')
# futils.write_shell_scripts(airfs_def, 'job.sh', 'reThetaSimple', 'st', 'output/reThetaSimple/qsh')

# # SST turbulence model with SIMPLE segregated solver
# futils.write_journals(airfs_def, 'default_sstPiso.jou', 'sst', 'tr', 'output/sstPiso/jou')
# futils.write_shell_scripts(airfs_def, 'job_tr.sh', 'sst', 'tr', 'output/sstPiso/qsh')

# # SST turbulence model with coupled solver and pseudo transient option
futils.write_journals(airfs_def, 'default_sstPseudoTrans.jou', 'sst', 'st', 'output/sstPseudoTrans/jou')
futils.write_shell_scripts(airfs_def, 'job.sh', 'sst', 'st', 'output/sstPseudoTrans/qsh')

# # ReTheta transition model with coupled solver and pseudo transient option
futils.write_journals(airfs_def, 'default_reThetaPseudoTrans.jou', 'reTheta', 'st', 'output/reThetaPseudoTrans/jou')
futils.write_shell_scripts(airfs_def, 'job.sh', 'reTheta', 'st', 'output/reThetaPseudoTrans/qsh')
