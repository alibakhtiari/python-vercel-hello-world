import win32com.client

def add_text_to_cdr(cdr_file, text, x, y, font_name, font_size):
    # Create a CorelDRAW application object
    corel_app = win32com.client.Dispatch("CorelDRAW.Application")
    
    # Open the CDR file
    cdr_doc = corel_app.OpenDocument(cdr_file)
    
    # Add a new text shape to the document
    text_shape = cdr_doc.ActiveLayer.CreateArtisticText(x, y, text)
    
    # Set the font properties for the text shape
    text_range = text_shape.Text.Story.Range
    text_range.FontProperties.Name = font_name
    text_range.FontProperties.Size = font_size
    
    # Save and close the document
    cdr_doc.Save()
    cdr_doc.Close()
    
    # Quit CorelDRAW application
    corel_app.Quit()

def add_qrcode_to_cdr(cdr_file, qr_code_file, x, y, width, height):
    # Create a CorelDRAW application object
    corel_app = win32com.client.Dispatch("CorelDRAW.Application")
    
    # Open the CDR file
    cdr_doc = corel_app.OpenDocument(cdr_file)
    
    # Import the QR code file as a new shape
    cdr_doc.ActiveLayer.Import(qr_code_file, x, y, x + width, y + height)
    
    # Save and close the document
    cdr_doc.Save()
    cdr_doc.Close()
    
    # Quit CorelDRAW application
    corel_app.Quit()

# Example usage
cdr_file_path = "path/to/your/file.cdr"
qr_code_file_path = "path/to/your/qrcode.png"

# Add text to the CDR file
add_text_to_cdr(cdr_file_path, "Hello, World!", 100, 100, "Arial", 12)

# Add QR code to the CDR file
add_qrcode_to_cdr(cdr_file_path, qr_code_file_path, 200, 200, 100, 100)




# Make sure you have the pywin32 library installed (pip install pywin32) before running this code. Also, replace "path/to/your/file.cdr" and "path/to/your/qrcode.png" with the actual paths to your CDR file and QR code image file, respectively. Adjust the coordinates and other parameters according to your requirements.

# Please note that this code assumes you have CorelDRAW installed on your machine and it is associated with .cdr files.