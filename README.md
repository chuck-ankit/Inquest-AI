# InquestAI

InquestAI is a FastAPI-based web application that allows users to upload PDF documents and analyze them using a Large Language Model (LLM) pipeline. The application extracts questions and generates corresponding answers from the uploaded documents, saving the results in a CSV format for easy access.

## Features

- **PDF Upload**: Upload a PDF file through a web interface.
- **Question-Answer Generation**: Automatically extract questions and generate answers from the uploaded PDF using a custom LLM pipeline.
- **CSV Export**: Save the generated question-answer pairs in a CSV file.
- **Web Interface**: Simple and clean user interface built with FastAPI and Jinja2 templates.

## Table of Contents

- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [File Structure](#file-structure)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Links](#links)

## Installation

### Requirements

To run InquestAI, you will need:

- Python 3.8+
- FastAPI
- Uvicorn
- aiofiles
- Jinja2

You can install the required dependencies using pip. Create a `requirements.txt` file with the following content:

