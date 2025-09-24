import PyPDF2
from pathlib import Path


"""
The purpose of this script is to allow the ability to cut PDFS into specific ranges,
so that range of pages can be put into a LLM for processing
"""
def extract_pages(input_pdf_path, output_pdf_path, start_page, end_page):
    """
    Extract specific pages from a PDF file.
    
    Args:
        input_pdf_path (str): Path to the input PDF file
        output_pdf_path (str): Path for the output PDF file
        start_page (int): Starting page number (1-indexed)
        end_page (int): Ending page number (1-indexed, inclusive)
    """
    start_page = start_page + 22
    end_page = end_page + 22
    try:
        # Open the input PDF
        with open(input_pdf_path, 'rb') as input_file:
            reader = PyPDF2.PdfReader(input_file)
            writer = PyPDF2.PdfWriter()
            
            # Check if page range is valid
            total_pages = len(reader.pages)
            if start_page < 1 or end_page > total_pages or start_page > end_page:
                raise ValueError(f"Invalid page range. PDF has {total_pages} pages.")
            
            # Extract pages (convert to 0-indexed)
            for page_num in range(start_page - 1, end_page):
                page = reader.pages[page_num]
                writer.add_page(page)
            
            # Write to output file
            with open(output_pdf_path, 'wb') as output_file:
                writer.write(output_file)
            
            print(f"Successfully extracted pages {start_page}-{end_page}")
            print(f"Output saved to: {output_pdf_path}")
            
    except FileNotFoundError:
        print(f"Error: Could not find file '{input_pdf_path}'")
    except Exception as e:
        print(f"Error: {str(e)}")


# List of page ranges to extract
Ranges = [
    [136, 148]

]

def batch_cut(input_pdf_path, output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    for i, page_range in enumerate(Ranges, start=1):
        start_page, end_page = page_range
        output_pdf_path = Path(output_dir) / f"pages_{start_page}_to_{end_page}.pdf"
        extract_pages(input_pdf_path, str(output_pdf_path), start_page, end_page)

# Example usage
if __name__ == "__main__":
    input_pdf = "Textbook_Living.pdf"
    output_dir = "extracted_pages"
    batch_cut(input_pdf, output_dir)


