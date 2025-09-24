import os
import pandas as pd
import importlib.util
from src.pypdfcodebook.pdfcb_03c_codebook import codebook

def test_codebook_with_sample_data(tmp_path):
    # Paths to sample files
    sample_dir = os.path.join(os.path.dirname(__file__), '..', 'sample_data')
    projectoverview_path = os.path.join(sample_dir, 'pdfcb_00a_projectoverview.md')
    keyterms_path = os.path.join(sample_dir,        'pdfcb_00b_keyterms.md')
    csv_path = os.path.join(sample_dir,             'pdfcb_00c_sampledata.csv')
    datastructure_path = os.path.join(sample_dir,   'pdfcb_00d_data_structure.py')

    # Load CSV
    input_df = pd.read_csv(csv_path)

    # Load data structure dict from .py file
    spec = importlib.util.spec_from_file_location("pdfcb_00d_data_structure", datastructure_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {datastructure_path}")
    ds_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ds_module)
    datastructure = ds_module.DATA_STRUCTURE

    # Set up output in tests directory
    tests_dir = os.path.dirname(__file__)
    output_filename_path = os.path.join(tests_dir, "test_codebook.pdf")
    output_filename = "test_codebook"  # Just the name without extension
    outputfolders = {'top': tests_dir}

    # Provide valid test values for communities and community
    communities = {'test_comm': {'community_name': 'Test Community'}}
    community = 'test_comm'
    # Create codebook
    pdfcodebook = codebook(
        input_df=input_df,
        header_title='Housing Unit Inventory',
        datastructure=datastructure,
        projectoverview=projectoverview_path,
        keyterms=keyterms_path,
        output_filename=output_filename,
        outputfolders=outputfolders,
        figures=None,      # or your test value
        image_path=""      # empty string instead of None to avoid file error
    )
    pdfcodebook.create_codebook()

    # Assert output file was created
    assert os.path.exists(output_filename_path)
