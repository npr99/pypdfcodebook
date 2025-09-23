"""
Data Structure for Housing Unit Allocation

pyType = Python Type - needed to set correct data type in Python

"""

DATA_STRUCTURE = {
    'huid'  : 
    {   'label' : 'Housing Unit ID', 
        'DataType'  : 'String',
        'pyType' : str,
        'AnalysisUnit' : 'Housing unit',
        'MeasureUnit' : 'Housing units',
        'notes' : '\n'.join([
            '1. Primary Key for sample data. '
                ])},
    'blockid' : 
    {   'label' : 'Block ID' , 
        'huiv3-0-0' : 'Block2010',
        'formula' : "\n".join([
                        "output_df['blockid']."
                        "apply(lambda x :"
                        "str(int(x)).zfill(15))"]),
        'DataType'  : 'String',
        'pyType' : str,
        'AnalysisUnit' : 'Geographic unit',
        'MeasureUnit' : 'Housing unit in census block',
        'length' : 15,
        'zero_padded' : True,
        'notes' :
            '1. 2010 Census Block ID'},
    'numprec' : 
    {   'label' : 'Number of Person Records',
        'DataType'  : 'Int',
        'pyType' : int,
        'AnalysisUnit' : 'Housing unit',
        'MeasureUnit' : 'Persons'},
    'ownershp' : 
    {   'label' : 'Tenure Status',
        'DataType'  : 'Int',
        'pyType' : "category",
        'categorical' : True,
        'AnalysisUnit' : 'Household',
        'MeasureUnit' : 'Housing unit',
        'categories_dict' : {
            1 : '1. Owned or being bought (loan)',
            2 : '2. Rented'},
        'categories' : 
        [   '1. Owned or being bought (loan)',
            '2. Rented'],
        'notes' : '\n'.join([
            '1. Based on 2010 Census SF1 Table H16. \n \n'
            '2. Tenure status is not applicable for vacant not occupied housing units. \n \n'
            '3. Tenure status is not applicable for group quarters. \n \n'
            '4. To verify results compare table to: \n \n'
            'https://data.census.gov/cedsci/table?g=0500000US{state_county}&tid=DECENNIALSF12010.H16.'
                ]),
        'primary_key' : 'huid',
        'pop_var' : 'numprec'},
}

# Add additional columns as needed following this structure.
