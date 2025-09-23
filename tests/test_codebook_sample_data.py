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
    ds_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ds_module)
    datastructure = ds_module.DATA_STRUCTURE

    # Set up output
    output_filename = tmp_path / "test_codebook.pdf"
    outputfolders = [str(tmp_path)]

    # Create codebook
    pdfcodebook = codebook(
        input_df=input_df,
        header_title='Housing Unit Inventory',
        datastructure=datastructure,
        projectoverview=projectoverview_path,
        keyterms=keyterms_path,
        communities=None,  # or your test value
        community=None,    # or your test value
        year=2020,
        output_filename=str(output_filename),
        outputfolders=outputfolders,
        figures=None,      # or your test value
        image_path=None    # or your test value
    )
    pdfcodebook.create_codebook()

    # Assert output file was created
    assert output_filename.exists()
