# Interview Q&A API

An API for interview preparation and Q&A using RAG (Retrieval-Augmented Generation) technology.

## Features

- Upload PDF documents as knowledge sources
- Generate interview questions based on selected knowledge sources
- Submit answers and receive AI-powered evaluations
- Support for multiple interview domains (Data Science, Software Engineering, etc.)

## Prerequisites

- Python 3.11 or higher

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Before running the application, make sure you have the following API keys set up:

1. Create a `.env` file in the `src` directory
2. Copy the content from `.env_example` to `.env`

Note: You can generate your API Keys from the following:
- OPENAI_API_KEY --> https://platform.openai.com/api-keys
- GROQ_API_KEY --> https://console.groq.com/keys
- LANGCHAIN_API_KEY --> https://docs.langchain.com/langsmith/create-account-api-key
## Running the Application

1. Start the API server:
   ```
   python main.py
   ```

2. The API will be available at `http://localhost:5000`

## API Endpoints

### API Information
- **URL**: `GET /api/info`
- **Description**: Returns detailed information about the API endpoints

### Get Available Sources
- **URL**: `GET /api/sources`
- **Description**: Returns a list of available knowledge sources (PDF files)

### Select Knowledge Source
- **URL**: `POST /api/select_source`
- **Description**: Select a knowledge source to use for Q&A
- **Request Body**:
  ```json
  {
    "source_name": "Data Science"
  }
  ```

### Generate Interview Question
- **URL**: `GET /api/generate_question`
- **Description**: Generate a new interview question from the selected knowledge source

### Submit Answer
- **URL**: `POST /api/submit_answer`
- **Description**: Submit an answer to the current interview question and get evaluation with scores
- **Request Body**:
  ```json
  {
    "answer": "Your answer here"
  }
  ```
## Usage Example

1. First, check available sources:
   ```
   GET http://localhost:5000/api/sources
   ```

2. Select a knowledge source:
   ```
   POST http://localhost:5000/api/select_source

   {
     "source_name": "Data Science"
   }
   ```

3. Generate an interview question:
   ```
   GET http://localhost:5000/api/generate_question
   ```

4. Submit your answer:
   ```
   POST http://localhost:5000/api/submit_answer
   Content-Type: application/json

   {
     "answer": "Your answer to the question"
   }
   ```

## Available Knowledge Sources

The application comes with pre-loaded PDF files in the `data` directory and you can add to it later:
- Data Analyst.pdf
- Data Science.pdf
- Mechanical Engineering.pdf
- Planning Engineers.pdf
- SQL.pdf
- Software Engineering.pdf