# 🎓 Uni Papers Portal

> An AI-powered academic platform for accessing, processing, and enhancing university question papers through intelligent document analysis, automated solution generation, and watermark removal.

---

## 📖 Overview

Uni Papers Portal is a full-stack web application developed to simplify access to university examination papers while showcasing practical applications of Artificial Intelligence in academic document processing.

The platform provides students with a centralized repository of previous year question papers along with intelligent features such as AI-generated solutions and automated watermark removal.

Unlike a traditional question paper archive, the system integrates multiple AI pipelines that automate document understanding, OCR, answer generation, document reconstruction, and restoration workflows.

The project has been designed with a modular architecture where each major feature operates as an independent backend pipeline while remaining seamlessly integrated into a unified web application.

The current implementation demonstrates a complete Proof of Concept (PoC) for intelligent academic document processing and serves as a scalable foundation for future enhancements.

---

# Features

Uni Papers Portal combines a modern web application with multiple AI-powered document processing pipelines to provide a comprehensive academic resource platform for university students.

| Feature | Description |
|----------|-------------|
| 📚 Centralized Question Paper Database | Browse and access a large collection of previous year university question papers from a single platform. |
| 🔍 Advanced Search & Filtering | Quickly locate papers using Degree, Branch, Semester, Subject, Year, Month, or Subject Code filters. |
| 📄 Instant PDF Download | Download original question papers directly from the portal with a single click. |
| 🤖 AI Solution Generation | Automatically generate structured solutions for supported question papers using a multi-agent AI pipeline. |
| 🧠 3-Agent Answer Validation | Student Agent generates answers, Professor Agent evaluates quality, and only validated responses are exported. |
| 📝 Word Document Export | Generated solutions are exported as professionally formatted Microsoft Word (.docx) documents. |
| 🧹 AI Watermark Removal Pipeline | Process scanned question papers through an AI-powered document restoration pipeline to produce cleaner PDFs. |
| 🔎 OCR-Based Document Analysis | Extract textual content from scanned PDFs using Optical Character Recognition (OCR). |
| 🧩 Modular AI Processing Pipelines | Independent AI pipelines for solution generation and document restoration, making the system easy to extend and maintain. |
| 🌐 RESTful Backend APIs | Clean REST APIs for frontend communication, AI processing, and document generation. |
| 📱 Responsive User Interface | Fully responsive interface designed for desktop and mobile users. |
| ⚡ End-to-End Automation | From selecting a paper to downloading AI-generated outputs, the complete workflow is automated. |

---

## 🚀 Key Highlights

- 📚 Centralized repository of previous year university question papers.
- 🤖 AI-assisted solution generation through a multi-agent architecture.
- 🧹 Automated watermark removal and document restoration pipeline.
- 🔍 Intelligent OCR-based text extraction for scanned documents.
- 📄 Automatic Word document generation for AI-produced solutions.
- ⚙️ Modular backend architecture enabling independent AI services.
- 🌐 REST API-driven communication between frontend and backend.
- 📱 Responsive React-based user interface.
- 🏗️ Scalable project structure designed for future AI feature expansion.
- 🔄 End-to-end automated document processing workflow.

---

## 🎯 Project Objectives

The primary objectives of this project are:

- Provide students with easy access to previous year university examination papers.
- Reduce manual effort involved in searching and organizing academic resources.
- Demonstrate practical applications of Artificial Intelligence in educational technology.
- Generate structured academic solutions using an AI-driven multi-agent workflow.
- Improve the quality of scanned documents through automated watermark removal and restoration.
- Build a modular and scalable full-stack application following modern software engineering practices.
- Create a foundation for future intelligent academic assistance tools.


---

# 🏗️ System Architecture

The Uni Papers Portal follows a modular full-stack architecture where the frontend communicates with a centralized Node.js backend, which further orchestrates multiple independent AI processing pipelines.

Each AI module has been designed as a standalone processing service while remaining fully integrated into the application through REST APIs.

