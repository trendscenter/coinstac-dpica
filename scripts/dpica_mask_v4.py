'''
Decentralized Parallel ICA (“dpICA”) : COINSTAC simulator
This script computes pICA using the INFOMAX criteria in decentralized environment.
Creator : Chan Panichvatana (cpanichvatana1@student.gsu.edu)
Reference: Parallel Independent Component Analysis (pICA): (Liu et al. 2009)
'''

import os
import nibabel as nib
import numpy as np

sep = os.sep

def get_files_or_folders_in_dir(dir, fileType = 'directories'):
    with os.scandir(dir) as directory:
        if fileType == 'directories':
            filesOrDirs = [entry.name for entry in directory if entry.is_dir()]
        else:
            filesOrDirs = [entry.name for entry in directory if not entry.is_dir()]
    return filesOrDirs

def pica_masked_Modality_X_creation(data_path_input, mask_file_location_input):
    mask_data = nib.load(mask_file_location_input).get_fdata()  #
    folder1 = get_files_or_folders_in_dir(data_path_input)
    fmri_1d_masked_all = []
    fmri_1d_mat_masked_all = []
    fmri_subject_all = []

    for subject_folders in folder1:
        fmri_subject_all.append(subject_folders)
        folder2 = get_files_or_folders_in_dir(os.path.join(data_path_input, subject_folders))
        for fmri_folders in folder2:
            files3 = get_files_or_folders_in_dir(os.path.join(data_path_input, subject_folders, fmri_folders), 'files')
            for img_file in files3:
                if img_file[-3:] == "img":

                    data = nib.load(os.path.join(data_path_input, subject_folders, fmri_folders, img_file)).get_fdata()
                    data = np.squeeze(data, 3)
                    # Masking data
                    data_masked = data[mask_data > 0]
                    data = data.T
                    data = data[mask_data.T > 0]

                    fmri_1d_masked_all.append(data_masked)
                    fmri_1d_mat_masked_all.append(data)

    fmri_1d_masked_all = np.asarray(fmri_1d_masked_all)

    return (fmri_1d_masked_all, fmri_1d_masked_all.shape[0], fmri_1d_masked_all.shape[1])


def pica_Modality_Y_creation(data_path_input):

    folder1 = get_files_or_folders_in_dir(data_path_input)
    snp_1d_all = []

    for subject_folders in folder1:
        folder2 = get_files_or_folders_in_dir(os.path.join(data_path_input, subject_folders))
        for snp_folders in folder2:
            files3 = get_files_or_folders_in_dir(os.path.join(data_path_input, subject_folders, snp_folders), 'files')
            for img_file in files3:
                if img_file[-3:] == "asc":
                    fname = os.path.join(data_path_input, subject_folders, snp_folders, img_file)
                    snp_1d_all.append(np.genfromtxt(fname, dtype=float))

    snp_1d_all = np.asarray(snp_1d_all)

    return (snp_1d_all, snp_1d_all.shape[0], snp_1d_all.shape[1])


def pica_Modality_XY_creation_from_file1(data_path_input, fmri_file_name):
    data_1d_all = []
    data_1d_all = pica_import_csv_to_array(data_path_input, fmri_file_name)

    return (data_1d_all, data_1d_all.shape[0], data_1d_all.shape[1])


def pica_import_csv_to_array(data_path_input, file_name_input):
    import csv

    file_name = os.path.join(data_path_input, file_name_input)

    array_1d_output = []
    with open(file_name, newline='') as csvfile:
        array_1d_output = list(csv.reader(csvfile))


    array_1d_output = np.asarray(array_1d_output, dtype=float)


    return (array_1d_output)
