# takes the text as input and creates a pdf file with the text
import os
from fpdf import FPDF

class PDFGenerator:
    def __init__(self, text, language_1, language_2, file_name):
        self.text = text
        self.language_1 = language_1
        self.language_2 = language_2
        self.file_name = file_name
        self.pdf = FPDF()        
    
    def get_file_name(self):
        return self.file_name
    
    def format_content(self):

        # Set the table header to language one and language two
        self.text = f'{self.language_1};{self.language_2}\n{self.text}'
        # Split the text into rows and columns
        rows = self.text.split('\n')
        rows = [row.split(';') for row in rows]

        # remove any white space in front of the string for each row        
        rows = [[row[0].strip(), row[1].strip()] for row in rows]

        # Create a new PDF object and add a page
        
        self.pdf.add_page()    

        self.pdf.add_font('Arial', '', 'arial.ttf', uni=True)
        # Add a title to the page, centered at the top of the page with a 20pt font
        self.pdf.set_font('Arial',  'B', 20)
        self.pdf.cell(0, 20, f'{self.file_name}', 0, 1, 'C')

        # add a 10% of the page width space between the title and the table
        self.pdf.ln(self.pdf.w * 0.1)

        # Set the title font and font size
        self.pdf.set_font('Arial', 'B', 16)

        # Print the title
        self.pdf.cell(0, 10, 'Translation Table', 0, 1, 'C')

        # Set the table font and font size
        self.pdf.set_font('Arial', '', 14)

        # Set the table column widths so each column is 40% of the page width
        col_widths = [self.pdf.w * 0.4, self.pdf.w * 0.4]        
        # Move to the next line
        self.pdf.ln()


        # Print the table rows
        for row in rows:
            self.pdf.cell(col_widths[0], 10, row[0], 1)
            self.pdf.cell(col_widths[1], 10, row[1], 1)
            self.pdf.ln()
        
        # explain the following line of code, what does the 'F' do?
        # save the pdf file        
        self.pdf.output(f'{self.file_name}.pdf', 'F')

    def gen_pdf(self):
        return self.pdf.output(f'{self.file_name}.pdf', 'F')

    def delete_pdf_file(self):
        os.remove(f'{self.file_name}.pdf')
    

# create a test function that will be used to test the pdf_generator class
def test():
    text = """you are welcome;de rien
    good morning;bonjour
    good afternoon;bonne apres-midi
    good evening;bonne soirée"""
    file_name = "test"
    language_1 = "en"
    language_2 = "fr"
    pdf = PDFGenerator(text, language_1, language_2, file_name)
    pdf.format_content()
    pdf.gen_pdf()
