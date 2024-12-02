# Customer Support Project
A powerful AI-driven assistant for customer support that can process and respond to audio messages sent by users. This project utilizes a Flask API to receive audio files, process them asynchronously, and return AI-generated responses based on the content of the audio.

## Prerequisites

Before you begin, ensure that you have the following installed:

- **Python 3.9** (Required)
  - This project is built using Python 3.9. Other Python versions may work, but compatibility is not guaranteed.
  - You can download Python 3.9 from the official Python website: [https://www.python.org/downloads/release/python-390/](https://www.python.org/downloads/release/python-390/)

## Installation

To get started with the project, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/customer-support-project.git
    ```

2. Navigate to the project directory:

    ```bash
    cd customer-support-project
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    python3.9 -m venv venv
    ```

4. Activate the virtual environment:

    - On **Windows**:
    
      ```bash
      .\venv\Scripts\activate
      ```

    - On **macOS/Linux**:

      ```bash
      source venv/bin/activate
      ```

5. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

Once you've installed the dependencies, you can run the application locally:

```bash
python app.py
