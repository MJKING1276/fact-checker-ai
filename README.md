# Fact Checker AI Agent

## Overview

This project leverages Google Generative AI and NewsAPI to create a fact-checking agent. The agent receives a claim (a statement or news item) and verifies its accuracy, returning a verdict and explanation. The app is built with Flask and utilizes a beautiful, retro-styled web interface.
Prerequisites

## Features

- Users can submit claims (facts or statements) to be verified.
- The system pulls news articles related to the claim using News API.
- **Google Generative AI (Gemini 2.0)** is used to generate detailed fact-checking results.
- The app displays:
  - The claim.
  - The accuracy of the claim.
  - The verdict (CORRECT, WRONG, UNVERIFIABLE).
  - A detailed explanation based on AI analysis.
  
## Requirements

- Python 3.8+
- **Flask**: A micro web framework for Python.
- **dotenv**: To load environment variables from a `.env` file.
- **requests**: To make HTTP requests to external APIs (News API).
- **google-generativeai**: To use Google’s generative AI for fact-checking.
- **News API Key**: To access news data for claim verification.
- **Google Generative AI Key**: For AI-based fact-checking analysis.

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/fact-checker-ai-agent.git
    cd fact-checker-ai-agent
    ```

2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables by creating a `.env` file in the root directory:
    ```bash
    NEWSAPI_KEY=your_newsapi_key
    GENAI_API_KEY=your_google_genai_key
    ```

4. Run the Flask application:
    ```bash
    python app.py
    ```

5. Open a web browser and go to `http://127.0.0.1:5000` to access the application.

## How It Works

### 1. User Interface
When the user visits the homepage, they see an interface with the title **"FACT CHECKER AI AGENT"** and a form where they can input a claim (e.g., "The earth is flat"). 

Once the user submits a claim:
- The form sends the claim to the server via a POST request.
- The server processes the claim, queries News API for related sources, and sends the claim to Google Generative AI for analysis.

### 2. Fact-Checking Process
- **News API**: Retrieves news articles related to the claim.
- **Google Generative AI (Gemini 2.0)**: Uses the retrieved news sources and AI reasoning to analyze the claim, providing an accuracy score, verdict, and explanation.

### 3. Results
After processing, the server responds with a verdict that can be:
- **CORRECT ✅**
- **WRONG ❌**
- **NOT VERIFIABLE ❓**

The result is displayed to the user along with a percentage accuracy and a detailed explanation of the reasoning.

## Example Output

For a claim like **"The moon is made of cheese"**:
- **Verdict**: WRONG ❌
- **Accuracy**: 30%
- **Explanation**: The moon is not made of cheese. Scientific evidence suggests that the moon is primarily composed of rock and minerals, not dairy products. 



### Notes

- **Error Handling**: If the AI model or APIs return an error, the user is informed with an appropriate message.
- **Performance**: While the app is generally fast, external API calls (to News API and Google Generative AI) may take some time, depending on the claim's complexity and the number of sources retrieved.

Enjoy verifying your claims with AI!


