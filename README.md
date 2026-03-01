# Local LLM Document Analysis Dashboard

A web-based document analysis dashboard that integrates with LM Studio for local LLM-powered document processing. Built with Python and NiceGUI, this tool provides a clean interface for analyzing documents using locally-hosted language models.

## Why This Project?

While LM Studio offers excellent desktop-based LLM capabilities, this project addresses several specific needs:

**Customizable Workflow**
LM Studio provides a general-purpose chat interface. This dashboard is specifically designed for document analysis workflows with dedicated features for summarization, key point extraction, and custom queries.

**Web-Based Architecture**
Unlike LM Studio's desktop application, this web-based solution allows:
- Access from any device on the local network
- Team collaboration without passing files around
- Integration into existing web-based workflows
- Easier automation and scripting capabilities

**Extensible Foundation**
Built as an open-source project with a modular architecture:
- Add custom analysis templates for specific use cases
- Integrate additional document processing pipelines
- Extend with domain-specific features (legal, medical, technical analysis)
- Build batch processing capabilities for multiple documents

**Learning and Development**
Serves as a practical example of:
- LM Studio API integration
- NiceGUI web application development
- Local LLM workflow automation
- Document processing pipeline architecture

**Privacy-First Design**
All processing happens locally with complete data privacy, while providing a more tailored interface than general-purpose chat tools.

## Features

**Document Processing**
- Support for multiple formats: PDF, TXT, DOCX, Markdown
- File validation and size limits
- Real-time document upload and processing

**Analysis Capabilities**
- Custom query analysis with natural language
- One-click document summarization
- Automatic key point extraction
- Streaming results display

**User Interface**
- Modern dark mode interface
- Responsive layout with dedicated panels
- Real-time connection health monitoring
- Scrollable results with custom styling

**Local LLM Integration**
- Direct integration with LM Studio API
- No cloud services or API costs
- Complete data privacy
- Support for any LM Studio compatible model

## Prerequisites

- Python 3.8 or higher
- LM Studio installed and running (download from [lmstudio.ai](https://lmstudio.ai))
- A language model loaded in LM Studio

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/local-llm-doc-assistant.git
cd local-llm-doc-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` to match your setup:
```
LM_STUDIO_API_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=your-model-name
APP_PORT=8080
```

## Usage

1. Start LM Studio and load your preferred language model

2. Run the application:
```bash
python main.py
```

3. Open your browser to `http://localhost:8080`

4. Upload a document and start analyzing

## Project Structure

```
local-llm-doc-assistant/
├── app/
│   ├── services/
│   │   ├── llm_service.py
│   │   └── document_processor.py
│   └── ui/
│       └── pages.py
├── config.py
├── main.py
├── requirements.txt
└── .env
```

## Configuration

Key configuration options in `.env`:

- `LM_STUDIO_API_URL`: LM Studio API endpoint
- `LM_STUDIO_MODEL`: Model identifier from LM Studio
- `APP_PORT`: Web server port
- `MAX_UPLOAD_SIZE_MB`: Maximum file size for uploads
- `SUPPORTED_FORMATS`: Comma-separated list of allowed file extensions

## Troubleshooting

**Connection Issues**
- Verify LM Studio is running with API enabled
- Check that the port 1234 is not blocked
- Confirm the model is loaded in LM Studio

**Document Processing**
- Ensure file size is within limits
- Check file format is supported
- For PDFs, verify PyPDF2 is installed correctly

## Roadmap

- Batch document processing
- Analysis history and export
- Custom analysis templates
- Multi-document comparison
- API endpoints for automation
- Additional document formats

## Technology Stack

- **Backend**: Python 3.8+
- **Web Framework**: NiceGUI
- **LLM Integration**: LM Studio API
- **Document Processing**: PyPDF2, python-docx
- **Configuration**: python-dotenv

## License

MIT License

## Contributing

Contributions are welcome. Please open an issue to discuss proposed changes before submitting a pull request.
