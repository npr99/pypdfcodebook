## Instructions for Key Terms and Definitions

Key terms provide essential definitions that ensure future data users do not have to assume what terms mean, promoting clear understanding and consistent interpretation of the dataset and its documentation.

**Please define key terms related to your project, including:**

- **Technical terminology** used in variable names or descriptions
- **Domain-specific concepts** relevant to your field of study
- **Measurement units** and their definitions
- **Categorical codes** and what they represent
- **Analysis concepts** that may not be familiar to all users

This process may require a literature review and communication with the data creator. If you do not know what a term in the dataset means it is ok to simply state "Definition unknown".


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