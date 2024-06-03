# Resume Parser with BERT NER

A Python-based resume parser that leverages BERT-based Named Entity Recognition (NER) to extract relevant information from resumes. The model identifies entities such as:

- **Names**
- **Colleges**
- **Degrees**
- **Work Experience**
- **Skills**
- **Locations**
- **Email addresses**
- **Phone numbers**

## Features

- **NER Model:**
  - Utilizes a BERT-based NER pretrained model from Hugging Face, fine-tuned for accurate entity extraction.
- **Data Preprocessing:**
  - Includes data cleaning and normalization steps to improve model performance.
- **User-Friendly Web Application:**
  - Provides code-free execution of parsing via a web interface.
  - Accepts plain text resumes.
- **Easy Deployment:**
  - Can be used in virtual environments like Google Colab (via ngrok integration).
- **Model Availability:**
  - The model is larger than the recommended size for GitHub, so it must be downloaded separately from this link.
  - https://drive.google.com/file/d/1xwWUFBlMW18mPb3Qzt_204xCwDzSA3W5/view?usp=sharing
  - Extract the model in the cloned repository before running the application.
