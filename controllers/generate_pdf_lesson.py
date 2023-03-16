import os
from fpdf import FPDF
from models.lesson import Lesson

# a controller that takes a lesson and parameters and generates a pdf file of the lesson
class PDFLessonGenerator():
    # takes a lesson and parameters and generates a pdf file of the lesson
    def __init__(self, lesson: Lesson, **params: dict):
        self.lesson = lesson
        self.params = params
        self.pdf = FPDF()     
    
    def get_file_name(self):
        return self.lesson.lesson_name
    
    def format_content(self):

        # Set the table header to language one and language two
        self.text = f'{self.lesson.origin_language};{self.lesson.target_language}\n{self.lesson.content}'
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
        self.pdf.cell(0, 20, f'{self.lesson.lesson_name}', 0, 1, 'C')

        # add a paragraph of text with the lesson introduction
        self.pdf.set_font('Arial', '', 14)
        self.pdf.multi_cell(0, 10, f'{self.lesson.intro}', 0, 1, 'L')

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
        self.pdf.output(f'{self.lesson.lesson_name}.pdf', 'F')
        return f'{self.lesson.lesson_name}.pdf'

    def gen_pdf(self):
        return self.pdf.output(f'{self.lesson.lesson_name}.pdf', 'F')

    def delete_pdf_file(self):
        os.remove(f'{self.lesson.lesson_name}.pdf')