```text
                        ┌─────────────────────────────┐
                        │         End User            │
                        └──────────────┬──────────────┘
                                       │
                                       ▼
                     ┌──────────────────────────────────┐
                     │        React Frontend            │
                     │  (Search • Download • AI Tools) │
                     └──────────────┬───────────────────┘
                                    │ REST API
                                    ▼
                 ┌────────────────────────────────────────┐
                 │         Node.js + Express Backend      │
                 │                                        │
                 │ • Controllers                          │
                 │ • Routes                               │
                 │ • Services                             │
                 │ • API Layer                            │
                 └───────┬───────────────────────┬────────┘
                         │                       │
                         ▼                       ▼
        ┌─────────────────────────┐    ┌─────────────────────────────┐
        │ Solution Generation AI  │    │ Watermark Removal Pipeline  │
        │                         │    │                             │
        │ • OCR                   │    │ • PDF Decomposition         │
        │ • Student Agent         │    │ • Margin Cleaning           │
        │ • Professor Agent       │    │ • OCR Detection             │
        │ • Word Export           │    │ • YOLO Detection            │
        │ • JSON Output           │    │ • Restoration               │
        └──────────────┬──────────┘    │ • QA Validation             │
                       │               │ • PDF Reconstruction        │
                       ▼               └──────────────┬──────────────┘
         ┌───────────────────────────┐               │
         │ Generated Solution (.docx)│               │
         └───────────────────────────┘               ▼
                                       ┌─────────────────────────────┐
                                       │  Clean PDF Output           │
                                       └─────────────────────────────┘
```

---

## 🧩 Architecture Overview

The project is divided into three major layers:

### 🎨 Frontend Layer

Built using **React.js**, the frontend provides an intuitive interface for browsing question papers, downloading PDFs, requesting AI-generated solutions, and accessing document enhancement features.

---

### ⚙️ Backend Layer

The backend is developed using **Node.js** and **Express.js**, acting as the central communication layer between the frontend and the AI processing modules.

Responsibilities include:

- Managing REST API endpoints
- Handling user requests
- Triggering AI pipelines
- Managing file generation
- Returning downloadable outputs
- Coordinating backend services

---

### 🧠 AI Processing Layer

The AI layer consists of two independent processing pipelines:

### 🤖 Solution Generation Pipeline

Responsible for:

- OCR extraction from question papers
- Multi-agent answer generation
- Professor-based answer validation
- Structured JSON generation
- Microsoft Word document generation

---

### 🧹 Watermark Removal Pipeline

Responsible for:

- PDF decomposition
- Margin sanitization
- OCR analysis
- Watermark detection
- YOLO fallback detection
- Detection fusion
- Image restoration
- Quality assurance
- PDF reconstruction

---

## 🔄 Overall Workflow

```text
User
 │
 ▼
Search Question Paper
 │
 ▼
Download / AI Request
 │
 ▼
Frontend API Call
 │
 ▼
Node.js Backend
 │
 ├──────────────► Solution Generation Pipeline
 │                     │
 │                     ▼
 │               Generated DOCX
 │
 └──────────────► Watermark Pipeline
                       │
                       ▼
                  Clean PDF
```

---

## 🎯 Design Principles

The project has been designed around the following engineering principles:

- Modular Architecture
- Separation of Concerns
- Independent AI Pipelines
- Scalable Backend Design
- RESTful Communication
- Reusable Components
- Maintainable Code Structure
- Extensible Processing Workflows
- Future-ready AI Integration


---

# 🛠️ Technology Stack

The Uni Papers Portal is built using a modern full-stack technology stack that combines web development frameworks, AI processing libraries, OCR engines, and document processing tools to deliver an end-to-end intelligent academic platform.

---

## 🎨 Frontend

| Technology | Purpose |
|------------|---------|
| **React.js** | Component-based frontend development |
| **JavaScript (ES6+)** | Application logic and client-side functionality |
| **CSS3** | Responsive user interface styling |
| **Axios** | HTTP communication with backend APIs |
| **React Icons** | Consistent iconography across the application |

---

## ⚙️ Backend

| Technology | Purpose |
|------------|---------|
| **Node.js** | JavaScript runtime for backend services |
| **Express.js** | REST API framework and request handling |
| **Multer** | File upload and processing middleware |
| **Dotenv** | Environment variable management |
| **Child Process API** | Executes Python AI pipelines from the backend |

---

## 🤖 Artificial Intelligence

