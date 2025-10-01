"""
******************************************************************************
* Project: pypdfcodebook                                                     *
* License: BSD 3-Clause License                                              *
* Author/Maintainer: Nathanael Rosenheim                                     *
* Copyright (c) 2025 Nathanael Rosenheim                                     *
******************************************************************************
"""

import pandas as pd
import numpy as np
import csv
import random
from datetime import datetime
from fpdf import FPDF, TextStyle, XPos, YPos
from typing import Dict, List, Union, Optional, Any

from pypdfcodebook.pdfcb_03b_pdffunctions import PDF


class codebook():
    """
    Functions to create a pdf codebook for data
    """ 
    def __init__(self,
            input_df: pd.DataFrame,
            header_title: str,
            datastructure: Dict[str, Dict[str, Any]],
            projectoverview: str,
            keyterms: str,
            output_filename: str,
            outputfolders: Dict[str, str] = {},
            seed: int = 15151,
            figures: Optional[Any] = None,
            footer_image_path: str = "") -> None:
        """
        Initialize a codebook generator for creating PDF documentation of datasets.
        
        This class creates comprehensive codebooks with data dictionaries, variable
        summaries, and statistical analyses. It processes pandas DataFrames and 
        generates professional PDF documentation with customizable formatting.
        
        Args:
            input_df (pd.DataFrame): The dataset to create a codebook for.
            header_title (str): Main title to appear in PDF headers.
            datastructure (Dict[str, Dict[str, Any]]): Metadata dictionary defining
                variable characteristics. Each key is a variable name, values are
                dictionaries with 'DataType', 'length', 'categorical', 'label',
                'AnalysisUnit', 'MeasureUnit' etc.
            projectoverview (str): Path to markdown file containing project description.
            keyterms (str): Path to markdown file containing key terms and definitions.
            output_filename (str): Base filename for generated PDF (without extension).
            outputfolders (Dict[str, str], optional): Directory paths for outputs.
                Defaults to {}.
            seed (int, optional): Random seed for reproducible example generation.
                Defaults to 15151.
            figures (Optional[Any], optional): Figure objects to include in codebook.
                Defaults to None.
            footer_image_path (str): Path to logo/image file to display in the PDF footer.
                An empty string means no footer image. Supported formats: PNG, JPG, JPEG, BMP, GIF, TIF, TIFF.
                The file must exist and be in a supported format, otherwise it will be ignored.
        
        Returns:
            None: This is a constructor method.
            
        Note:
            - The datastructure dict should follow a consistent schema for best results
            - File paths (projectoverview, keyterms, footer_image_path) should be absolute paths and exist
            - Image files must be in supported formats (PNG, JPG, JPEG, BMP, GIF, TIF, TIFF)
            - Community key must exist in communities dictionary
            - Random seed affects example generation in variable summaries
        """

        self.input_df = input_df
        self.header_title = header_title
        self.datastructure = datastructure
        self.projectoverview = projectoverview
        self.keyterms = keyterms
        self.output_filename = output_filename
        self.outputfolders = outputfolders
        self.seed = seed
        self.figures = figures
        self.footer_image_path = footer_image_path

    def render_toc(self, pdf: Any, outline: List[Any]) -> None:
        """
        Render a formatted table of contents in the PDF document with alternating row colors 
        and clickable links.

        Render TOC is a required input for the FPDF2 function insert_toc_placeholder.
        """
        pdf.ln()
        pdf.set_font("Helvetica", size=16)
        pdf.underline = True
        text = "Table of contents:"
        pdf.multi_cell(w=pdf.epw, h=pdf.font_size, text=text, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(pdf.font_size)
        pdf.underline = False
        pdf.set_font("Helvetica", size=12)
        pdf.set_fill_color(224, 235, 255)  # Light blue
        pdf.set_font("Helvetica", size=12)
        fill = False
        for section in outline:
            indent = " " * section.level * 2
            link = pdf.add_link()
            pdf.set_link(link, page=section.page_number)
            section_title = f"{indent}{section.name}"
            page_str = str(section.page_number)
            # Calculate available width for dots
            total_width = pdf.epw
            title_width = pdf.get_string_width(section_title)
            page_width = pdf.get_string_width(page_str)
            dot_width = pdf.get_string_width('.')
            # Padding between title and page number
            padding = 2 * pdf.get_string_width(' ')
            dots_width = total_width - title_width - page_width - padding
            n_dots = max(2, int(dots_width // dot_width))
            leader = '.' * n_dots
            toc_line = f"{section_title} {leader} {page_str}"
            pdf.cell(0, pdf.font_size * 2, text=toc_line, border=0, new_x="LMARGIN", new_y="NEXT", link=link)

    def add_projectoverview(self, pdf: Any) -> None:
        """
        Add a Project Overview section to the PDF document.

        A project overview is a summary that describes the purpose, scope, and key details
        of a project or dataset. It provides essential context for anyone using the data,
        helping them understand why the data was collected, what it represents, and how it
        should be interpreted. Including a project overview is important because it orients
        new users, supports transparency, and ensures that the data is used appropriately.

        This method reads a markdown file containing the project overview/summary
        and adds it as a formatted section to the codebook PDF. The content is rendered
        with markdown support, allowing for rich text formatting.

        The section includes:
        - A section header "Project Overview: Summary of Project Details"
        - Content from the projectoverview markdown file
        - Proper font formatting (Times 12pt)
        - Markdown rendering support
        - Automatic page break after the section

        Args:
            pdf (Any): The PDF object to add the project overview section to.
                Should be an instance of the PDF class with FPDF2 functionality
                including start_section(), multi_cell(), and markdown support.

        Returns:
            None: This method modifies the PDF document in-place.

        Raises:
            FileNotFoundError: If the projectoverview file path doesn't exist.
            UnicodeDecodeError: If the projectoverview file cannot be decoded as latin-1.

        Note:
            - The projectoverview file should be in markdown format for best results
            - Content is decoded using 'latin-1' encoding for broad compatibility
            - A new page is automatically added after the project overview section
            - The projectoverview file path is specified in self.projectoverview during initialization
        """
        pdf.start_section("Project Overview: Summary of Project Details")
        pdf.ln()

        try:
            with open(self.projectoverview, "rb") as fh:
                txt = fh.read().decode("latin-1")
        except FileNotFoundError:
            raise FileNotFoundError(f"Project overview file not found: {self.projectoverview}")
        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(
                e.encoding, e.object, e.start, e.end,
                f"Cannot decode project overview file as latin-1: {self.projectoverview}"
            )

        pdf.set_font("Times", size=12)
        line_height = pdf.font_size
        pdf.multi_cell(w=pdf.epw, h=line_height,
                       text=txt, new_x="LEFT", new_y="NEXT",
                       max_line_height=line_height*2,
                       align='L', markdown=True)

        pdf.add_page()

    def create_data_dictionary_table(self) -> pd.DataFrame:
        """
        Create a data dictionary table summarizing variables and their metadata.

        A data dictionary is a table or document that describes the structure, meaning,
        and attributes of each variable in a dataset. It explains what each variable
        represents, its data type, possible values, and any special notes. This is important
        because it helps anyone using the data understand what the variables mean, how to
        interpret them, and how to use the data correctly—reducing confusion and errors,
        especially for new users or collaborators.

        This method constructs a pandas DataFrame that lists all variables in the input
        dataset along with key metadata fields (Data Type, Length, Categorical, Label)
        if available in the datastructure dictionary. The resulting table is suitable
        for inclusion in a codebook or for further processing.

        Returns:
            pd.DataFrame: A table with columns for variable name and metadata fields.

        Note:
            - Only variables present in the input DataFrame are included.
            - If a metadata field is missing for a variable, it is filled with a blank string.
            - The output columns are: Variable Name, Data Type, Length, Categorical, Variable Label.
        """
        table_rows = []
        # Set up initial table of variables in data file
        for variable in self.input_df.columns:
            table_rows.append([variable])
        # Create base table
        table = pd.DataFrame(data=table_rows, columns=["variable name"])

        # Add variable details if in data structure
        for variable in self.input_df.columns:
            if variable in self.datastructure:
                for characteristic in ['DataType', 'length', 'categorical', 'label']:
                    if characteristic in self.datastructure[variable]:
                        char = self.datastructure[variable][characteristic]
                        table.loc[table["variable name"] == variable, characteristic] = char
                    else:
                        table.loc[table["variable name"] == variable, characteristic] = ' '

        # Rename columns for output
        table = table.rename(columns={
            'variable name': 'Variable Name',
            'DataType': 'Data Type',
            'length': 'Length',
            'categorical': 'Categorical',
            'label': 'Variable Label'
        })

        return table

    def add_datadictionary(self, pdf: Any) -> None:
        """
        Add a Data Dictionary section to the PDF document.

        The data dictionary provides a summary table of all variables in the dataset,
        including their names, data types, lengths, categorical status, and labels.
        This section is essential for users to understand the structure and content
        of the dataset, and is generated using the `create_data_dictionary_table` method.

        The section includes:
        - A section header "Data Dictionary: Summary of Variables"
        - A formatted table with variable metadata
        - Automatic page break after the section

        Args:
            pdf (Any): The PDF object to add the data dictionary section to.
                Should be an instance of the PDF class with FPDF2 functionality
                including start_section(), create_table(), and markdown support.

        Returns:
            None: This method modifies the PDF document in-place.

        Note:
            - The data dictionary table is generated from the current input DataFrame and datastructure.
            - The table columns are: Variable Name, Data Type, Length, Categorical, Variable Label.
            - A new page is automatically added after the data dictionary section.
        """
        table = self.create_data_dictionary_table()
        styled_table = table.copy()
        styled_table.reset_index(inplace=True)
        styled_table = styled_table.drop(columns=['index'])

        # Convert DataFrame directly to list of lists for PDF table
        table_data = [styled_table.columns.tolist()] + styled_table.values.tolist()
        pdf.start_section("Data Dictionary: Summary of Variables")
        pdf.ln()
        pdf.create_table(
            table_data=table_data,
            title='',
            align_data='L',
            align_header='C',
            line_space=1.75,
            cell_width=[30, 20, 14, 25, pdf.epw - (30 + 20 + 14 + 25)]
        )
        pdf.add_page()


    def add_keyterms(self, pdf: Any) -> None:
        """
        Add a Key Terms and Definitions section to the PDF document.
        
        Key terms provide essential definitions that ensure future data users
        do not have to assume what terms mean, promoting clear understanding
        and consistent interpretation of the dataset and its documentation.
        
        This method reads a markdown file containing key terms and definitions
        and adds it as a formatted section to the codebook. The content is 
        rendered with markdown support, allowing for rich text formatting
        including bold, italic, and other markdown features.
        
        The section includes:
        - A section header "Key Terms and Definitions"
        - Content from the keyterms markdown file
        - Proper font formatting (Times 12pt)
        - Markdown rendering support
        - Automatic page break after the section
        
        Args:
            pdf (Any): The PDF object to add the key terms section to.
                Should be an instance of the PDF class with FPDF2 functionality
                including start_section(), multi_cell(), and markdown support.
        
        Returns:
            None: This method modifies the PDF document in-place.
            
        Raises:
            FileNotFoundError: If the keyterms file path doesn't exist.
            UnicodeDecodeError: If the keyterms file cannot be decoded as latin-1.
            
        Note:
            - The keyterms file should be in markdown format for best results
            - Content is decoded using 'latin-1' encoding for broad compatibility
            - A new page is automatically added after the key terms section
            - The keyterms file path is specified in self.keyterms during initialization
        """
        # Add Key Terms and Definitions
        pdf.start_section("Key Terms and Definitions")
        pdf.ln()

        try:
            with open(self.keyterms, "rb") as fh:
                txt = fh.read().decode("latin-1")
        except FileNotFoundError:
            raise FileNotFoundError(f"Key terms file not found: {self.keyterms}")
        except UnicodeDecodeError as e:
            raise UnicodeDecodeError(
                e.encoding, e.object, e.start, e.end,
                f"Cannot decode key terms file as latin-1: {self.keyterms}"
            )
        
        pdf.set_font("Times", size=12)
        line_height = pdf.font_size
        pdf.multi_cell(w=pdf.epw, h = line_height,
                    text = txt,
                    new_x = XPos.LEFT,
                    new_y = YPos.NEXT,
                    max_line_height=line_height*2,
                    align='L', markdown=True)

        pdf.add_page()  

    def numeric_table(self, variable: str) -> pd.DataFrame:
        """
        Generate a summary table of descriptive statistics and metadata for a numeric variable.

        This function produces a table summarizing key characteristics of an integer or float variable,
        including counts, missing values, range, mean, median, standard deviation, and percentiles.
        It also includes relevant metadata from the datastructure, such as unit of measure and unit of analysis.

        Args:
            variable (str): The name of the numeric variable to summarize.

        Returns:
            pd.DataFrame: A table with two columns: 'Variable characteristic' and 'Variable details'.

        Note:
            - The variable must be present in both the input DataFrame and the datastructure.
            - If a metadata field is missing, it is filled with a blank string.
            - Percentiles reported: 10th, 25th, 50th, 75th, and 90th.
        """
        # Collect key characteristics of variable
        total_cases = len(self.input_df[variable])
        total_cases_fmt = "{:,.0f}".format(total_cases)
        valid_count = self.input_df[variable].describe()['count']
        valid_count_fmt = "{:,.0f}".format(valid_count)
        missing_count = self.input_df[variable].isna().sum()
        missing_count_fmt = "{:,.0f}".format(missing_count)

        descriptive_stats = {}
        for descriptive_stat in ['min', 'max', 'mean', '50%', 'std']:
            descriptive_stats[descriptive_stat] = "{:,.2f}".format(
                self.input_df[variable].describe()[descriptive_stat])

        # Add percentiles
        percentiles_values = self.input_df[variable].quantile([.1, .25, .5, .75, .9])
        descriptive_stats["10%"] = "{:,.2f}".format(percentiles_values[.1])
        descriptive_stats["25%"] = "{:,.2f}".format(percentiles_values[.25])
        descriptive_stats["50%"] = "{:,.2f}".format(percentiles_values[.5])
        descriptive_stats["75%"] = "{:,.2f}".format(percentiles_values[.75])
        descriptive_stats["90%"] = "{:,.2f}".format(percentiles_values[.9])

        # Add additional metadata to table
        characteristics = {}
        for characteristic in ['DataType', 'AnalysisUnit', 'MeasureUnit']:
            if characteristic in self.datastructure[variable]:
                metadata = self.datastructure[variable][characteristic]
                characteristics[characteristic] = metadata
            else:
                characteristics[characteristic] = ''

        table_data = np.array([
            ['variable type', 'numeric (' + characteristics['DataType'] + ')'],
            ['total cases', total_cases_fmt],
            ['valid cases', valid_count_fmt],
            ['missing cases', missing_count_fmt],
            ['unit of measure', characteristics['MeasureUnit']],
            ['unit of analysis', characteristics['AnalysisUnit']],
            ['range', 'minimum value: ' + descriptive_stats['min'] + ' to  maximum value: ' + descriptive_stats['max']],
            ['mean', descriptive_stats['mean']],
            ['median', descriptive_stats['50%']],
            ['standard deviation', descriptive_stats['std']],
            ['10th percentile', descriptive_stats['10%']],
            ['25th percentile', descriptive_stats['25%']],
            ['50th percentile', descriptive_stats['50%']],
            ['75th percentile', descriptive_stats['75%']],
            ['90th percentile', descriptive_stats['90%']]
        ])
        table = pd.DataFrame(data=table_data, columns=["Variable characteristic", "Variable details"])
        return table

    def string_table(self, variable: str, PDF_only: bool = True) -> pd.DataFrame:
        """
        Generate a summary table of descriptive statistics and metadata for a string (object) variable.

        This function produces a table summarizing key characteristics of a string or object variable,
        including counts, missing values, unique values, minimum and maximum string lengths, and random examples.
        It also includes relevant metadata from the datastructure, such as unit of measure and unit of analysis.

        Args:
            variable (str): The name of the string variable to summarize.
            PDF_only (bool, optional): If True, output is formatted for PDF inclusion. (Currently unused.)

        Returns:
            pd.DataFrame: A table with two columns: 'Variable characteristic' and 'Variable details'.

        Note:
            - The variable must be present in both the input DataFrame and the datastructure.
            - If a metadata field is missing, it is filled with a blank string.
            - Random examples are selected to reduce disclosure of identifiable data.
            - Minimum and maximum string lengths are based on the shortest and longest unique values.
        """
        # Ensure variable is treated as string for processing
        describe_var = self.input_df[variable].astype(str)

        # Collect key characteristics of variable
        total_cases = len(describe_var)
        total_cases_fmt = f"{total_cases:,}"
        valid_count = describe_var.describe()['count']
        valid_count_fmt = f"{valid_count:,}"
        missing_count = describe_var.loc[describe_var.isna()].count()
        missing_count_fmt = f"{missing_count:,}"
        unique_count = describe_var.describe()['unique']
        unique_count_fmt = f"{unique_count:,}"

        string_list = describe_var.astype(str)
        varid_list = list(string_list.fillna(value="0"))
        varid_min = min(varid_list)
        min_var_len = len(varid_min)
        varid_max = max(varid_list)
        max_var_len = len(varid_max)

        # Collect random examples of variable
        random.seed(self.seed)
        example_list = self.input_df[variable].unique().tolist()
        if len(example_list) >= 4:
            examples = random.sample(example_list, 4)
        else:
            # If fewer than 4 unique values, repeat as needed
            examples = (example_list * 4)[:4]
        example1, example2, example3, example4 = examples

        # Add additional metadata to table
        characteristics = {}
        for characteristic in ['DataType', 'AnalysisUnit', 'MeasureUnit']:
            if characteristic in self.datastructure[variable]:
                metadata = self.datastructure[variable][characteristic]
                characteristics[characteristic] = metadata
            else:
                characteristics[characteristic] = ''

        table_data = np.array([
            ['variable type', 'string'],
            ['total cases', total_cases_fmt],
            ['valid cases', valid_count_fmt],
            ['missing cases', missing_count_fmt],
            ['unit of measure', characteristics['MeasureUnit']],
            ['unit of analysis', characteristics['AnalysisUnit']],
            ['unique values', unique_count_fmt],
            ['minimum length', min_var_len],
            ['maximum length', max_var_len],
            ['example 1', example1],
            ['example 2', example2],
            ['example 3', example3],
            ['example 4', example4]
        ])
        table = pd.DataFrame(data=table_data, columns=["Variable characteristic", "Variable details"])
        return table

    def categorical_toptable(self, variable: str) -> pd.DataFrame:
        """
        Generate a summary table of descriptive statistics and metadata for a categorical variable.

        This function produces a table summarizing key characteristics of a categorical variable,
        including counts, missing values, and the range of values (min/max if numeric-like).
        It also includes relevant metadata from the datastructure, such as unit of measure and unit of analysis.

        Args:
            variable (str): The name of the categorical variable to summarize.

        Returns:
            pd.DataFrame: A table with two columns: 'Variable characteristic' and 'Variable details'.

        Note:
            - The variable must be present in both the input DataFrame and the datastructure.
            - If a metadata field is missing, it is filled with a blank string.
            - If the variable cannot be converted to float, min/max are reported as 'NA'.
        """
        # Collect key characteristics of variable
        total_cases = len(self.input_df[variable])
        total_cases_fmt = f"{total_cases:,}"
        valid_count = self.input_df[variable].describe()['count']
        valid_count_fmt = f"{valid_count:,}"
        missing_count = self.input_df[variable].isna().sum()
        missing_count_fmt = f"{missing_count:,}"

        descriptive_stats = {}
        for descriptive_stat in ['min', 'max']:
            try:
                # convert to float to avoid error
                float_var = self.input_df[variable].astype(float)
                descriptive_stats[descriptive_stat] = f"{float_var.describe()[descriptive_stat]:,.0f}"
            except Exception:
                descriptive_stats[descriptive_stat] = 'NA'

        # Add additional metadata to table
        characteristics = {}
        for characteristic in ['DataType', 'AnalysisUnit', 'MeasureUnit']:
            if characteristic in self.datastructure[variable]:
                metadata = self.datastructure[variable][characteristic]
                characteristics[characteristic] = metadata
            else:
                characteristics[characteristic] = ''

        table_data = np.array([
            ['variable type', f"categorical ({characteristics['DataType']})"],
            ['total cases', total_cases_fmt],
            ['valid cases', valid_count_fmt],
            ['missing cases', missing_count_fmt],
            ['unit of measure', characteristics['MeasureUnit']],
            ['unit of analysis', characteristics['AnalysisUnit']],
            ['range', f"minimum value: {descriptive_stats['min']} to  maximum value: {descriptive_stats['max']}"]
        ])
        table = pd.DataFrame(data=table_data, columns=["Variable characteristic", "Variable details"])
        return table

    def categorical_countfreq_table(self,
                                    variable,
                                    primary_key: str = 'huid',
                                    pop_var: str = ''):
        """
        Create table with count and frequency by 
        category for categorical variable with label

        primary_key = variable to group by for counts

        pop_var = variable to use to summarize population totals

        """
        output_df = self.input_df.copy()
        try:
            # Convert variable from categorical to numeric
            output_df[variable] = output_df[variable].astype(float)
        except:
            output_df[variable] = output_df[variable].astype(str)
        # Drop missing values
        output_df = output_df.dropna(subset=[variable])
        try:
            output_df[variable] = output_df[variable].astype(int)
        except:
            output_df[variable] = output_df[variable].astype(str)
        count_table = output_df[[primary_key,variable]].groupby(by=variable).count()
        count_table.reset_index(inplace=True)
        # Rename columns
        label_col = self.datastructure[primary_key]['MeasureUnit']
        count_table = count_table.rename(columns={primary_key:'Count of '+label_col,
                                    variable : 'Code'})

        # Add percent column
        count_table['Percent '+label_col] = \
            count_table['Count of '+label_col]/count_table['Count of '+label_col].sum()

        # Format columns
        count_table['Count of '+label_col] = \
            count_table['Count of '+label_col].apply(lambda x: "{:,}".format(x))
        count_table['Percent '+label_col] = \
            count_table['Percent '+label_col].apply(lambda x: "{:.2%}".format(x))

        # Generate table with all labels
        if 'categories_dict' in self.datastructure[variable].keys():
            categories_dict = \
            self.datastructure[variable]['categories_dict']
            categories_df = pd.DataFrame.from_dict(categories_dict, orient='index')
            categories_df.reset_index(inplace = True)
            # Rename columns
            categories_df = categories_df.rename(columns={'index':'Code',
                                        0 : 'Label'})
        elif 'categories_dict_v2' in self.datastructure[variable].keys():
            categories_dict = \
            self.datastructure[variable]['categories_dict_v2']
            categories_df = pd.DataFrame.from_dict(categories_dict, orient='index')
            categories_df.reset_index(inplace = True)
            # Rename columns
            categories_df = categories_df.rename(columns={'index':'Code'})            
        else:
            # If no categories dictionary exists, create empty dataframe with just codes
            unique_codes = count_table['Code'].unique()
            categories_df = pd.DataFrame({'Code': unique_codes, 'Label': unique_codes})

        # Merge count and categories tables
        categorical_table = \
            categories_df.merge(count_table, on='Code', how='outer')

        # Fill in missing values
        categorical_table['Count of '+label_col] = \
            categorical_table['Count of '+label_col].fillna(value='0')
        categorical_table['Percent '+label_col] = \
            categorical_table['Percent '+label_col].fillna(value='0.00%')

        # Add population totals
        if pop_var != '':
            label_col = self.datastructure[pop_var]['MeasureUnit']
            pop_table = output_df[[pop_var,variable]].groupby(by=variable).sum()
            pop_table.reset_index(inplace=True)
            # Rename columns
            pop_table = pop_table.rename(columns={pop_var:'Sum of '+label_col,
                                        variable : 'Code'})

            # Add percent column
            pop_table['Percent '+label_col] = \
                pop_table['Sum of '+label_col]/pop_table['Sum of '+label_col].sum()

            # Format columns
            pop_table['Sum of '+label_col] = \
                pop_table['Sum of '+label_col].apply(lambda x: "{:,}".format(x))
            pop_table['Percent '+label_col]  = \
                pop_table['Percent '+label_col] .apply(lambda x: "{:.2%}".format(x))

            # Merge count and categories tables
            categorical_table = \
                categorical_table.merge(pop_table, on='Code', how='outer')

            # Fill in missing values
            categorical_table['Sum of '+label_col] = \
                categorical_table['Sum of '+label_col].fillna(value='0')
            categorical_table['Percent '+label_col] = \
                categorical_table['Percent '+label_col].fillna(value='0.00%')

        return categorical_table

    def add_var_summary(self, pdf: Any) -> None:
        """
        Add a Variable Details and Notes section to the PDF document.

        This method iterates through all variables in the datastructure and generates a detailed summary
        for each, including descriptive statistics, metadata, and notes. It automatically determines the
        appropriate summary table (numeric, string, or categorical) based on the variable's data type and
        pyType. For categorical variables, it also includes a table of category codes, labels, and frequencies.
        Any notes associated with a variable are appended after its summary table.

        The section includes:
        - A section header "Variable Details and Notes"
        - A summary table for each variable
        - Categorical code/frequency tables where applicable
        - Notes for each variable if present
        - Automatic page break after each variable

        Args:
            pdf (Any): The PDF object to add the variable summaries to.
                Should be an instance of the PDF class with FPDF2 functionality
                including start_section(), create_table(), multi_cell(), etc.

        Returns:
            None: This method modifies the PDF document in-place.

        Note:
            - Variable type and summary logic is determined by 'DataType' and 'pyType' in the datastructure.
            - Categorical variables include a frequency table of codes and labels.
            - Notes are included if present in the datastructure for a variable.
            - Each variable's details start on a new page for clarity.
        """
        pdf.start_section("Variable Details and Notes")
        pdf.ln()
        pdf.set_font("helvetica", size=12)
        text = (
            "The following pages provide details on each variable. "
            "Where applicable, notes provide links to verify data. "
            "Categorical variables include details on category codes."
        )
        pdf.multi_cell(w=pdf.epw, h=pdf.font_size*2, text=text, new_x="LEFT", new_y="NEXT")
        pdf.ln()
        pdf.add_page()
        for variable in self.datastructure.keys():
            print(variable)
            dtype = self.datastructure[variable].get('DataType', '')
            pytype = self.datastructure[variable].get('pyType', '')
            if dtype == 'String' and pytype != 'category':
                table = self.string_table(variable)
            elif dtype == 'String' and pytype == 'category':
                table = self.categorical_toptable(variable)
            elif dtype in ['Float', 'Int'] and pytype != 'category':
                table = self.numeric_table(variable)
            elif dtype in ['Float', 'Int'] and pytype == 'category':
                table = self.categorical_toptable(variable)
            else:
                continue
            styled_table = table.copy()
            styled_table.reset_index(inplace=True)
            styled_table = styled_table.drop(columns=['index'])

            # Convert DataFrame directly to list of lists for PDF table
            table_data = [styled_table.columns.tolist()] + styled_table.values.tolist()
            title = f"{variable}: {self.datastructure[variable].get('label', '')}"
            pdf.create_table(
                table_data=table_data,
                title=title,
                data_size=10,
                title_size=12,
                align_data='R',
                align_header='C',
                cell_width='split-20-80',
                line_space=1.75
            )

            # Add table of categories for categorical variables
            if pytype == 'category':
                pdf.ln()
                pop_var = self.datastructure[variable].get('pop_var', '')
                table = self.categorical_countfreq_table(
                    variable=variable,
                    primary_key=self.datastructure[variable]['primary_key'],
                    pop_var=pop_var
                )
                styled_table = table.copy()
                styled_table.reset_index(inplace=True)
                styled_table = styled_table.drop(columns=['index'])

                # Convert DataFrame directly to list of lists for PDF table
                table_data = [styled_table.columns.tolist()] + styled_table.values.tolist()
                title = (
                    f"{variable}: {self.datastructure[variable].get('label', '')} - "
                    "Categorical codes, labels and frequencies"
                )
                ncols = len(table_data[0])
                print(ncols)
                if ncols == 6:
                    cell_widths = [12, pdf.epw - (12 + 24 + 24 + 18 + 18), 24, 24, 18, 18]
                elif ncols == 5:
                    cell_widths = [12, pdf.epw - (12 + 24 + 24 + 30), 30, 24, 24]
                elif ncols == 4:
                    cell_widths = [12, pdf.epw - (12 + 24 + 24), 24, 24]
                else:
                    cell_widths = 'even'
                pdf.create_table(
                    table_data=table_data,
                    title=title,
                    data_size=10,
                    title_size=12,
                    align_data='R',
                    align_header='C',
                    cell_width=cell_widths,
                    line_space=1.75
                )
            # Add notes if present
            if 'notes' in self.datastructure[variable]:
                notes = self.datastructure[variable]['notes']
                pdf.cell(w=0, h=10, text=f"Variable Notes: {variable}", border=0, new_x="LMARGIN", new_y="NEXT")
                pdf.multi_cell(0, 3, text=notes, new_x="RIGHT", new_y="TOP", align='L', max_line_height=pdf.font_size*2)
                pdf.ln()

            pdf.add_page()



    def create_codebook(self) -> None:
        """
        Generate a complete PDF codebook for the dataset, including all metadata sections.

        This method orchestrates the creation of a comprehensive codebook PDF, including:
        - Table of contents
        - Project overview
        - Data dictionary
        - Variable details and notes (with summary tables)
        - Key terms and definitions
        - Custom footer with filename and generation timestamp

        The PDF is formatted with section headings, page breaks, and optional logo/image in the footer.
        All content is generated from the input DataFrame and datastructure provided at initialization.

        Returns:
            None: The generated PDF is saved to the output folder specified in initialization.

        Note:
            - The output file is saved as <outputfolders['top']>/<output_filename>.pdf
            - If figures are provided, they must be added by the user after PDF creation.
            - All section content is generated in sequence for clarity and reproducibility.
        """
        header_text = self.header_title
        print(f"Creating codebook: {header_text}")

        # Generate timestamp for footer reproducibility
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        pdf = PDF(
            header_text=header_text,
            footer_text=f"{self.output_filename} | Generated: {timestamp}",
            footer_image_path=self.footer_image_path
        )

        pdf.set_margins(left=15, top=10)
        pdf.alias_nb_pages()
        # Set styles for section headings
        pdf.set_section_title_styles(
            # Level 0 titles:
            TextStyle(
                font_family="helvetica",
                font_style="B",
                font_size_pt=14,
                color=(0, 0, 0),
                underline=True,
                t_margin=0,
                l_margin=10,
                b_margin=0,
            ),
            # Level 1 subtitles:
            TextStyle(
                font_family="helvetica",
                font_style="B",
                font_size_pt=12,
                color=(0, 0, 0),
                underline=True,
                t_margin=0,
                l_margin=20,
                b_margin=5,
            ),
        )
        pdf.add_page()

        # Add Table of Contents
        pdf.insert_toc_placeholder(self.render_toc, pages=1)
        pdf.add_page()

        # Add Project Overview
        if self.projectoverview != '':
            self.add_projectoverview(pdf)

        # Add Data Dictionary
        self.add_datadictionary(pdf)

        # Add Variable Details and Notes
        self.add_var_summary(pdf)

        # If user provides figures, they must handle figure addition themselves.
        # This codebook does not generate or add figures automatically.

        # Add Key Terms and Definitions
        if self.keyterms != '':
            pdf.add_page()
            self.add_keyterms(pdf)

        # Save codebook
        codebook_filepath = self.outputfolders['top'] + "/" + self.output_filename + '.pdf'
        print("Saving codebook to", codebook_filepath)
        pdf.output(codebook_filepath)
