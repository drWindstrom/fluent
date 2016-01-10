import os


# Angles of attack for airfoil simulation
# aoas = [-4.0, -2.0, 0.0, 2.0, 4.0, 6.0, 7.0, 8.0,
#        9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
aoas = [10.0, 11.0, 12.0, 13.0, 14.0, 15.0]
template_journal = 'default_sst.jou'
setup_name = 'sst'


def create_sim_name(aoa, setup_name):
    """ Returns the full name of the simulation. """
    if aoa < 0:
        sim_name = 'm{:0=5.2f}_{}'.format(abs(aoa), setup_name)
    else:
        sim_name = 'p{:0=5.2f}_{}'.format(abs(aoa), setup_name)
    return sim_name

job_sh_names = []
for aoa in aoas:
    sim_name = create_sim_name(aoa, setup_name) # Example: p02.00_sst

    # Create fluent journal file
    with open(template_journal, 'r') as f:
        journal_txt = f.read()
    journal_txt = journal_txt.replace('AOA', str(aoa))
    journal_txt = journal_txt.replace('"out.cl"', '"{}.cl"'.format(sim_name))
    journal_txt = journal_txt.replace('"out.cd"', '"{}.cd"'.format(sim_name))
    journal_txt = journal_txt.replace('"out.cm"', '"{}.cm"'.format(sim_name))
    journal_txt = journal_txt.replace('"out_res.cas"', '"{}_res.cas"'.
                                      format(sim_name))
    jou_name = sim_name + '.jou'
    if not os.path.exists('./output'):
        os.makedirs('./output')
    with open(os.path.join('./output', jou_name), 'w') as f:
        f.write(journal_txt)

    # Create shell script for simulation
    with open('job.sh', 'r') as f:
        job_txt = f.read()
    job_txt = job_txt.replace('SIMNAME', sim_name)
    job_txt = job_txt.replace('in.jou', sim_name + '.jou')
    job_txt = job_txt.replace('fluent.out', sim_name + '.out')
    job_out = sim_name + '.sh'
    with open(os.path.join('./output', job_out), 'w') as f:
        f.write(job_txt)
    job_sh_names.append(job_out)

# Create shell script to submit all jobs at once
send_to_queue_txt = ['#!/bin/sh', '']
for job_name in job_sh_names:
    send_to_queue_txt.append('qsub ' + job_name)
send_to_queue_txt = '\n'.join(send_to_queue_txt)
with open(os.path.join('./output', 'send_to_queue.sh'), 'w') \
        as f:
            f.write(send_to_queue_txt)

print('Done writing all files!')
