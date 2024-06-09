import streamlit as st
import pdfminer.high_level
import re
import csv
from io import StringIO

def read_pdf(file):
    text = pdfminer.high_level.extract_text(file)
    return text

def convert_to_csv(data):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerows(data)
    return output.getvalue()

def main():
    st.markdown("<h1 align=center>Text Extractor from PDF</h1>", unsafe_allow_html=True)
    # File uploader for PDF files
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    # Check if a file is uploaded
    if uploaded_file is not None:
        # Read PDF
        text = read_pdf(uploaded_file)
        
        # Regular expressions to match specific patterns
        mail_pattern = re.compile(r'\b[a-zA-Z0-9]{2,}@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b')
        phone_pattern = re.compile(r'\b(?:\d{3}-\d{3}-\d{4}|\d{10})\b')
        amount_pattern = re.compile(r'\b(?:\d{1,3}(?:,\d{3})*|\d+)?(?:\.\d{1,2})\b')

        # Extracting information
        mail = mail_pattern.findall(text)
        phone = phone_pattern.findall(text)
        amount = amount_pattern.findall(text)
       
        # Display the extracted text
        st.subheader("Extracted Email Addresses:")
        st.write(mail)
        st.subheader("Extracted Phone Numbers:")
        st.write(phone)
        st.subheader("Extracted Amounts:")
        st.write(amount)

        # Allow user to download the extracted data as CSV
        if st.button("Download Extracted Data as CSV"):
            csv_data = [["Category", "Extracted Text"]]
            for em in mail:
                csv_data.append(["Email Address", em])
            for ph in phone:
                csv_data.append(["Contact No.", ph])
            for am in amount:
                csv_data.append(["Amount", am])
            
            csv_file = convert_to_csv(csv_data)
            st.download_button(
                label="Download CSV",
                data=csv_file,
                file_name='extracted_data.csv',
                mime='text/csv'
            )

if __name__ == "__main__":
    main()

