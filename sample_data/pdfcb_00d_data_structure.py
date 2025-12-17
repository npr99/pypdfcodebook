"""
Data Structure for Generic Survey Response Data

pyType = Python Type - needed to set correct data type in Python

"""

DATA_STRUCTURE = {
    'rid'  : 
    {   'label' : 'Random Survey Response ID', 
        'DataType'  : 'String',
        'pyType' : str,
        'AnalysisUnit' : 'Survey response',
        'MeasureUnit' : 'Responses',
        'notes' : '\n'.join([
            '1. Unique, non-missing key for sample data. \n \n'
            '2. Randomly generated 5 digit alphanumeric string identifier. \n \n'
            '3. Range from A1000 to Z9999.'
                ])},
    'region' : 
    {   'label' : 'Geographic Region',
        'DataType'  : 'Int',
        'pyType' : "category",
        'categorical' : True,
        'AnalysisUnit' : 'Survey response',
        'MeasureUnit' : 'Responses by Region',
        'categories_dict' : {
            1 : '1. North',
            2 : '2. South', 
            3 : '3. East',
            4 : '4. West'},
        'categories' : 
        [   '1. North',
            '2. South',
            '3. East', 
            '4. West'],
        'primary_key' : 'rid',
        'pop_var' : 'weight'},
    'satscore' : 
    {   'label' : 'Satisfaction Rating',
        'DataType'  : 'Int',
        'pyType' : "category",
        'categorical' : True,
        'AnalysisUnit' : 'Survey response',
        'MeasureUnit' : 'Satisfaction Level',
        'categories_dict' : {
            1 : '1. Very Dissatisfied',
            2 : '2. Dissatisfied',
            3 : '3. Neutral',
            4 : '4. Satisfied',
            5 : '5. Very Satisfied'},
        'categories' : 
        [   '1. Very Dissatisfied',
            '2. Dissatisfied',
            '3. Neutral',
            '4. Satisfied',
            '5. Very Satisfied'],
        'notes' : '\n'.join([
            '1. Five-point Likert scale measuring overall satisfaction. \n \n'
            '2. Missing values indicate participant did not respond to this question.'
                ]),
        'primary_key' : 'rid',
        'pop_var' : 'weight'},
    'weight' : 
    {   'label' : 'Survey Weight',
        'DataType'  : 'Float',
        'pyType' : float,
        'AnalysisUnit' : 'Survey response',
        'MeasureUnit' : 'Population',
        'notes' : '\n'.join([
            '1. Statistical weight for population inference and representative results. \n \n'
            '2. Used to adjust for sampling bias and ensure results reflect target population. \n \n'
            '3. Based on sample design for each region. \n \n'
            '4. Region 1 weight = 2.0, Region 2 weight = 1.0, Region 3 weight = 0.5, Region 4 weight = 2.0. \n \n'
            '5. Regions 1 and 4 are under sampled regions. Region 3 is over sampled.'
                ])},
    'age' : 
    {   'label' : 'Age in Years',
        'DataType'  : 'Int',
        'pyType' : int,
        'AnalysisUnit' : 'Survey response',
        'MeasureUnit' : 'Years',
        'notes' : '\n'.join([
            '1. Age of survey respondent at time of survey. \n \n'
            '2. Range from 18 to 99 years. \n \n'
            '3. Missing values indicate participant did not provide age information.'
            '4. Surveys completed between November 2025 and December 2025.'
                ]),
        'primary_key' : 'rid',
        'pop_var' : 'weight'},
}

# Add additional columns as needed following this structure.
