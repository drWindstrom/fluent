import sys
sys.path.append('/home/winstroth/src/python/fluent/fluent')
import fluutils as futils

# Angles of attack for airfoil simulation
aoas = [-4.0, -2.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0,
        11.0, 12.0]

airfoils = {}
airfoils['e44r02000'] = {'mach': 0.0387, 'chord': 2.453037, 'aoas': aoas}
airfoils['e44r02800'] = {'mach': 0.0439, 'chord': 2.402322, 'aoas': aoas}
airfoils['e44r04200'] = {'mach': 0.0551, 'chord': 2.306531, 'aoas': aoas}
airfoils['e44r05500'] = {'mach': 0.0667, 'chord': 2.204551, 'aoas': aoas}
airfoils['e44r07100'] = {'mach': 0.0815, 'chord': 2.065402, 'aoas': aoas}
airfoils['e44r08400'] = {'mach': 0.0949, 'chord': 1.942005, 'aoas': aoas}
airfoils['e44r09900'] = {'mach': 0.1100, 'chord': 1.790112, 'aoas': aoas}
airfoils['e44r11200'] = {'mach': 0.1232, 'chord': 1.652348, 'aoas': aoas}
airfoils['e44r12700'] = {'mach': 0.1386, 'chord': 1.487661, 'aoas': aoas}
airfoils['e44r14100'] = {'mach': 0.1531, 'chord': 1.335335, 'aoas': aoas}
airfoils['e44r15600'] = {'mach': 0.1687, 'chord': 1.175150, 'aoas': aoas}
airfoils['e44r16900'] = {'mach': 0.1823, 'chord': 1.035377, 'aoas': aoas}
airfoils['e44r18500'] = {'mach': 0.1990, 'chord': 0.866005, 'aoas': aoas}
airfoils['e44r19600'] = {'mach': 0.2106, 'chord': 0.746913, 'aoas': aoas}
airfoils['e44r20500'] = {'mach': 0.2200, 'chord': 0.647561, 'aoas': aoas}
airfoils['e44r21500'] = {'mach': 0.2305, 'chord': 0.485032, 'aoas': aoas}
airfoils['e44r22000'] = {'mach': 0.2358, 'chord': 0.349029, 'aoas': aoas}

futils.write_journals(airfoils, 'default_sst.jou', 'sst', 'st', 'output/jou')
futils.write_shell_scripts(airfoils, 'job.sh', 'sst', 'st', 'output/qsh')