| Technology | Purpose |
|------------|---------|
| **Python** | AI pipeline development and orchestration |
| **Groq API** | Large Language Model inference |
| **Multi-Agent Architecture** | AI-based answer generation and validation |
| **Student Agent** | Generates initial solutions |
| **Professor Agent** | Reviews and validates generated answers |
| **Orchestrator Agent** | Routes questions to the most suitable LLM |

---

## 🔍 OCR & Document Intelligence

| Technology | Purpose |
|------------|---------|
| **PaddleOCR** | Optical Character Recognition for scanned PDFs |
| **YOLO (Object Detection)** | Watermark detection fallback model |
| **OpenCV** | Image preprocessing and document enhancement |
| **PDF2Image** | Converts PDF pages into images for AI processing |

---

## 📄 Document Processing

| Technology | Purpose |
|------------|---------|
| **python-docx** | Microsoft Word (.docx) generation |
| **PyMuPDF (fitz)** | PDF parsing and reconstruction |
| **Pillow (PIL)** | Image manipulation and processing |
| **JSON** | Intermediate structured document representation |

---

## 🗂️ Data Handling

| Technology | Purpose |
|------------|---------|
| **JSON Files** | AI pipeline data exchange |
| **File System Storage** | Temporary document management |
| **REST APIs** | Communication between frontend and backend |

---

## 🧰 Development Tools

| Tool | Purpose |
|------|---------|
| **Visual Studio Code** | Primary development environment |
| **Git** | Version control |
| **GitHub** | Repository hosting and collaboration |
| **Postman** | REST API testing |
| **Nodemon** | Automatic backend server restart during development |
| **npm** | JavaScript package management |
| **pip** | Python package management |
| **Python Virtual Environment (venv)** | Isolated Python dependency management |

---

## 🔄 Version Control & Collaboration

| Tool | Purpose |
|------|---------|
| **Git Branching** | Feature-based development workflow |
| **Pull Requests (PRs)** | Code review and feature integration |
| **GitHub Issues & Reviews** | Team collaboration and review process |

---

## 📦 Key Dependencies

### Frontend

- React
- Axios
- React Icons

### Backend

- Express
- Multer
- Dotenv
- Nodemon

### Python AI Pipeline

- PaddleOCR
- OpenCV
- PyMuPDF
- Pillow
- NumPy
- python-docx
- PDF2Image
- Ultralytics (YOLO)
- Groq
- Torch
- torchvision

---

## 🏛️ Technology Architecture

```text
                    Frontend
                  React.js + CSS
                        │
                        ▼
              Node.js + Express APIs
                        │
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
 Solution Generation             Watermark Removal
      (Python)                        (Python)
        │                               │
        ▼                               ▼
 Groq AI + OCR                 OCR + YOLO + OpenCV
        │                               │
        ▼                               ▼
 DOCX Solution                  Clean PDF Output
```

---

## 💡 Design Philosophy

The technology stack has been selected with a strong emphasis on modularity, scalability, maintainability, and practical AI integration.

The architecture separates the web application from the AI processing layer, allowing independent development and future enhancements without affecting the core application.

This modular approach enables new AI services to be integrated with minimal changes to the existing backend infrastructure while maintaining a clean separation of responsibilities across the system.


---

# 📁 Project Structure

The project follows a modular full-stack architecture where the frontend, backend, and AI processing pipelines are organized into independent components. This structure improves maintainability, scalability, and collaborative development.

```text
Uni Papers Portal
│
├── frontend/                 # React Frontend Application
│
├── backend/                  # Express Backend Server
│   ├── ai_pipeline/          # AI Solution Generation Pipeline
│   ├── python/               # AI Watermark Removal Pipeline
│   ├── controllers/          # Request Handlers
│   ├── routes/               # API Endpoints
│   ├── services/             # Business Logic
│   ├── utils/                # Helper Utilities
│   └── server.js             # Backend Entry Point
│
├── README.md
└── .gitignore
```

---

# 📂 Directory Breakdown

## 🎨 Frontend (`/frontend`)

Contains the complete React-based client application responsible for providing the user interface and interacting with backend APIs.

### Responsibilities

- User Interface
- Question Paper Search
- Filtering
- AI Solution Requests
- Watermark Removal Requests
- Download Management
- Responsive Design

### Important Files

