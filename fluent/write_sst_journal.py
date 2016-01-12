import os
import fluutils as futils


# nairfoil = 'e44r02000'; mach = 0.0387; chord = 2.453037
# nairfoil = 'e44r02800'; mach = 0.0439; chord = 2.402322
# nairfoil = 'e44r04200'; mach = 0.0551; chord = 2.306531
# nairfoil = 'e44r05500'; mach = 0.0667; chord = 2.204551
# nairfoil = 'e44r07100'; mach = 0.0815; chord = 2.065402
# nairfoil = 'e44r08400'; mach = 0.0949; chord = 1.942005
# nairfoil = 'e44r09900'; mach = 0.1100; chord = 1.790112
# nairfoil = 'e44r11200'; mach = 0.1232; chord = 1.652348
# nairfoil = 'e44r12700'; mach = 0.1386; chord = 1.487661
# nairfoil = 'e44r14100'; mach = 0.1531; chord = 1.335335
# nairfoil = 'e44r15600'; mach = 0.1687; chord = 1.175150
# nairfoil = 'e44r16900'; mach = 0.1823; chord = 1.035377
# nairfoil = 'e44r18500'; mach = 0.1990; chord = 0.866005
nairfoil = 'e44r19600'; mach = 0.2106; chord = 0.746913
# nairfoil = 'e44r20500'; mach = 0.2200; chord = 0.647561
# nairfoil = 'e44r21500'; mach = 0.2305; chord = 0.485032
# nairfoil = 'e44r22000'; mach = 0.2358; chord = 0.349029

# Angles of attack for airfoil simulation
aoas = [-4.0, -2.0, 0.0, 2.0, 4.0, 6.0, 7.0, 8.0, 9.0, 10.0]
# aoas = [4.0, 6.0]
template_journal = 'default_sst.jou'
nsetup = 'sst'
ntype = 'st'
out_path = 'output'

# Get output path
out_path = os.path.join(out_path, nairfoil)
# Create fluent journal and shell script for pbs queue
job_sh_names = []
for aoa in aoas:
    sim_name = futils.create_sim_name(nairfoil, ntype, nsetup, aoa)

    # Create fluent journal file
    with open(template_journal, 'r') as f:
        journal_txt = f.read()
        journal_txt = journal_txt.replace('AOA', str(aoa))
    journal_txt = journal_txt.replace('MACH', str(mach))
    journal_txt = journal_txt.replace('CHORD', str(chord))
    journal_txt = journal_txt.replace('OUT_TECPLOT', '{}.plt'.format(sim_name))
    journal_txt = journal_txt.replace('CASE_FILE', '{}.cas'.format(nairfoil))
    journal_txt = journal_txt.replace('OUT.CL', '{}.cl'.format(sim_name))
    journal_txt = journal_txt.replace('OUT.CD', '{}.cd'.format(sim_name))
    journal_txt = journal_txt.replace('OUT.CM', '{}.cm'.format(sim_name))
    journal_txt = journal_txt.replace('OUT_RESULTS', '{}.cas.gz'.
                                      format(sim_name))
    jou_name = sim_name + '.jou'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    with open(os.path.join(out_path, jou_name), 'w') as f:
        f.write(journal_txt)

    # Create shell script for simulation
    with open('job.sh', 'r') as f:
        job_txt = f.read()
    job_txt = job_txt.replace('SIMNAME', sim_name)
    job_txt = job_txt.replace('in.jou', sim_name + '.jou')
    job_txt = job_txt.replace('fluent.out', sim_name + '.out')
    job_out = sim_name + '.qsh'
    job_out_path = os.path.join(out_path, job_out)
    with open(job_out_path, 'w') as f:
        f.write(job_txt)
    # Make shell script executable
    st = os.stat(job_out_path)
    os.chmod(job_out_path, st.st_mode | 0111)
    # Append script name to list of job names
    job_sh_names.append(job_out)

# Create shell script to submit all jobs at once
# send_to_queue_txt = ['#!/bin/sh', '']
# for job_name in job_sh_names:
#     send_to_queue_txt.append('qsub ' + job_name)
# for job_name in job_sh_names:
#     send_to_queue_txt.append('rm ' + job_name)
# send_to_queue_txt = '\n'.join(send_to_queue_txt)
# send_to_queue_path = os.path.join(out_path, 'send_to_queue.sh')
# with open(send_to_queue_path, 'w') \
#         as f:
#             f.write(send_to_queue_txt)
# # Make shell script executable
# st = os.stat(send_to_queue_path)
# os.chmod(send_to_queue_path, st.st_mode | 0111)
print('Done writing all files!')
