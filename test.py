# import streamlit as st
# import firebase_admin
# from firebase_admin import credentials, db
# from tempfile import NamedTemporaryFile
# from PyPDF2 import PdfReader
# import docx

# # Check if Firebase app is already initialized
# if not firebase_admin._apps:
#     # Initialize Firebase
#     cred = credentials.Certificate("medi-bot-cce34-firebase-adminsdk-s3wca-a0a9493170.json") # Replace with your Firebase credentials
#     firebase_admin.initialize_app(cred, {
#         'databaseURL': 'https://medi-bot-cce34-default-rtdb.firebaseio.com/'
#     })

# # Function to upload PDF file to Firebase Realtime Database
# def upload_pdf_to_firebase(pdf_file):
#     with open(pdf_file, 'rb') as file:
#         pdf_reader = PdfReader(file)
#         text = ""
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#     # Store the text in Firebase Realtime Database
#     ref = db.reference('pdf_documents')
#     ref.push().set({"text": text})

# # Function to upload DOC file to Firebase Realtime Database
# def upload_doc_to_firebase(doc_file):
#     doc = docx.Document(doc_file)
#     text = ""
#     for para in doc.paragraphs:
#         text += para.text
#     # Store the text in Firebase Realtime Database
#     ref = db.reference('doc_documents')
#     ref.push().set({"text": text})

# # Streamlit App
# def main():
#     st.title("Upload PDF and DOC files to Firebase Realtime Database")

#     file = st.file_uploader("Upload PDF or DOC file", type=["pdf", "doc", "docx"])

#     if file is not None:
#         temp_file = NamedTemporaryFile(delete=False)
#         temp_file.write(file.getvalue())

#         if file.type == 'application/pdf':
#             upload_pdf_to_firebase(temp_file.name)
#             st.success("PDF file uploaded successfully!")
#         elif file.type == 'application/msword' or file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
#             upload_doc_to_firebase(temp_file.name)
#             st.success("DOC file uploaded successfully!")
#         else:
#             st.error("Unsupported file format. Please upload a PDF or DOC file.")

# if __name__ == "__main__":
#     main()
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from tempfile import NamedTemporaryFile
from PyPDF2 import PdfReader
import docx

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    # Initialize Firebase
    cred = credentials.Certificate("medi-bot-cce34-firebase-adminsdk-s3wca-a0a9493170.json") # Replace with your Firebase credentials
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://medi-bot-cce34-default-rtdb.firebaseio.com/'
    })

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to upload health-related data and text to Firebase Realtime Database
def upload_data_to_firebase(name, age, weight, other_data, text):
    # Store the data in Firebase Realtime Database
    ref = db.reference('health_data')
    ref.push().set({
        "name": name,
        "age": age,
        "weight": weight,
        "other_data": other_data,
        "pdf_text": text
    })

# Streamlit App
def main():
    st.title("Upload Health Data PDF to Firebase Realtime Database")

    name = st.text_input("Enter Name:")
    age = st.number_input("Enter Age:", min_value=0, max_value=150)
    weight = st.number_input("Enter Weight (kg):", min_value=0.0, max_value=1000.0)
    other_data = st.text_area("Enter Other Health Data:")

    file = st.file_uploader("Upload Health Data PDF", type=["pdf"])

    if file is not None:
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.write(file.getvalue())

        pdf_text = extract_text_from_pdf(temp_file.name)

        upload_data_to_firebase(name, age, weight, other_data, pdf_text)
        st.success("Health data uploaded successfully!")

if __name__ == "__main__":
    main()
