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
from src.pypdfcodebook.pdfcb_03b_pdffunctions import PDF


def test_codebook_with_images(tmp_path):
    # Paths to sample files
    sample_dir = os.path.join(os.path.dirname(__file__), '..', 'sample_data')
    projectoverview_path = os.path.join(sample_dir, 'pdfcb_00a_projectoverview.md')
    keyterms_path = os.path.join(sample_dir,        'pdfcb_00b_keyterms.md')
    csv_path = os.path.join(sample_dir,             'pdfcb_00c_sampledata.csv')
    datastructure_path = os.path.join(sample_dir,   'pdfcb_00d_data_structure.py')
    footer_image_path = os.path.join(sample_dir, 'pdfcb_00e_samplelogo.png')
    
    # Define figure list - users can easily modify this list
    figure_filenames = [
        'pdfcb_00f_satisfaction_dist.png',  # Satisfaction histogram
        'pdfcb_00g_age_dist.png',  # Age distribution
        'pdfcb_00h_region_dist.png'  # Regional pie charts
    ]
    
    # Convert filenames to full paths
    figure_list_paths = [os.path.join(sample_dir, filename) for filename in figure_filenames]

    # Check if paths exist, else set to empty string or None
    projectoverview_path = projectoverview_path if os.path.exists(projectoverview_path) else ""
    keyterms_path = keyterms_path if os.path.exists(keyterms_path) else ""
    csv_path = csv_path if os.path.exists(csv_path) else ""
    datastructure_path = datastructure_path if os.path.exists(datastructure_path) else ""
    footer_image_path = footer_image_path if os.path.exists(footer_image_path) else ""
    # Keep figure_list_paths as is - individual validation happens later

    # Output folder setup
    output_folder = os.path.abspath("./tests/example_codebooks")
    os.makedirs(output_folder, exist_ok=True)

    # Validate image formats and process figure list
    supported_exts = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.tiff'}
    
    # Validate footer image
    if footer_image_path != "":
        footer_ext = os.path.splitext(footer_image_path)[1].lower()
        print(f"Footer image extension: {footer_ext}")
        footer_image_path_to_use = footer_image_path if footer_ext in supported_exts else ""
        if not footer_image_path_to_use:
            print(f"Skipping unsupported footer image format: {footer_image_path}")
    else:
        footer_image_path_to_use = ""
    
    # Process figure list paths
    figures_to_use = []
    if figure_list_paths:
        for figure_path in figure_list_paths:
            if figure_path and os.path.exists(figure_path):
                figure_ext = os.path.splitext(figure_path)[1].lower()
                if figure_ext in supported_exts:
                    figures_to_use.append(figure_path)
                    print(f"Added figure: {os.path.basename(figure_path)}")
                else:
                    print(f"Skipping unsupported figure format: {os.path.basename(figure_path)}")
            elif figure_path:
                print(f"Figure not found: {figure_path}")

    print(f"\nUsing footer image: {os.path.basename(footer_image_path_to_use) if footer_image_path_to_use else 'None'}")
    print(f"Total figures to include: {len(figures_to_use)}")
    if figures_to_use:
        print("Figure list:")
        for i, fig in enumerate(figures_to_use, 1):
            print(f"  {i}. {os.path.basename(fig)}")
    print()

    # Load CSV
    input_df = pd.read_csv(csv_path)

    # Test both methods of providing data structure
    
    # Method 1: Using datastructure_path (new approach)
    print("Testing Method 1: Using datastructure_path parameter...")
    output_filename_method1 = "test_codebook_with_images_method1"
    output_filename_path_method1 = os.path.join(output_folder, f"{output_filename_method1}.pdf")
    
    figures_param = figures_to_use if figures_to_use else None
    pdfcodebook_method1 = codebook(
        input_df=input_df,
        header_title='Regional Satisfaction Survey Codebook (Method 1)',
        datastructure_path=datastructure_path,  # New parameter
        projectoverview=projectoverview_path,
        keyterms=keyterms_path,
        output_filename=output_filename_method1,
        outputfolder=output_folder,
        figures=figures_param,
        footer_image_path=footer_image_path_to_use
    )
    pdfcodebook_method1.create_codebook()
    
    # Assert Method 1 output file was created
    assert os.path.exists(output_filename_path_method1)
    print(f"Method 1 completed: {output_filename_path_method1}")
    
    # Method 2: Loading datastructure manually (original approach)
    print("\nTesting Method 2: Using datastructure dictionary parameter...")
    
    # Load data structure dict from .py file manually
    spec = importlib.util.spec_from_file_location("pdfcb_00d_data_structure", datastructure_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {datastructure_path}")
    ds_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ds_module)
    datastructure = ds_module.DATA_STRUCTURE

    output_filename_method2 = "test_codebook_with_images_method2"
    output_filename_path_method2 = os.path.join(output_folder, f"{output_filename_method2}.pdf")

    pdfcodebook_method2 = codebook(
        input_df=input_df,
        header_title='Regional Satisfaction Survey Codebook (Method 2)',
        datastructure=datastructure,  # Original parameter
        projectoverview=projectoverview_path,
        keyterms=keyterms_path,
        output_filename=output_filename_method2,
        outputfolder=output_folder,
        figures=figures_param,
        footer_image_path=footer_image_path_to_use
    )
    pdfcodebook_method2.create_codebook()

    # Assert Method 2 output file was created
    assert os.path.exists(output_filename_path_method2)
    print(f"Method 2 completed: {output_filename_path_method2}")
    
    print("\nBoth methods completed successfully!")
