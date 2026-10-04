# Gemini Personal Assistant

A lightweight web application built with Flask and the Google Gemini API. It offers two tools in a single page: a general-purpose question assistant and an email summarizer that condenses pasted emails into two or three sentences.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)
- [How It Works](#how-it-works)
- [Customization](#customization)
- [Privacy and Security](#privacy-and-security)
- [Known Limitations](#known-limitations)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Overview

Gemini Personal Assistant is a small, easy-to-read full-stack project that demonstrates how to connect a Flask backend to a hosted large language model and expose it through a simple browser interface. The frontend is plain HTML, CSS and JavaScript with no build step, and the backend is a single Python file.

The application has two features:

1. **Ask Anything** - type a question and receive an answer from the model, prompted to behave like a helpful personal assistant.
2. **Summarize Email** - paste the body of an email and receive a short summary.

## Features

- Single-page interface with two independent tools
- Flask backend with two JSON endpoints
- Google Gemini integration through the official `google-genai` SDK
- Separate generation settings per feature: a higher temperature for open-ended answers and a lower one for consistent summaries
- Loading indicators while a request is in progress
- Basic input validation with clear error messages
- Light and dark theme support that follows the system setting
- Responsive layout for desktop and mobile
- API key kept out of source control through environment variables

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Python 3, Flask |
| AI model | Google Gemini via the `google-genai` SDK |
| Configuration | `python-dotenv` |
| Frontend | HTML5, CSS3, vanilla JavaScript (Fetch API) |
| Templating | Jinja2 (bundled with Flask) |

## Project Structure

```
.
├── main.py              # Flask app: routes and Gemini calls
├── templates/
│   └── index.html       # Single-page UI and client-side JavaScript
├── static/
│   └── style.css        # Stylesheet
├── .env                 # Local secrets (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

Flask expects HTML templates in a folder named `templates` and static files in a folder named `static`. The template references the stylesheet with `url_for('static', filename='style.css')`, so keep this layout.

## Getting Started

### Prerequisites

- Python 3.9 or newer
- A Google Gemini API key. You can create one in [Google AI Studio](https://aistudio.google.com/).
- Git

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>
   ```

2. Create and activate a virtual environment:

   ```bash
   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows (PowerShell)
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   If you do not have a `requirements.txt` yet, create one with the following contents:

   ```
   flask
   python-dotenv
   google-genai
   ```

4. Create a `.env` file in the project root:

   ```
   GEMINI_API_KEY=your_api_key_here
   ```

5. Start the development server:

   ```bash
   python main.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.

## Configuration

| Variable | Required | Description |
| --- | --- | --- |
| `GEMINI_API_KEY` | Yes | API key used to authenticate with the Gemini API |

Model and generation settings are defined directly in `main.py`:

| Feature | Temperature | Max output tokens |
| --- | --- | --- |
| Ask Anything (`/ask`) | 0.7 | 2048 |
| Summarize Email (`/summarize`) | 0.3 | 512 |

The model name is set in each `generate_content` call. Make sure the model you specify is available to your API key; the list of current model names is in the Gemini API documentation. To change it, edit the `model` argument in both routes, or move it into a constant or environment variable to keep a single source of truth.

Add the following to `.gitignore` so secrets and local files are never committed:

```
.env
venv/
__pycache__/
*.pyc
```

## Usage

### Ask Anything

1. Type a question in the text field under **Ask Anything**.
2. Click **Ask**.
3. A "Processing..." message appears while the request runs, followed by the answer.

### Summarize Email

1. Paste the full text of an email into the text area under **Summarize Email**.
2. Click **Summarize**.
3. The summary appears below the form after processing.

## API Reference

Both endpoints accept `POST` requests with form-encoded data and return JSON.

### POST `/ask`

Sends a question to the model.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `question` | string | Yes | The question to answer |

Example request:

```bash
curl -X POST http://127.0.0.1:5000/ask \
  -d "question=Give me three tips for planning a productive week"
```

Success response (`200 OK`):

```json
{
  "response": "Here are three tips for planning a productive week..."
}
```

Error response (`400 Bad Request`):

```json
{
  "error": "Question is required"
}
```

### POST `/summarize`

Summarizes email text in two to three sentences.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `email_content` | string | Yes | The email body to summarize |

Example request:

```bash
curl -X POST http://127.0.0.1:5000/summarize \
  --data-urlencode "email_content=Hi team, the quarterly review has moved to Thursday at 3 PM..."
```

Success response (`200 OK`):

```json
{
  "summary": "The quarterly review has been rescheduled to Thursday at 3 PM."
}
```

Error response (`400 Bad Request`):

```json
{
  "error": "Email content is required"
}
```

### GET `/`

Serves the single-page interface.

## How It Works

1. The browser submits a form using the Fetch API with `FormData`.
2. Flask reads the form field, validates that it is not empty, and builds a prompt.
3. The backend calls `client.models.generate_content` with the prompt and the generation settings for that feature.
4. The text of the model response is trimmed and returned as JSON.
5. The frontend writes the result into the page using `innerText`, which prevents model output from being interpreted as HTML.

Prompts used:

- **Ask Anything:** the question is prefixed with an instruction to act as a helpful personal assistant.
- **Summarize Email:** the model is instructed to act as an expert email assistant and summarize the email in two to three sentences.

## Customization

- **Change the assistant persona:** edit the instruction text at the start of the prompt in `ask_question()`.
- **Change summary length or style:** edit the prompt in `summarize()`, for example to request bullet points or action items.
- **Tune creativity:** raise `temperature` for more varied answers or lower it for more consistent output.
- **Allow longer answers:** increase `max_output_tokens`.
- **Restyle the interface:** colors, radii and spacing are defined as CSS variables at the top of `style.css`.

Make sure the CSS selectors match the element classes and IDs in `index.html`. The current markup uses the `chat-container` class and the `chat-answer` and `email-summary` IDs, so the stylesheet must target those names for the styles to apply.

## Privacy and Security

- Questions and email content are sent to the Google Gemini API for processing. Do not paste confidential, regulated or personal information unless you have reviewed Google's data handling terms for the API tier you use.
- Never commit your `.env` file or hard-code your API key. If a key is ever exposed, revoke it in Google AI Studio and create a new one.
- The Flask development server and `debug=True` are intended for local use only. Do not expose the debug server to the public internet, because debug mode can allow remote code execution.
- The application has no authentication or rate limiting. If you deploy it publicly, anyone with the URL can consume your API quota.

## Known Limitations

- No conversation memory. Each question is treated independently.
- No streaming. The full response appears only after generation completes.
- The Gemini call is not wrapped in error handling on the server. If the API fails (invalid key, quota exceeded, network error), Flask returns a generic server error and the interface shows "Something went wrong. Please try again."
- No limit on input length beyond the model's own limits.
- No authentication, user accounts or request throttling.
- Output is displayed as plain text, so Markdown formatting from the model is not rendered.

## Troubleshooting

**The page loads but has no styling.**
Confirm that `style.css` is inside a folder named `static` and that `index.html` is inside `templates`. Also check that the CSS selectors match the class and ID names in the HTML.

**"Something went wrong. Please try again." appears for every request.**
Check the terminal running Flask for the underlying error. Common causes are a missing or invalid `GEMINI_API_KEY`, an unavailable model name, or exceeded quota.

**`ModuleNotFoundError` on startup.**
Activate your virtual environment and run `pip install -r requirements.txt` again.

**The API key is not being read.**
Make sure the `.env` file is in the same directory you run `python main.py` from and that the variable is spelled exactly `GEMINI_API_KEY` with no quotes or spaces around the equals sign.

**Port 5000 is already in use.**
Run the app on another port by changing the last line of `main.py` to `app.run(debug=True, port=5001)`.

## Roadmap

Ideas for future improvement:

- Server-side error handling with meaningful error messages for API failures
- Streaming responses for faster perceived output
- Conversation history for follow-up questions
- Markdown rendering of answers
- Copy-to-clipboard buttons for answers and summaries
- Additional tools such as email reply drafting, tone rewriting and translation
- Input length limits and rate limiting
- Docker support and a production configuration using Gunicorn
- Automated tests for the API routes

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes with a clear message.
4. Push the branch and open a pull request describing what you changed and why.

For larger changes, please open an issue first to discuss the approach.

## License

Add a license file to specify how others may use this project. The MIT License is a common choice for small open-source projects. Replace this section with the license you choose.
