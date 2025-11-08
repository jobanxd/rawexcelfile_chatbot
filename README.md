# Raw ExcelFile Chatbot

A full-stack conversational AI application that allows users to interact with structured data from Excel/CSV files through a modern chat interface. Built with FastAPI (backend) and React (frontend).

---

## 🌟 Features

- 📊 Import Excel/CSV files into SQLite databases
- 💬 Natural language queries over your data using AI
- 🎨 Modern, sleek chat interface with gradient design
- 🔄 Session management for conversation history
- ⚡ Real-time streaming responses

---

## 🏗️ Architecture

**Backend (Python/FastAPI):**
- Google ADK Agent for natural language processing
- SQLite for data storage
- FastAPI for REST API endpoints

**Frontend (React/Vite):**
- React with modern hooks
- Tailwind CSS for styling
- Axios for API communication

---

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

---

## 🚀 Setup Instructions

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate (macOS/Linux)
   source .venv/bin/activate

   # Activate (Windows)
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your database (optional):**
   ```bash
   # Create a new database
   python db_tool.py create-db insurance.db

   # Import CSV files as tables
   python db_tool.py add-table insurance_policies.csv insurance.db
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

---

## 🎮 Running the Application

### Option 1: Full Stack (Recommended)

You need **two terminal windows** to run both backend and frontend simultaneously.

**Terminal 1 - Backend:**
```bash
cd backend
source .venv/bin/activate  # Activate virtual environment
uvicorn main:app --reload
```
Backend will run on: `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Frontend will run on: `http://localhost:5173`

**Open your browser and go to:** `http://localhost:5173`

---

### Option 2: Backend Only (Testing with ADK Web UI)

For quick backend testing without the frontend:

```bash
cd backend
source .venv/bin/activate
adk web
```

Open the ADK web interface, select **`chatbot_agent`**, and start querying your data.

---

### Option 3: Backend Only (Testing with API Docs)

Test the API endpoints directly using FastAPI's interactive documentation:

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

Open: `http://localhost:8000/docs`

Test the `/api/chatbot/generate` endpoint with this payload:
```json
{
  "session_id": "session_123",
  "user_id": "user_001",
  "input_query": "Show me all insurance policies"
}
```

---

## 🗄️ Database Management

### Create a Database

```bash
python db_tool.py create-db <database_name>
```

**Example:**
```bash
python db_tool.py create-db insurance.db
```

### Add a Table from CSV

```bash
python db_tool.py add-table <csv_file> <database_name> [--table <table_name>]
```

**Examples:**
```bash
# Use CSV filename as table name
python db_tool.py add-table insurance_policies.csv insurance.db

# Specify a custom table name
python db_tool.py add-table insurance_claims.csv insurance.db --table claims
```

**Notes:**
- Database must exist before adding tables
- If a table already exists, it will be replaced
- Sample rows are displayed after import

---

## 💬 Using the Chat Interface

1. **Start a new conversation:**
   - Click the **"+ New Chat"** button to create a fresh session
   
2. **Ask questions about your data:**
   - "Show me all insurance policies"
   - "How many active policies do we have?"
   - "List all cancelled policies"
   - "What's the average premium amount?"

3. **Session Management:**
   - Each session maintains conversation history
   - Use the same `session_id` to continue a conversation
   - Create a new session to start fresh

---

## 🔧 Configuration

### Backend Configuration

- **Database location:** Configured in agent setup
- **API Port:** Default `8000` (change in `uvicorn` command)
- **CORS:** Configured to allow `localhost:5173`

### Frontend Configuration

- **API Endpoint:** `http://localhost:8000` (in `src/App.jsx`)
- **Dev Server Port:** Default `5173` (configurable in `vite.config.js`)

---

## 📁 Project Structure

```
rawexcelfile_chatbot/
├── backend/
│   ├── chatbot_agent/        # Agent logic and tools
│   ├── routers/              # API route handlers
│   ├── models/               # Request/response models
│   ├── main.py               # FastAPI application
│   ├── db_tool.py            # Database CLI utility
│   └── requirements.txt      # Python dependencies
│
└── frontend/
    ├── src/
    │   ├── App.jsx           # Main React component
    │   ├── index.css         # Global styles
    │   └── main.jsx          # React entry point
    ├── package.json          # Node dependencies
    └── vite.config.js        # Vite configuration
```

---

## 🐛 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError`
```bash
# Make sure virtual environment is activated and dependencies installed
pip install -r requirements.txt
```

**Problem:** Port 8000 already in use
```bash
# Use a different port
uvicorn main:app --reload --port 8001

# Don't forget to update the frontend API URL in src/App.jsx
```

### Frontend Issues

**Problem:** `Cannot connect to backend`
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in backend
- Verify API URL in `src/App.jsx`

**Problem:** Styling not working
```bash
# Make sure Tailwind CSS is properly installed
npm install -D tailwindcss postcss autoprefixer @tailwindcss/postcss
```

**Problem:** White screen after sending message
- Check browser console for errors (F12)
- Verify react-markdown is installed: `npm install react-markdown`

---

## 🎨 Frontend Features

- **iMessage-style animations:** Messages bubble up smoothly from the input box
- **Thinking indicator:** Animated "Thinking..." text while waiting for responses
- **Markdown support:** Rich text formatting in bot responses
- **Session display:** Current session ID visible in the header
- **Gradient design:** Modern purple-pink gradient theme with glassmorphism

---

## 📝 API Endpoints

### POST `/api/chatbot/generate`

Send a message to the chatbot and get a response.

**Request Body:**
```json
{
  "session_id": "string",
  "user_id": "string", 
  "input_query": "string"
}
```

**Response:**
```json
{
  "response": "string"
}
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 🆘 Support

For issues and questions:
- Check the troubleshooting section above
- Review the API documentation at `http://localhost:8000/docs`
- Open an issue on the repository

---

**Happy Chatting! 🚀**