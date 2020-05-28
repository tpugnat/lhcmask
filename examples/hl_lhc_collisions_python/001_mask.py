import os

#from cpymad.madx import Madx
from madxp import Madxp as Madx
import pymasktools as pmt
import optics_specific_tools as ost

beam_to_configure = 1

pmt.make_links(force=True, links_dict={
    'tracking_tools': '/afs/cern.ch/eng/tracking-tools',
    'modules': 'tracking_tools/modules',
    'tools': 'tracking_tools/tools',
    'beambeam_macros': 'tracking_tools/beambeam_macros',
    'errors': 'tracking_tools/errors'})


mad = Madx()

# Build sequence (to become python function)
mad.input(f'mylhcbeam = {beam_to_configure}')
mad.call('hl14_thin.madx')

# Make optics (to become python function)
mad.call('hl14_collision_optics.madx')

# Load parameters 
from parameters import parameters
pmt.checks_on_parameter_dict(parameters)


mad.set_variables_from_dict(params=parameters)

# Prepare sequences and attach beam
mad.call("modules/submodule_01a_preparation.madx")
mad.call("modules/submodule_01b_beam.madx")

# Test machine before any change
ost.twiss_and_check(mad, sequences_to_check=['lhcb1', 'lhcb2'],
        twiss_fname='twiss_from_optics',
        check_betas_at_ips=True, check_separations_at_ips=True)


#mad.call("modules/submodule_01c_phase.madx")



#mad.call("modules/module_02_lumilevel.madx")
#mad.call("modules/module_03_beambeam.madx")
#mad.call("modules/module_04_errors.madx")
#mad.call("modules/module_05_tuning.madx")
#mad.call("modules/module_06_generate.madx")
