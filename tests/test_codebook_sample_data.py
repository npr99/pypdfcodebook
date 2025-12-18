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

def test_codebook_with_sample_data():
    # Sample data directory
    sample_dir = os.path.join(os.path.dirname(__file__), '..', 'sample_data')
    
    # Define filenames - codebook class handles path building
    projectoverview_filename = 'pdfcb_00a_projectoverview.md'
    keyterms_filename = 'pdfcb_00b_keyterms.md'
    csv_filename = 'pdfcb_00c_sampledata.csv'
    datastructure_filename = 'pdfcb_00d_data_structure.py'

    output_filename = "test_sample_data"
    output_folder = "./tests/example_codebooks"
    output_filename_path = os.path.join(output_folder, f"{output_filename}.pdf")


    # Create codebook with new simplified API
    pdfcodebook = codebook(
        input_csv_filename=csv_filename,  # Use CSV filename instead of loading manually
        header_title='Test pyPDFCodebook',
        input_dir=sample_dir,  # One directory for all input files
        datastructure_filename=datastructure_filename,
        projectoverview_filename=projectoverview_filename,
        keyterms_filename=keyterms_filename,
        output_filename=output_filename,
        outputfolder=output_folder
    )
    pdfcodebook.create_codebook()

    # Assert output file was created
    assert os.path.exists(output_filename_path)
