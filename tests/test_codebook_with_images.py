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
    svg_path = os.path.join(sample_dir, 'hhracedotmap_2010_Seaside_OR_NSI_2_NSI.svg')

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

    # Create codebook with banner image
    pdfcodebook = codebook(
        input_df=input_df,
        header_title='Housing Unit Inventory',
        datastructure=datastructure,
        projectoverview=projectoverview_path,
        keyterms=keyterms_path,
        output_filename=output_filename,
        outputfolders=outputfolders,
        figures=None,
        image_path=banner_path
    )
    pdfcodebook.create_codebook()

    # Add image as a figure to the PDF (after codebook creation) only if supported format
    from fpdf import FPDF
    supported_exts = {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.tiff'}
    image_ext = os.path.splitext(svg_path)[1].lower()
    pdf = FPDF()
    pdf.add_page()
    if image_ext in supported_exts:
        pdf.image(svg_path, x=10, y=30, w=pdf.epw)
    else:
        print(f"Skipping unsupported image format: {svg_path}")
    image_pdf_path = os.path.join(tests_dir, 'test_codebook_with_images_fig.pdf')
    pdf.output(image_pdf_path)

    # Assert output file was created
    assert os.path.exists(output_filename_path)