| File / Folder | Purpose |
|---------------|---------|
| `src/App.jsx` | Root application component |
| `src/components/` | Reusable React UI components |
| `src/services/api.js` | Axios API configuration |
| `src/index.css` | Global Tailwind CSS styles |
| `public/` | Static assets (icons, favicon, etc.) |
| `.env.example` | Frontend environment configuration |
| `vite.config.js` | Vite build configuration |
| `tailwind.config.js` | Tailwind CSS configuration |

---

## ⚙️ Backend (`/backend`)

Acts as the central communication layer between the frontend and all AI processing pipelines.

Responsibilities include:

- REST API Management
- Request Validation
- File Processing
- AI Pipeline Invocation
- Document Download
- Service Orchestration

---

## 🛣️ Routes (`/backend/routes`)

Defines all REST API endpoints exposed by the backend.

| File | Purpose |
|------|---------|
| `paperRoutes.js` | Question paper APIs |
| `filterRoutes.js` | Search & filter APIs |
| `solutionRoutes.js` | AI Solution Generation APIs |
| `watermarkRoutes.js` | Watermark Removal APIs |

---

## 🎮 Controllers (`/backend/controllers`)

Controllers receive API requests, validate incoming data, and coordinate with backend services.

| File | Purpose |
|------|---------|
| `paperController.js` | Handles question paper requests |
| `filterController.js` | Processes filtering logic |
| `solutionController.js` | Starts AI solution generation |
| `watermarkController.js` | Starts watermark removal pipeline |

---

## ⚙️ Services (`/backend/services`)

Contains the core backend business logic.

| File | Purpose |
|------|---------|
| `solutionGenerationService.js` | Launches Python solution generation pipeline |
| `watermarkService.js` | Executes watermark removal pipeline |

Services separate business logic from API controllers, making the codebase easier to maintain and extend.

---

# 🤖 AI Solution Generation Pipeline (`/backend/ai_pipeline`)

This directory contains the complete AI-based answer generation system.

Major responsibilities include:

- OCR Processing
- Question Extraction
- Multi-Agent Orchestration
- Student Agent
- Professor Agent
- LLM Communication
- Diagram Extraction
- Word Document Generation

### Major Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point of the AI pipeline |
| `student_agent.py` | Generates initial answers |
| `professor_agent.py` | Reviews and validates answers |
| `orchestrator.py` | Routes questions to appropriate AI models |
| `llm_client.py` | Handles Groq API communication |
| `word_exporter.py` | Generates final DOCX solutions |
| `pdf_processor.py` | PDF preprocessing |
| `diagram_extractor.py` | Diagram extraction |
| `layout_detector.py` | Document layout detection |
| `extractor.py` | OCR content extraction |
| `config.py` | AI configuration |

---

# 🧹 Watermark Removal Pipeline (`/backend/python`)

Contains the complete AI-powered document restoration pipeline.

The pipeline processes scanned PDFs through multiple sequential stages.

### Processing Workflow

```text
PDF
 │
 ▼
PDF Decomposition
 │
 ▼
Margin Cleaning
 │
 ▼
OCR
 │
 ▼
Watermark Detection
 │
 ▼
YOLO Detection
 │
 ▼
Detection Fusion
 │
 ▼
Visual Restoration
 │
 ▼
Quality Assurance
 │
 ▼
Recovery
 │
 ▼
PDF Reconstruction
 │
 ▼
Clean PDF
```

### Major Files

| File | Purpose |
|------|---------|
| `run_pipeline.py` | Pipeline orchestrator |
| `stage2_decompose.py` | PDF decomposition |
| `stage3_margin_wipe.py` | Margin sanitization |
| `stage4_ocr.py` | OCR processing |
| `stage5_watermark.py` | Watermark candidate generation |
| `stage6_verify.py` | Candidate verification |
| `stage7_fallback.py` | YOLO fallback detection |
| `stage8_fusion.py` | Detection fusion |
| `stage9_restoration.py` | Image restoration |
| `stage10_qa.py` | Automated quality validation |
| `stage11_recovery.py` | Recovery mechanism |
| `stage12_reconstruct.py` | PDF reconstruction |
| `stage13_feedback.py` | Telemetry & feedback collection |
| `best.pt` | Custom YOLO model weights |

---

## 🛠️ Utilities (`/backend/utils`)

Contains helper functions used throughout the backend.

