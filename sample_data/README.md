# Sample Data and Templates for pypdfcodebook

This folder contains example files to help users understand the required and optional inputs for generating a codebook.

## Files

- `pdfcb_00a_projectoverview.md`  
  Example project overview markdown file. Place at the front of the codebook for context and citation.

- `pdfcb_00b_keyterms.md`  
  Example key terms markdown file. Use to define important terms for your dataset.

- `pdfcb_00c_sampledata.csv`  
  Example CSV data file with columns matching the expected input format.

- `pdfcb_00d_data_structure.py`  
  Python dictionary template describing the structure and metadata for each column in the CSV. Users should adapt this for their own data.

## How to Use

1. **Required:**
   - Provide a CSV data file with your data.
   - Create a data structure dictionary (see `pdfcb_00d_data_structure.py`) describing each column.

2. **Optional:**
   - Add a project overview markdown file for context.
   - Add a key terms markdown file for definitions.
   - (Optional) Add figures or banner images as needed for your codebook.

See each file for more details and adapt as needed for your project.
