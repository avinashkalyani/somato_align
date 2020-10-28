#  Functional alignment of somatosensory digit representations using 7T fMRI data

Code accompanying poster # 2197 at OHBM 2020. Authors: Oliver Contier, Dr. Esther Kühn, Prof. Michael Hanke.
The poster presents preliminary results of a lab rotation by Oliver Contier at the Research Center Jülich, Institute of Neuroscience and Medicine, Department Brain and Behavior (INM-7) headed by Prof. Simon Eickhoff.
The lab rotation was part of the Max Planck School of Cognition.

In order to generate the results:
Step1: ds_prerp.py (to modify the dataset and change headers)
Step2: roi_glm_ffx.py (uses nipype for glm analysis in order to produce the mask/roi)
Step3: srm_roi.py (runs srm and rsrm on the roi bold data to produce a rsrm.p file)