| File | Purpose |
|------|---------|
| `fileReader.js` | Reads and processes dataset files |

---

## 🔐 Environment Configuration

Both frontend and backend maintain independent environment configurations.

```text
frontend/
└── .env.example

backend/
└── .env.example
```

This separation allows developers to configure frontend and backend services independently without exposing sensitive credentials.

---

## 📦 Overall Repository Organization

The repository is intentionally divided into independent layers:

```text
Frontend
     │
     ▼
REST APIs
     │
     ▼
Express Backend
     │
 ┌───┴─────────────┐
 ▼                 ▼
Solution AI     Watermark AI
     │                 │
     └──────┬──────────┘
            ▼
      Generated Outputs
```

This modular organization allows each subsystem to evolve independently while maintaining a clean separation of concerns across the project.

---

# 🚀 Getting Started

This section provides a complete guide to setting up the Uni Papers Portal on a fresh machine.

By following the steps below, any developer should be able to clone, configure, and run the project successfully.

---

# 📋 Prerequisites

Before cloning the repository, install the following software.

| Software | Recommended Version | Required |
|-----------|--------------------|-----------|
| Git | Latest | ✅ |
| Node.js | 22 LTS (or compatible) | ✅ |
| Python | **3.11.x** | ✅ |
| Visual Studio Code | Latest | Optional |
| Poppler for Windows | Latest | ✅ |
| Microsoft Visual C++ Redistributable (x64) | Latest | ✅ |

> **Important:** Python **3.11** is strongly recommended. Newer versions such as Python 3.14 may cause compatibility issues with PyTorch and other AI libraries.

---

# 📥 Clone the Repository

```bash
git clone <repository-url>
cd uni-papers-portal
```

---

# 📦 Backend Setup

Move into the backend directory.

```bash
cd backend
```

Install all Node.js dependencies.

```bash
npm install
```

Return to the project root.

```bash
cd ..
```

---

# 🐍 Python Virtual Environment Setup

Create a dedicated virtual environment.

```bash
py -3.11 -m venv ocr_env
```

Activate it.

### Windows PowerShell

```powershell
ocr_env\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
ocr_env\Scripts\activate
```

Verify the Python version.

```bash
python --version
```

Expected output:

```text
Python 3.11.x
```

---

# 📚 Install Python Dependencies

The project contains **two independent AI pipelines**, each with its own dependency requirements.

---

## 🤖 Solution Generation Pipeline

Install the required packages.

```bash
pip install -r backend/ai_pipeline/requirements.txt
```

---

## 🧹 Watermark Removal Pipeline

Install the required packages.

```bash
pip install -r backend/python/requirements.txt
```

Depending on your internet connection, this step may take several minutes because it installs OCR, PyTorch, YOLO, OpenCV, and other AI libraries.

---

# ⚙️ Environment Configuration

Both frontend and backend require environment configuration.

---

## Backend

Copy the example environment file.

```text
backend/.env.example
        ↓
backend/.env
```

Fill in the following values.

```env
PORT=5000

ocr_api_key=

answer_gen_key1=

answer_gen_key2=

answer_gen_key3=

PYTHON_PATH=
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| PORT | Backend server port |
| ocr_api_key | OCR service API key |
| answer_gen_key1 | Primary LLM API key |
| answer_gen_key2 | Secondary LLM API key |
| answer_gen_key3 | Backup LLM API key |
| PYTHON_PATH | Path to Python executable inside the virtual environment |

Example:

```text
PYTHON_PATH=C:\Projects\uni-papers-portal\ocr_env\Scripts\python.exe
```

---

## Frontend

Copy:

```text
frontend/.env.example
        ↓
frontend/.env
```

Configuration:

```env
VITE_API_URL=http://localhost:5000/api
```

---

# 🖥️ External Software Installation

## 1. Poppler

The AI pipelines use Poppler to process PDF files.

Download and install Poppler for Windows.

After installation:

- Extract the archive.
- Locate the `bin` directory.
- Add the `bin` directory to your system **PATH**.

Alternatively, configure a Poppler path in the backend configuration if required.

---

## 2. Microsoft Visual C++ Redistributable

PyTorch requires the Microsoft Visual C++ Redistributable.

Install the latest **x64** version before running the AI pipelines.

Failure to install this dependency may result in errors similar to:

```text
WinError 1114

