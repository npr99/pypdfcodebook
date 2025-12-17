## Instructions for Project Overview

A project overview provides essential context that helps users understand the purpose, scope, and key details of your dataset. It orients new users, supports transparency, and ensures that the data is used appropriately and interpreted correctly.

**Please include information about your project, such as:**

### Required:
**Project title**: Clear, descriptive name for your project or dataset
**Principal Investigator(s)**: Lead researcher(s) with contact information

### Good to have:
**Required citations**: How others should cite your work or dataset
**Project description**: What questions is this research trying to answer and why it matters
**Funding source**: Grant numbers, award names, and funding agency information
**Data provenance**: Detailed information about data sources, collection methods, and any synthetic/simulated elements

### Good to include if survey data:
**Data collection context** - When, where, and how the data was collected
**Target population** - Who or what the data represents
**Sample size and methodology** - How many observations and what sampling approach
**Time period** - When the data was collected and what time frame it covers
**Geographic scope** - Location(s) where the data applies

### Good to include if known:
**Related works** - Publications, reports, or other research using or related to this data
**Keywords** - Terms that help others discover and categorize your work
**License** - Legal terms governing how others may use your data
**Limitations and considerations** - Important caveats about data use and interpretation

## File Format Requirements

When you have your project overview file completed, pypdfcodebook requires that this is saved as a **markdown file** (with `.md` extension). Markdown is a text file with simple formatting options.

### Formatting Support in PDF Output

**Important:** pypdfcodebook uses fpdf2 to convert your markdown content to PDF, which has limited formatting support. Only these markdown features will be rendered in the final PDF:

- **Bold text**: Use `**bold text**` 
- *Italic text*: Use `__italic text__`
- Underlined text: Use `--underlined text--`

**Formatting that will NOT appear in the PDF:**
- Headers (# ## ###) - these are ignored in PDF rendering
- Bullet lists (- or *) - these become plain text
- Numbered lists (1. 2. 3.) - these become plain text  
- Links [text](url) - only the text portion displays
- Code blocks or inline code - these become plain text

### Recommendations for Best Results

1. **Use descriptive text** rather than relying on headers for organization
2. **Use bold formatting** (`**text**`) to emphasize important information like section names
3. **Write in paragraph form** rather than using bullet lists, since lists won't format properly
4. **Keep it simple** - focus on clear, well-written content rather than complex formatting

### Creating Your Files

For both project overview and key terms files:
- Save as `.md` files (e.g., `project_overview.md`, `keyterms.md`)
- Use any text editor (Notepad, VS Code, etc.)
- Focus on clear content over complex formatting
- Use the simple bold/italic formatting sparingly for emphasis

*This section was auto-generated using the default instruction mode in pypdfcodebook. To turn off instruction mode set instruction_mode to False in the codebook command. Please replace with actual project details relevant to your dataset and research.*