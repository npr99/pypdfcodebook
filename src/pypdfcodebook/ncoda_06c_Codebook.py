import pandas as pd
import numpy as np
import csv
import random # used for selecting random examples of

from pypdfcodebook.ncoda_06a_PDF_functions import PDF, TitleStyle
from pypdfcodebook.ncoda_04a_Figures import income_distribution

class codebook():
    """
    Functions to create a pdf codebook for data
    """
    def __init__(self,
            input_df,
            header_title,
            datastructure,
            projectoverview,
            keyterms,
            communities,
            community,
            year,
            output_filename,
            outputfolders = {},
            seed = 15151,
            figures = '',
            image_path = ""):
        self.input_df = input_df
        self.header_title = header_title
        self.datastructure = datastructure
        self.projectoverview = projectoverview
        self.keyterms = keyterms
        self.communities = communities
        self.community = community
        self.year = year
        self.output_filename = output_filename
        self.outputfolders = outputfolders
        self.seed = seed
        self.figures = figures
        self.image_path = image_path
