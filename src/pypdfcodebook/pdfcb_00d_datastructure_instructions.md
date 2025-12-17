**Instructions for Data Structure File**

A data structure file defines the metadata and specifications for each variable in your dataset. This Python dictionary provides essential information that pypdfcodebook uses to create comprehensive variable documentation in your PDF codebook.

**Please create a DATA_STRUCTURE dictionary following this format:**

DATA_STRUCTURE = {
    'variable_name' : {
        Required fields for all variables:
        'label' : 'Human-readable variable description',
        'DataType' : 'String|Int|Float|Bool',  Data type as it appears in your data
        'pyType' : str|int|float|bool|"category",  Python type for processing
        'AnalysisUnit' : 'What each row represents (e.g., Survey response, Person, etc.)',
        'MeasureUnit' : 'Units of measurement (e.g., Years, Dollars, Responses, etc.)',
        
        Optional but recommended:
        'notes' : 'Additional context, methodology, or important details about this variable',
        
        Required for categorical variables:
        'categorical' : True,  Set to True if this is a categorical variable
        'categorical_type' : 'nominal|ordinal',  Type of categorical variable
        'categories_dict' : {
            1 : '1. First category label',
            2 : '2. Second category label',
            ... continue for all categories
        },
        'categories' : [
            '1. First category label',
            '2. Second category label',
            ... list matching the categories_dict
        ],
        
        Optional for weighted analysis:
        'primary_key' : 'variable_name_of_unique_identifier',
        'weight_var' : 'variable_name_of_weight_variable',
    },
    
    Add additional variables following the same structure...
}

**Example based on sample survey data:**

DATA_STRUCTURE = {
    'rid': {
        'label': 'Random Survey Response ID', 
        'DataType': 'String',
        'pyType': str,
        'AnalysisUnit': 'Survey response',
        'MeasureUnit': 'Responses',
        'notes': 'join([
            '1. Unique, non-missing key for sample data.',
            '2. Randomly generated 5 digit alphanumeric string identifier.',
            '3. Range from A1000 to Z9999.'
        ])
    },
    'region': {
        'label': 'Geographic Region',
        'DataType': 'Int',
        'pyType': "category",
        'categorical': True,
        'categorical_type': 'nominal',
        'AnalysisUnit': 'Survey response',
        'MeasureUnit': 'Responses by Region',
        'categories_dict': {
            1: '1. North',
            2: '2. South', 
            3: '3. East',
            4: '4. West'
        },
        'categories': [
            '1. North',
            '2. South',
            '3. East', 
            '4. West'
        ],
        'primary_key': 'rid',
        'weight_var': 'weight'
    },
    'age': {
        'label': 'Age in Years',
        'DataType': 'Int',
        'pyType': int,
        'AnalysisUnit': 'Survey response',
        'MeasureUnit': 'Years',
        'notes': 'join([
            '1. Age of survey respondent at time of survey.',
            '2. Range from 18 to 99 years.',
            '3. Missing values indicate participant did not provide age information.',
            '4. Surveys completed between November 2025 and December 2025.'
        ]),
        'primary_key': 'rid',
        'weight_var': 'weight'
    }
}

**Field Specifications**

**Required Fields (all variables):** **label** is a clear, descriptive name for the variable. **DataType** is the data type as stored ('String', 'Int', 'Float', 'Bool'). **pyType** is the Python type for processing (str, int, float, bool, or "category"). **AnalysisUnit** describes what each observation represents. **MeasureUnit** specifies units or scale of measurement.

**Categorical Variables:** Set **categorical** to True. Use **categorical_type** as 'nominal' for unordered categories, 'ordinal' for ordered categories. **categories_dict** should be a dictionary mapping numeric codes to labeled categories. **categories** should be a list of category labels matching the dictionary.

**Optional but Recommended:** **notes** provides additional context, methodology notes, or important details. **primary_key** names the unique identifier variable (for analysis). **weight_var** names the weight variable (for weighted analysis).

**Data Types Guide**

**'String'** is for text data (names, IDs, open responses). **'Int'** is for whole numbers (ages, counts, categorical codes). **'Float'** is for decimal numbers (weights, measurements, percentages). **'Bool'** is for True/False values. **pyType "category"** should be used for categorical variables regardless of underlying storage type.

**File Requirements**

**Save as Python file** using .py extension (e.g., data_structure.py). **Variable naming** must use the exact column names from your dataset. **Dictionary format** must be valid Python dictionary syntax. **Category consistency** requires that categories_dict and categories list match exactly.

**Notes Format**

For multi-line notes, use the join pattern: 'notes': 'join([ '1. First important point.', '2. Second important point.', '3. Additional context or methodology.' ])

**Creating Your Data Structure File**

Create a new Python file with .py extension. Define your DATA_STRUCTURE dictionary using the exact variable names from your dataset. For each variable, include all required fields and any relevant optional fields. For categorical variables, make sure to include the categorical-specific fields. Save the file in your project directory where pypdfcodebook can access it.

**Common Patterns**

For survey data, typically include a unique identifier (like rid), demographic variables (like age, region), response variables (like satisfaction scores), and any weight variables for analysis. For experimental data, include treatment indicators, outcome measures, and control variables. For observational data, include all measured variables with appropriate data types and units.

*This section was auto-generated using the default instruction mode in pypdfcodebook. To turn off instruction mode set instruction_mode to False in the codebook command. Please replace with your actual variable definitions.*