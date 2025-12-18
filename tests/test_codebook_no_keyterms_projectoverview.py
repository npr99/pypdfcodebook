#!/usr/bin/env python3
"""
Test making a codebook without keyterms or projectoverview files.

******************************************************************************
* Project: pypdfcodebook                                                     *
* License: BSD 3-Clause License                                              *
* Author/Maintainer: Nathanael Rosenheim                                     *
* Copyright (c) 2025 Nathanael Rosenheim                                     *
******************************************************************************

Made with assistance from Claude Sonnet 4 LLM in VS Code Agent Mode.

Date Last Modified: December 17, 2025
"""

import pandas as pd
from src.pypdfcodebook.pdfcb_03c_codebook import codebook
import os


def test_codebook_no_keyterms_projectoverview():
    # Sample data
    data = {
        'id': [1, 2, 3, 4],
        'age': [25, 30, 22, 40],
        'gender': ['M', 'F', 'F', 'M'],
        'score': [88.5, 92.0, 79.5, 85.0]
    }
    df = pd.DataFrame(data)

    # Minimal datastructure
    datastructure = {
        'id': {
            'DataType': 'Int',
            'label': 'Identifier',
            'pyType': 'int',
            'AnalysisUnit': 'Person',
            'MeasureUnit': 'ID',
        },
        'age': {
            'DataType': 'Int',
            'label': 'Age in years',
            'pyType': 'int',
            'AnalysisUnit': 'Person',
            'MeasureUnit': 'Years',
        },
        'gender': {
            'DataType': 'String',
            'label': 'Gender',
            'pyType': 'category',
            'AnalysisUnit': 'Person',
            'MeasureUnit': 'Gender',
            'primary_key': 'id',
            'categories_dict': {
                'M': 'Male',
                'F': 'Female',
            },
        },
        'score': {
            'DataType': 'Float',
            'label': 'Test Score',
            'pyType': 'float',
            'AnalysisUnit': 'Person',
            'MeasureUnit': 'Score',
        },
    }

    # Output folder setup
    output_folder = "./tests/example_codebooks"

    # Create codebook instance with no keyterms or projectoverview
    # Output folder is now optional - this will save to current directory
    cb = codebook(
        input_df=df,
        header_title="Sample Codebook v2 (Current Dir)",
        datastructure=datastructure,
        output_filename="test_codebook_v2_current_dir"
    )
    cb.create_codebook()
    
    # Test with explicit output folder as well
    cb_explicit = codebook(
        input_df=df,
        header_title="Sample Codebook v2 (Explicit Dir)",
        datastructure=datastructure,
        output_filename="test_codebook_v2_explicit_dir",
        outputfolder=output_folder
    )
    cb_explicit.create_codebook()
    
    # Assert files were created
    current_dir_file = os.path.join(os.getcwd(), "test_codebook_v2_current_dir.pdf")
    explicit_dir_file = os.path.join(output_folder, "test_codebook_v2_explicit_dir.pdf")
    
    assert os.path.exists(current_dir_file), f"Current dir PDF not created: {current_dir_file}"
    assert os.path.exists(explicit_dir_file), f"Explicit dir PDF not created: {explicit_dir_file}"
    
    print(f"✓ Codebook PDF (current dir) generated: {current_dir_file}")
    print(f"✓ Codebook PDF (explicit dir) generated: {explicit_dir_file}")

    # Clean up generated file in current working directory
    os.remove(current_dir_file)
if __name__ == "__main__":
    test_codebook_no_keyterms_projectoverview()