DLL initialization failed

Error loading c10.dll
```

---

# ▶️ Running the Project

## Step 1 — Start the Frontend

Open a terminal.

```bash
cd frontend

npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## Step 2 — Start the Backend

Open another terminal.

Activate the Python virtual environment.

```powershell
ocr_env\Scripts\Activate.ps1
```

Navigate to the backend.

```bash
cd backend
```

Start the server.

```bash
npm run dev
```

Backend runs at:

```text
http://localhost:5000
```

---

# 🌐 Default Ports

| Service | Port |
|----------|------|
| Frontend | 5173 |
| Backend | 5000 |

---

# ✅ Verifying the Installation

A successful setup should produce the following:

### Backend

```text
🚀 Server is running on port 5000
```

---

### Frontend

Vite should display something similar to:

```text
Local: http://localhost:5173
```

---

### AI Pipelines

When triggered from the application, the backend terminal should display pipeline execution logs indicating successful processing.

---

# 📂 Generated Outputs

The application generates output files during AI processing.

### Solution Generation

Generated solution documents are stored temporarily in:

```text
backend/temp/generated-solutions/
```

---

### Watermark Removal

Clean PDFs are generated inside:

```text
backend/python/final_outputs/
```

Temporary intermediate files are created during execution and are ignored by Git.

---

# 🛠️ Common Issues

## Python Version

If PyTorch fails to initialize, ensure you are using:

```text
Python 3.11
```

Avoid Python 3.14 or newer unless officially supported.

---

## DLL Initialization Error

Example:

```text
WinError 1114

Error loading c10.dll
```

Possible causes:

- Missing Microsoft Visual C++ Redistributable
- Unsupported Python version
- Corrupted PyTorch installation

---

## Poppler Not Found

If PDF processing fails:

- Verify Poppler is installed.
- Ensure the `bin` directory is available in the system PATH.

---

## Virtual Environment Not Activated

Always activate the virtual environment before running backend AI services.

Expected terminal prefix:

```text
(ocr_env)
```

---

# ✔️ First Run Checklist

Before using the application, confirm the following:

- Git repository cloned successfully
- Backend dependencies installed
- Frontend dependencies installed
- Python 3.11 virtual environment created
- Python packages installed
- Backend `.env` configured
- Frontend `.env` configured
- Poppler installed
- Microsoft Visual C++ Redistributable installed
- Frontend running on port **5173**
- Backend running on port **5000**
- AI pipelines execute without startup errors

Once all checks are complete, the Uni Papers Portal is ready for development and testing.


## 👥 Team & Contributions

This project was developed collaboratively by a multidisciplinary team, with members contributing across frontend development, backend services, AI pipelines, system integration, testing, documentation, and project coordination.

### Akshat Sharma — Technical Project Lead

* Led overall project planning, execution, and team coordination.
* Contributed to frontend development and backend integration.
* Coordinated feature integration across multiple modules.
* Reviewed pull requests and validated implementations.
* Performed end-to-end testing, debugging, and system verification.
* Managed repository workflow, branch integration, and technical documentation.
* Ensured successful integration of AI Solution Generation and Watermark Removal modules into the overall application.

---

### 👨‍💻 Team Members

* **Shriram Iyer** — AI pipeline development, backend implementation, and feature development.
* **Manish** — Watermark Removal pipeline development and backend integration.
* **Vinesh** — Watermark Removal pipeline development, testing, and implementation support.
* **Siddhesh Bagde** — Implementation support, and project collaboration.
* **Ansh** — Feature development, implementation, and testing support.
* **Kelina Vipu Valan** — Development, testing, and project collaboration.
* **Parth Tiwari** — Development support and feature implementation.


---

### 🤝 Collaboration Workflow

The project followed an industry-standard collaborative development workflow using Git and GitHub. Development was carried out through feature branches, pull requests, code reviews, testing, documentation, and continuous integration of individual modules into the main application.

# 📄 License

This project is licensed under the MIT License, allowing anyone to use, modify, and distribute the software while retaining the original copyright notice and license.

The project has been developed as part of an academic initiative for educational and research purposes. Any future commercial use or redistribution should comply with the terms of the MIT License.

For more information, see the `LICENSE` file in the repository.