import os


# nairfoil = 'r02000'; mach = 0.095
# nairfoil = 'r02800'; mach = 0.105
# nairfoil = 'r04200'; mach = 0.127
# nairfoil = 'r05500'; mach = 0.147
# nairfoil = 'r07100'; mach = 0.168
# nairfoil = 'r08400'; mach = 0.184
# nairfoil = 'r09900'; mach = 0.197
# nairfoil = 'r11200'; mach = 0.204
# nairfoil = 'r12700'; mach = 0.206
# nairfoil = 'r14100'; mach = 0.204
# nairfoil = 'r15600'; mach = 0.198
# nairfoil = 'r16900'; mach = 0.189
# nairfoil = 'r18500'; mach = 0.172
# nairfoil = 'r19600'; mach = 0.157
nairfoil = 'r20500'; mach = 0.142
# nairfoil = 'r21500'; mach = 0.112
# nairfoil = 'r22000'; mach = 0.082
# nairfoil = 't185'; mach = 0.172

# Angles of attack for airfoil simulation
aoas = [-4.0, -2.0, 0.0, 2.0, 4.0, 6.0, 7.0, 8.0,
        9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
# aoas = [4.0, 6.0]
template_journal = 'default_sst.jou'
ntype = 'st'
nsetup = 'sst'
out_path = './output'


def create_sim_name(nairfoil, ntype, nsetup, aoa, optional=None):
    """ Returns the full name of the simulation. """
    # Take care of optional string
    if optional is None:
        optional = ''
    else:
        optional = '_{}'.format(optional)
    # Construct sim_name
    if aoa < 0:
        sim_name = '{}_{}_{}_m{:0=5.2f}{}'.format(nairfoil, ntype, nsetup,
                                                  abs(aoa), optional)
    else:
        sim_name = '{}_{}_{}_p{:0=5.2f}{}'.format(nairfoil, ntype, nsetup,
                                                  abs(aoa), optional)
    return sim_name

# Get output path
out_path = os.path.join(out_path, nairfoil)

job_sh_names = []
for aoa in aoas:
    sim_name = create_sim_name(nairfoil, ntype, nsetup, aoa)

    # Create fluent journal file
    with open(template_journal, 'r') as f:
        journal_txt = f.read()
    journal_txt = journal_txt.replace('AOA', str(aoa))
    journal_txt = journal_txt.replace('MACH', str(mach))
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
send_to_queue_txt = ['#!/bin/sh', '']
for job_name in job_sh_names:
    send_to_queue_txt.append('qsub ' + job_name)
for job_name in job_sh_names:
    send_to_queue_txt.append('rm ' + job_name)
send_to_queue_txt = '\n'.join(send_to_queue_txt)
send_to_queue_path = os.path.join(out_path, 'send_to_queue.sh')
with open(send_to_queue_path, 'w') \
        as f:
            f.write(send_to_queue_txt)
# Make shell script executable
st = os.stat(send_to_queue_path)
os.chmod(send_to_queue_path, st.st_mode | 0111)
print('Done writing all files!')
