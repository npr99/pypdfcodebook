import pandas as pd
from pypdfcodebook.pdfcb_03c_codebook import codebook
import os

'''
Test making a codebook without keyterms or projectoverview files.
'''

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

    # Output folder
    output_folder = os.path.abspath("./tests/output")
    os.makedirs(output_folder, exist_ok=True)

    # Create codebook instance with no keyterms or projectoverview
    cb = codebook(
        input_df=df,
        header_title="Sample Codebook v2",
        datastructure=datastructure,
        projectoverview="",  # Not provided
        keyterms="",         # Not provided
        output_filename="test_codebook_v2",
        outputfolders={'top': output_folder}
    )
    cb.create_codebook()
    print("Codebook PDF generated at:", os.path.join(output_folder, "test_codebook_v2.pdf"))

if __name__ == "__main__":
    test_codebook_no_keyterms_projectoverview()
