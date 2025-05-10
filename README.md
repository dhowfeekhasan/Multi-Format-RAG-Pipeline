![image](https://github.com/user-attachments/assets/47191352-9130-492b-aaf4-297ccc46b7e0)



**Overview**

This project is an AI-driven system designed to process and extract meaningful data from various file formats, including PDFs, Word documents, PowerPoint presentations, Excel sheets, and images. By leveraging advanced Natural Language Processing (NLP) techniques, it allows users to query the content of these documents using natural language and receive context-aware responses.

**Features**
- Multi-Format Support: Processes a wide range of document formats (PDF, DOCX, PPTX, XLSX, JPG, PNG) and extracts text, tables, and images.

- Intelligent Text Extraction: Uses powerful libraries like PyMuPDF, pdfplumber, python-docx, and PIL to extract structured data from different file types.

**Indexed Search**: The extracted content is indexed using sentence-transformer embeddings, enabling efficient and accurate semantic search.

**Natural Language Queries**: Users can interact with the system by asking questions in natural language, and the system retrieves relevant content from the indexed documents.

**Contextual Answers**: A local LLaMA 2 model processes the retrieved data and generates precise answers, ensuring they are contextually relevant.

**Technologies Used**
**Python Libraries**: fitz (PyMuPDF), pdfplumber, python-docx, pandas, pptx, pytesseract, Sentence-Transformer

**Machine Learning**: Sentence-Transformer (for semantic search), LLaMA 2 (for contextual answers)

**OCR**: Tesseract (for text extraction from images)

**Data Processing**: Pandas (for Excel data extraction), Pillow (for image processing)

**How It Works**
**File Upload**: Users can upload documents in various formats.

**Text and Data Extraction**: The system processes each file, extracting text, tables, and images.

**Indexing**: Extracted content is indexed for fast retrieval using sentence-transformer embeddings.

**Querying**: Users can ask questions, and the system uses the indexed data to retrieve the most relevant content.

**Answer Generation**: The LLaMA 2 model generates a response based on the retrieved content, ensuring the answer is contextually accurate.

**How to Use**
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/document-query-system.git


**Install the required dependencies**:
bash
Copy
Edit
pip install -r requirements.txt

**Run the main script:**
bash
Copy
Edit
streamlit run app.py
Follow the on-screen instructions to upload documents and ask queries.
![image](https://github.com/user-attachments/assets/6ec8caec-b793-4622-95de-683ae1a16ee5)


License
This project is licensed under the MIT License - see the LICENSE file for details.
