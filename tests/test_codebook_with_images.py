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
    banner_path = os.path.join(sample_dir, 'IN-CORE_HRRC_Banner.png')
    figure_path = os.path.join(sample_dir, 'pdfcb_00e_sampleimage.jpg')

    # Check if paths exist, else set to empty string
    projectoverview_path = projectoverview_path if os.path.exists(projectoverview_path) else ""
    keyterms_path = keyterms_path if os.path.exists(keyterms_path) else ""
    csv_path = csv_path if os.path.exists(csv_path) else ""
    datastructure_path = datastructure_path if os.path.exists(datastructure_path) else ""
    banner_path = banner_path if os.path.exists(banner_path) else None
    figure_path = figure_path if os.path.exists(figure_path) else None

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
    output_filename_path = os.path.join(tests_dir, "test_codebook_with_images.pdf")
    output_filename = "test_codebook_with_images"
    outputfolders = {'top': tests_dir}

    # Check image formats before PDF creation
    supported_exts = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.tiff'}
    if banner_path is not None:
        banner_ext = os.path.splitext(banner_path)[1].lower()
        banner_to_use = banner_path if banner_ext in supported_exts else None
        if banner_to_use is None:
            print(f"Skipping unsupported banner image format: {banner_path}")
    else:
        banner_to_use = None
    if figure_path is not None:
        figure_ext = os.path.splitext(figure_path)[1].lower()
        figure_to_use = figure_path if figure_ext in supported_exts else None
        if figure_to_use is None:
            print(f"Skipping unsupported figure image format: {figure_path}")
    else:
        figure_to_use = None

    # Pass figures as a list if valid, else None
    figures_param = [figure_to_use] if figure_to_use else None
    pdfcodebook = codebook(
        input_df=input_df,
        header_title='Housing Unit Inventory',
        datastructure=datastructure,
        projectoverview=projectoverview_path,
        keyterms=keyterms_path,
        output_filename=output_filename,
        outputfolders=outputfolders,
        figures=figures_param,
        image_path=banner_to_use
    )
    pdfcodebook.create_codebook()

    # Assert output file was created
    assert os.path.exists(output_filename_path)
