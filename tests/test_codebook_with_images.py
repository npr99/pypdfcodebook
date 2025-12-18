"""
******************************************************************************
* Project: pypdfcodebook                                                     *
* License: BSD 3-Clause License                                              *
* Author/Maintainer: Nathanael Rosenheim                                     *
* Copyright (c) 2025 Nathanael Rosenheim                                     *
******************************************************************************

Made with assistance from Claude Sonnet 4 LLM in VS Code Agent Mode.

Date Last Modified: December 17, 2025
"""

import os
import pandas as pd
import importlib.util
from src.pypdfcodebook.pdfcb_03c_codebook import codebook


def test_codebook_with_images():
    # Paths to sample files (robust path building)
    sample_dir = os.path.join(os.path.dirname(__file__), '..', 'sample_data')

    # simplified path building for test
    # sample_dir = '../sample_data'
    
    # Define filenames (no path building needed - codebook class handles this)
    csv_filename = 'pdfcb_00c_sampledata.csv'
    datastructure_filename = 'pdfcb_00d_data_structure.py'
    projectoverview_filename = 'pdfcb_00a_projectoverview.md'
    keyterms_filename = 'pdfcb_00b_keyterms.md'
    footer_image_filename = 'pdfcb_00e_samplelogo.png'
    
    # Define figure list - users can easily modify this list
    figure_filenames = [
        'pdfcb_00f_satisfaction_dist.png',  # Satisfaction histogram
        'pdfcb_00g_age_dist.png',  # Age distribution
        'pdfcb_00h_region_dist.png'  # Regional pie charts
    ]

    # Output setup - codebook class now handles folder creation automatically
    output_folder = "./tests/example_codebooks"
    output_filename = "test_codebook_with_images_simplified"
    
    pdfcodebook = codebook(
        input_csv_filename=csv_filename,  # New CSV loading approach!
        header_title='Regional Satisfaction Survey Codebook',
        input_dir=sample_dir,  # One directory for all files
        datastructure_filename=datastructure_filename,
        projectoverview_filename=projectoverview_filename,
        keyterms_filename=keyterms_filename,
        figure_filenames=figure_filenames,
        footer_image_filename=footer_image_filename,
        output_filename=output_filename,
        outputfolder=output_folder
    )
    pdfcodebook.create_codebook()
    
    # Assert output file was created
    output_filename_path = os.path.join(output_folder, f"{output_filename}.pdf")
    assert os.path.exists(output_filename_path)

