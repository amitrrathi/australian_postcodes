import re
import pandas as pd
import PyPDF2


def extract_postcode_data(pdf_path, output_excel_path="postcodes.xlsx"):
    """
    Extracts locality names and postcodes from a PDF and saves them to an Excel file.

    Args:
        pdf_path (str): The path to the PDF file.
        output_excel_path (str, optional): The path where the Excel file will be saved.
                                          Defaults to "postcodes.xlsx".
    """

    def extract_text_from_pdf(pdf_path):
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    text = extract_text_from_pdf(pdf_path)
    postcode_list = []
    text = text.replace("NS W", "NSW").replace("N SW", "NSW").replace("VI C", "VIC").replace("V IC", "VIC").replace("Q LD", "QLD").replace("W A", "WA").replace("S A", "SA").replace("T AS", "TAS").replace("TA S", "TAS").replace("N T", "NT").replace("AC T", "ACT").replace("A CT", "ACT")
    """intermittent_matches = re.findall(r'([A-Z\s]+)\s(.)\s(\d{4})', text, re.M)"""
    matches = re.findall(r'([A-Z\s]+)\s+(NSW|VIC|QLD|WA|SA|TAS|NT|ACT)\s+(\d{4})', text, re.M)
    """orig matches = re.findall(r'([A-Z\s]+)\s(NSW|VIC|QLD|WA|SA|TAS|NT|ACT)\s(\d{4})', text, re.M)"""
    
    print(matches)

    for locality, state, postcode in matches:
        postcode_list.append([locality.strip(), state.strip(), postcode.strip()])

    df_postcodes = pd.DataFrame(postcode_list, columns=['Locality Name', 'State', 'Postcode'])

    df_postcodes.drop_duplicates(subset=['Locality Name', 'State', 'Postcode'], keep='first', inplace=True)
    
    df_postcodes.to_excel(output_excel_path, index=False)  # Save to Excel without index

if __name__ == "__main__":
    pdf_file_path = "standard_postcode_file_pc001_23042025.pdf"  # Replace with your PDF file path
    excel_output_path = "australian_postcodes.xlsx"  # Replace with desired output Excel file name
    extract_postcode_data(pdf_file_path, excel_output_path)
    print(f"Postcodes extracted and saved to '{excel_output_path}'")