import PyPDF2
import pyperclip

# Open the PDF file
pdfFileObj = open('docs/attention_sink.pdf','rb') 

# Create pdf reader object
pdfReader = PyPDF2.PdfReader(pdfFileObj)  

# Store number of pages
num_pages = len(pdfReader.pages)

# Create string to store extracted text 
extracted_text = ""  

# Loop through pages
for page_num in range(num_pages):
    # Get page object
    pageObj = pdfReader.pages[page_num]  
    
    # Extract text 
    extracted_text += pageObj.extract_text()

# Close pdf file  
pdfFileObj.close()

# Copy text to clipboard
pyperclip.copy(extracted_text)

print("Text copied to clipboard!")