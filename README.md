# AI Research Tool: Earnings Call & Management Commentary Analyzer

An AI-powered research tool that ingests earnings call transcripts (PDF/TXT) and produces a deterministic, deterministic, structured, and analyst-usable summary. 

This is an L2-level assignment built using FastAPI, Pydantic, and the OpenAI SDK. The frontend consists of pure, minimal HTML/CSS/JS with zero heavy frameworks, emphasizing backend quality and reliability.

## 🚀 How the Tool Works

1. **Upload**: The researcher uploads a document containing management commentary or an earnings call transcript (.txt or .pdf).
2. **Ingestion**: The backend extracts the raw text. For PDFs, it utilizes `pdfplumber` to accurately read page-by-page. Check `backend/document_parser.py`.
3. **Analysis**: The raw string is sent via the OpenAI SDK (using the `gpt-4o` or configured model) with **Structured Outputs** (`client.beta.chat.completions.parse`).
4. **Output Generation**: The LLM responds using the strict `EarningsCallSummary` Pydantic model (`backend/models.py`), representing the exact JSON schema required by the assignment.
5. **Presentation**: The vanilla JS frontend receives the JSON, rendering the data into a clean, professional dashboard view. It strictly displays missing fields as "Not mentioned in transcript" per the system prompt.

## 🛠️ Key Design Decisions

- **FastAPI + Uvicorn**: Chosen for high performance, modern Python type-hinting support (Pydantic), and simplicity in building robust APIs.
- **Pydantic Models**: Centralizes the definition of the data contract between the LLM, the backend router, and the frontend. It guarantees that the frontend receives identically structured data every time.
- **Vanilla JS + HTML + CSS**: Used for the frontend to fulfill the "simple HTML + JS (no React needed)" requirement while still looking professional and avoiding unnecessary build steps.
- **`model.beta.chat.completions.parse`**: Native Structured Outputs from OpenAI ensures absolute conformity to the JSON schema, drastically reducing parsing errors compared to basic JSON prompting.

## 🛑 How Hallucination is Avoided

The system avoids hallucination and maintains an objective, deterministic analyst profile through strict prompt engineering and model settings:

1. **Temperature = 0.0**: Enforces highly deterministic answers from the LLM.
2. **Strict System Prompt rules**: 
   - *"ONLY use the information explicitly found in the provided transcript text."*
   - *"Do NOT guess, infer, or fabricate"*
3. **Explicit "Missing Info" protocol**: The prompt strictly instructs the model that if an attribute is missing, it **MUST** return `"Not mentioned in transcript"`. This eliminates the model's tendency to confidently guess or extrapolate data.
4. **Pydantic `Field` descriptions**: Each parameter within the Pydantic schema has a `description` explicitly instructing the LLM about the fallback expected when data is missing.

## 💻 Local Setup Instructions

1. **Clone the repository and enter the directory**:
   ```bash
   cd ai-research-tool
   ```

2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add your API Key.
   ```env
   OPENAI_API_KEY="your-api-key-here"
   # If using Gemini with openai SDK compatibility:
   # OPENAI_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
   # OPENAI_API_KEY="your-gemini-key"
   ```

5. **Run the Server**:
   ```bash
   uvicorn backend.main:app --reload
   ```

6. **Open Tool**:
   Navigate to `http://localhost:8000` in your web browser.

## ☁️ Deployment on Render

This tool easily deploys on Render as a Web Service.

1. Create a `New Web Service` on Render and connect your GitHub repository.
2. **Environment**: `Python 3`
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**: Add your `OPENAI_API_KEY` in the Render dashboard. DO NOT commit it to Git.

### Known Limitations of Free Hosting (Render)
- **Cold Boot Instantiation**: The free tier automatically spins down after 15 minutes of inactivity. The next time you make a request to the server, it will take up to ~50 seconds for the container to wake up and process your PDF upload.
- **RAM Limits**: The free tier has a 512MB RAM cap. Processing massive PDFs (>50-100 pages) simultaneously using `pdfplumber` might cause out-of-memory container crashes.
- **CPU Limits**: Text extraction heavily loads the CPU, adding 5-10 extra seconds to processing times on the free tier compared to a local machine.
