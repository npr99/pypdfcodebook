import pandas as pd
import numpy as np
import csv
import random
from fpdf import FPDF, TextStyle
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
            image_path: str = "") -> None:
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
            image_path (str, optional): Path to logo/image file for PDF footer.
                Defaults to "".
        
        Returns:
            None: This is a constructor method.
            
        Note:
            - The datastructure dict should follow a consistent schema for best results
            - File paths (projectoverview, keyterms, image_path) should be absolute paths
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
        self.image_path = image_path

    def render_toc(self, pdf, outline):
        pdf.ln()
        pdf.set_font("Helvetica", size=16)
        pdf.underline = True
        text = "Table of contents:"
        pdf.multi_cell(w=pdf.epw, h=pdf.font_size, txt=text, ln=1)
        pdf.ln(pdf.font_size) # move cursor back to the left margin
        pdf.underline = False
        pdf.set_font("Helvetica", size=12)
        pdf.set_fill_color(224, 235, 255)
        fill = True
        for section in outline:
            link = pdf.add_link()
            pdf.set_link(link, page=section.page_number)
            text = f'{" " * section.level * 2} {section.name}'
            pdf.multi_cell(w=int(pdf.epw * 0.8), h=pdf.font_size*2, txt=text, 
                    ln=3, align="L", link=link,fill = fill)
            text = f'{section.page_number}'
            pdf.multi_cell(w=int(pdf.epw * 0.2), h=pdf.font_size*2, txt=text, 
                    ln=3, align="R", link=link, fill = fill)
            fill = not fill
            pdf.ln()


    def add_keyterms(self,pdf):
        # Add Key Terms and Definitions
        pdf.start_section("Key Terms and Definitions")
        pdf.ln()

        with open(self.keyterms, "rb") as fh:
            txt = fh.read().decode("latin-1")
        pdf.set_font("Times", size=12)
        line_height = pdf.font_size
        pdf.multi_cell(w=pdf.epw, h = line_height,
                    txt = txt, ln = 2, 
                    max_line_height=line_height*2,
                    align='L', markdown=True)

        pdf.add_page()  

    def add_projectoverview(self,pdf):
        # Add Key Terms and Definitions
        pdf.start_section("Project Overview: Summary of Project Details")
        pdf.ln()

        with open(self.projectoverview, "rb") as fh:
            txt = fh.read().decode("latin-1")
        pdf.set_font("Times", size=12)
        line_height = pdf.font_size
        pdf.multi_cell(w=pdf.epw, h = line_height,
                    txt = txt, ln = 2, 
                    max_line_height=line_height*2,
                    align='L', markdown=True)

        pdf.add_page() 


    def create_data_dictionary_table(self):
        table_rows = []
        # Set up initial table of variables in data file
        for variable in self.input_df.columns:
            table_rows.append([variable])
        # Create base table
        table = pd.DataFrame(data = table_rows,columns=["variable name"])

        # Add variable details if in data structure
        for variable in self.input_df.columns:
            if variable in self.datastructure:
                for characteristic in ['DataType','length','categorical','label']:
                    if characteristic in self.datastructure[variable]:
                        char = self.datastructure[variable][characteristic]
                        table.loc[table["variable name"] == variable, 
                                        characteristic] = char
                    elif characteristic not in self.datastructure[variable]:
                        table.loc[table["variable name"] == variable, 
                                        characteristic] = ' '
                        
        # rename columns
        table = table.rename(columns = {'variable name':'Variable Name',
                                        'DataType':'Data Type',
                                        'length':'Length',  
                                        'categorical':'Categorical',
                                        'label':'Variable Label'})
                                                
        return table

    def add_datadictionary(self, pdf):
        # Add Data Dictionary - Variable Summary
        table = self.create_data_dictionary_table()
        styled_table = table.copy()
        styled_table.reset_index(inplace = True)
        styled_table = styled_table.drop(columns = ['index'])
        
        # Convert DataFrame directly to list of lists for PDF table
        table_data = [styled_table.columns.tolist()] + styled_table.values.tolist()
        pdf.start_section("Data Dictionary: Summary of Variables")
        pdf.ln()
        pdf.create_table(table_data = table_data,title='', 
            align_data = 'L', align_header = 'C', 
            line_space = 1.75, cell_width = [30,20,14,25,pdf.epw-(30+20+14+25)])
        pdf.add_page()

    def numeric_table(self,variable):
        """
        Function produces a integer variable details a integer variable

        """    

        # Collect key characteristics of variable
        total_cases = len(self.input_df[variable])
        total_cases_fmt = "{:,.0f}".format(total_cases)
        valid_count = self.input_df[variable].describe()['count']
        valid_count_fmt = "{:,.0f}".format(valid_count)
        missing_count = self.input_df[variable].isna().sum()
        missing_count_fmt = "{:,.0f}".format(missing_count)

        descriptive_stats = {}
        for descriptive_stat in ['min','max','mean','50%','std']:
            descriptive_stats[descriptive_stat] = "{:,.2f}".format(
                self.input_df[variable].describe()[descriptive_stat])

        # Add percentiles
        percentiles_values = self.input_df[variable].quantile([.1,.25,.5,.75,.9])
        descriptive_stats["10%"] = "{:,.2f}".format(percentiles_values[.1])
        descriptive_stats["25%"] = "{:,.2f}".format(percentiles_values[.25])
        descriptive_stats["50%"] = "{:,.2f}".format(percentiles_values[.5])
        descriptive_stats["75%"] = "{:,.2f}".format(percentiles_values[.75])
        descriptive_stats["90%"] = "{:,.2f}".format(percentiles_values[.9])


        # Add additional metadata to table
        characteristics = {}
        for characteristic in ['DataType','AnalysisUnit','MeasureUnit']:
            if characteristic in self.datastructure[variable]:
                metadata = self.datastructure[variable][characteristic]
                characteristics[characteristic] = metadata
            elif characteristic not in self.datastructure[variable]:
                characteristics[characteristic] = ''


        table_data = np.array([['variable type','numeric ('+\
                        characteristics['DataType']+')'],
                       ['total cases',total_cases_fmt],
                       ['valid cases',valid_count_fmt],
                       ['missing cases',missing_count_fmt],
                       ['unit of measure',characteristics['MeasureUnit']],
                       ['unit of analysis',characteristics['AnalysisUnit']],
                       ['range','minimum value: '+descriptive_stats['min']+\
                           ' to  maximum value: '+descriptive_stats['max']],
                       ['mean',descriptive_stats['mean']], 
                       ['median',descriptive_stats['50%']],
                       ['standard deviation',descriptive_stats['std']],
                       ['10th percentile',descriptive_stats['10%']],
                       ['25th percentile',descriptive_stats['25%']],
                       ['50th percentile',descriptive_stats['50%']],
                       ['75th percentile',descriptive_stats['75%']],
                       ['90th percentile',descriptive_stats['90%']]])
        table = pd.DataFrame(data=table_data, 
                        columns=["Variable characteristic", "Variable details"])

        return table

    def string_table(self,variable, PDF_only = True):
        """
        Function produces a string variable details a string/object variable
        """    

        # Check if variable is a string - if not, convert to string for processing
        if self.input_df[variable].dtype == 'object':
            describe_var = self.input_df[variable].astype(str)
        else:
            # For non-string variables, convert to string for processing
            describe_var = self.input_df[variable].astype(str)
        # Collect key characteristics of variable
        total_cases = len(describe_var)
        total_cases_fmt = "{:,}".format(total_cases)
        valid_count = describe_var.describe()['count']
        valid_count_fmt = "{:,}".format(valid_count)
        missing_count = describe_var.loc[describe_var.isna()].count()
        missing_count_fmt = "{:,}".format(missing_count)
        unique_count = describe_var.describe()['unique']
        unique_count_fmt = "{:,}".format(unique_count)

        string_list = describe_var.astype(str)
        varid_list = list(string_list.fillna(value="0"))
        varid_min = min(varid_list)       
        min_var_len = len(varid_min)
        varid_max = max(varid_list)       
        max_var_len = len(varid_max)

        # Collect Random examples of variable
        # Random examples help reduce disclosure of identifiable data
        random.seed(self.seed)
        example_list = self.input_df[variable].unique().tolist()
        example1 = example_list[random.randint(0, len(example_list)-1)]
        example2 = example_list[random.randint(0, len(example_list)-1)]
        example3 = example_list[random.randint(0, len(example_list)-1)]
        example4 = example_list[random.randint(0, len(example_list)-1)]

        # Add additional metadata to table
        characteristics = {}
        for characteristic in ['DataType','AnalysisUnit','MeasureUnit']:
            if characteristic in self.datastructure[variable]:
                metadata = self.datastructure[variable][characteristic]
                characteristics[characteristic] = metadata
            elif characteristic not in self.datastructure[variable]:
                characteristics[characteristic] = ''


        table_data = np.array([['variable type','string'],
                       ['total cases',total_cases_fmt],
                       ['valid cases',valid_count_fmt],
                       ['missing cases',missing_count_fmt],
                       ['unit of measure',characteristics['MeasureUnit']],
                       ['unit of analysis',characteristics['AnalysisUnit']],
                       ['unique values',unique_count_fmt],
                       ['minimum length', min_var_len], 
                       ['maximum length', max_var_len],
                       ['example 1',example1],
                       ['example 2',example2],
                       ['example 3',example3],
                       ['example 4',example4]])
        table = pd.DataFrame(data=table_data, 
                        columns=["Variable characteristic", "Variable details"])


        return table

    def categorical_toptable(self,variable):
        """
        Function produces categorical variable characteristics
        for the characteristics
        """    

        # Collect key characteristics of variable
        total_cases = len(self.input_df[variable])
        total_cases_fmt = "{:,.0f}".format(total_cases)
        valid_count = self.input_df[variable].describe()['count']
        valid_count_fmt = "{:,.0f}".format(valid_count)
        missing_count = self.input_df[variable].isna().sum()
        missing_count_fmt = "{:,.0f}".format(missing_count)

        descriptive_stats = {}
        for descriptive_stat in ['min','max']:
            try:
                # convert to float to avoid error
                float_var = self.input_df[variable].astype(float)
                descriptive_stats[descriptive_stat] = "{:,.0f}".format(
                    float_var.describe()[descriptive_stat])
            except:
                descriptive_stats[descriptive_stat] = 'NA'

        # Add additional metadata to table
        characteristics = {}
        for characteristic in ['DataType','AnalysisUnit','MeasureUnit']:
            if characteristic in self.datastructure[variable]:
                metadata = self.datastructure[variable][characteristic]
                characteristics[characteristic] = metadata
            elif characteristic not in self.datastructure[variable]:
                characteristics[characteristic] = ''


        table_data = np.array([['variable type','categorical ('+\
                        characteristics['DataType']+')'],
                       ['total cases',total_cases_fmt],
                       ['valid cases',valid_count_fmt],
                       ['missing cases',missing_count_fmt],
                       ['unit of measure',characteristics['MeasureUnit']],
                       ['unit of analysis',characteristics['AnalysisUnit']],
                       ['range','minimum value: '+descriptive_stats['min']+\
                           ' to  maximum value: '+descriptive_stats['max']]])        
        
        table = pd.DataFrame(data=table_data, 
            columns=["Variable characteristic", "Variable details"])


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

    def add_var_summary(self,pdf):
        # Summary of Variables
        pdf.start_section("Variable Details and Notes")
        pdf.ln()
        pdf.set_font("helvetica", size=12)
        text = "The following pages provide details on each variable. "
        text += "Where applicable notes provide links to verify data. "
        text += "Categorical variables include datails on category codes."
        pdf.multi_cell(w = pdf.epw, h= pdf.font_size*2, txt=text, ln = 2)
        pdf.ln()
        pdf.add_page()        
        for variable in self.datastructure.keys():
            print(variable)
            if self.datastructure[variable]['DataType'] == 'String' and \
                self.datastructure[variable]['pyType'] != 'category':
                table = self.string_table(variable)
            elif self.datastructure[variable]['DataType'] == 'String' and \
                self.datastructure[variable]['pyType'] == 'category':
                table = self.categorical_toptable(variable)
            elif self.datastructure[variable]['DataType'] in ['Float','Int'] and \
                self.datastructure[variable]['pyType'] != 'category':
                table = self.numeric_table(variable)
            elif self.datastructure[variable]['DataType'] in ['Float','Int'] and \
                self.datastructure[variable]['pyType'] == 'category':
                table = self.categorical_toptable(variable)
            else:
                continue
            styled_table = table.copy()
            styled_table.reset_index(inplace = True)
            styled_table = styled_table.drop(columns = ['index'])
            
            # Convert DataFrame directly to list of lists for PDF table
            table_data = [styled_table.columns.tolist()] + styled_table.values.tolist()
            title = variable+': '+self.datastructure[variable]['label'] 
            pdf.create_table(table_data = table_data, title=title, 
                data_size= 10, title_size = 12,
                align_data = 'R', align_header = 'C', 
                cell_width='split-20-80',
                line_space = 1.75)

            # Add table of categories
            if self.datastructure[variable]['pyType'] == 'category':
                pdf.ln()
                # Check if population variable is present
                if 'pop_var' in self.datastructure[variable].keys():
                    pop_var = self.datastructure[variable]['pop_var']
                else:
                    pop_var = ''
                table = self.categorical_countfreq_table(
                    variable = variable,
                    primary_key = self.datastructure[variable]['primary_key'],
                    pop_var = pop_var)
                styled_table = table.copy()
                styled_table.reset_index(inplace = True)
                styled_table = styled_table.drop(columns = ['index'])
                
                # Convert DataFrame directly to list of lists for PDF table
                table_data = [styled_table.columns.tolist()] + styled_table.values.tolist()
                title = variable+': '+self.datastructure[variable]['label'] + \
                    ' - Categorical codes, labels and frequencies'
                #  Number of columns in Table Data
                ncols = len(table_data[0])
                # If 6 columns then cell widths needs 6 widths
                print(ncols)
                if ncols == 6:
                    cell_widths = [12,pdf.epw-(12+24+24+18+18),
                                   24,24,18,18]
                elif ncols == 5:
                    cell_widths = [12,pdf.epw-(12+24+24+30),30,
                                   24,24]   
                elif ncols == 4:
                    cell_widths = [12,pdf.epw-(12+24+24),
                                   24,24]
                else:
                    # Default case: distribute columns evenly
                    cell_widths = 'even'                
                pdf.create_table(table_data = table_data, title=title, 
                    data_size= 10, title_size = 12,
                    align_data = 'R', align_header = 'C', 
                    cell_width=cell_widths,
                    line_space = 1.75)
            # Add notes
            if 'notes' in self.datastructure[variable]:
                notes = self.datastructure[variable]['notes'] 
                # If notes contain placeholders, user must provide formatted notes.
                # No automatic county FIPS insertion.
                pdf.cell(w = 0, h = 10, text = f"Variable Notes: {variable}", border = 0, ln = 1)
                pdf.multi_cell(0, 3, notes, ln = 3, align = 'L',
                                max_line_height=pdf.font_size*2)
                pdf.ln()

            pdf.add_page()



    def create_codebook(self):
        """
        Generate codebook for string variables as PDF File
        """
        
        # Use header_title directly for generic codebook generation
        header_text = self.header_title
        print(f"Creating codebook: {header_text}")
        
        pdf = PDF(
            header_text = header_text,
            footer_text = f"{self.output_filename}",
            image_path = self.image_path)
        
        pdf.set_margins(left = 15, top = 10)
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
        pdf.insert_toc_placeholder(self.render_toc,pages=1)
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
        codebook_filepath = self.outputfolders['top']+"/"+self.output_filename+'.pdf'
        print("Saving codebook to",codebook_filepath)
        pdf.output(codebook_filepath)
