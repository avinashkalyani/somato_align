#!/usr/bin/env python3

"""
Script to run brainiak's shared response model on our data.

We'll start with only the first run. Later, we might want to think about concatinating runs in a sensible fashion.

TODO: Generate and apply brain masks with BET.
"""

import glob
import numpy as np
import os
import pickle
from os.path import join as pjoin
from scipy import stats

from brainiak.funcalign.srm import SRM
from brainiak.io import load_images


def grab_bold_data(cond_id='D1_D5',
                   ds_dir='/data/BnB_USER/oliver/somato',
                   testsubs=3,
                   melodic_outdir=''):
    """
    Get file paths for our bold data for a given run.
    """
    print('grabbing data')
    sub_ids = [os.path.basename(subdir)
               for subdir in glob.glob(ds_dir + '/*')]
    if testsubs:
        sub_ids = sub_ids[:testsubs]
    bold_files = [pjoin(ds_dir, sub_id, cond_id, 'data.nii.gz')
                  for sub_id in sub_ids]
    return bold_files, sub_ids


def boldfiles_to_arrays(bold_files,
                        z_score=True):
    """
    Load bold data into list of arrays (bc that's what brainiak wants)
    """
    print('loading bold_files')
    # create generator that returns nibabel nifti instances
    nibs_gen = load_images(bold_files)
    # get numpy array data from each those instances (might take a while)
    print('converting to np arrays')
    bold_arrays_list = [np.reshape(nib_instance.get_fdata(), (1327104, 256))  # TODO: don't hard code this
                        for nib_instance in nibs_gen]
    print('z-scoring')
    if z_score:
        zscored = []
        for bold_array in bold_arrays_list:
            zs = stats.zscore(bold_array, axis=1, ddof=1)
            zs = np.nan_to_num(zs)
            zscored.append(zs)
            # TODO: put z-scoring in preprocessing pipeline later
        bold_arrays_list = zscored

    return bold_arrays_list


def train_srm(training_data,
              pickle_outdir='/home/homeGlobal/oli/somato/scratch/srm',
              n_comps=50,
              n_iters=20):
    # set up
    print('setting up srm')
    srm = SRM(n_iter=n_iters, features=n_comps)
    # fit
    print('fitting srm')
    srm.fit(training_data)
    # save srm as pickle
    print('saving srm as pickle')
    if pickle_outdir:
        if not os.path.exists(pickle_outdir):
            os.makedirs(pickle_outdir)
        outpickle = pjoin(pickle_outdir, 'srm.p')
        with open(outpickle, 'wb') as f:
            pickle.dump(srm, f)
    return srm


if __name__ == '__main__':
    bold_files, sub_ids = grab_bold_data()  # testsubs=3)
    bold_arrays = boldfiles_to_arrays(bold_files)
    srm = train_srm(bold_arrays)  # , n_comps=5, n_iters=5)
    print('done')
