# Raw ExcelFile Chatbot

A lightweight backend tool for creating and managing SQLite databases directly from raw Excel/CSV files — designed to support chatbot interactions over structured data.

---

## SQLite Database Tool

A simple Python command-line utility that allows you to:

- Create SQLite databases  
- Import CSV files as tables  
- Preview imported data

---

## Setup

```bash
# Create a virtual environment
python -m venv .venv

# Activate the environment
source .venv/bin/activate   # (use .venv\Scripts\activate on Windows)

# Install dependencies
pip install -r requirements.txt
```

Alternatively, install only pandas if you want minimal setup:
```bash
pip install pandas
```

---

## Create a Database

Create a new SQLite database file.

```bash
python db_tool.py create-db <database_name>
```

**Example:**
```bash
python db_tool.py create-db insurance.db
```

---

## Add a Table from CSV

Add a CSV file as a table to an existing SQLite database.

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

---

## Notes

- The database **must exist** before adding a table.  
- If a table already exists, it will be **replaced**.  
- The script prints a **sample of imported rows** after insertion.

---

## ADK Web Testing (Backend)

Run the chatbot web interface from the backend.

```bash
cd backend
adk web
```

Then open your local host in the browser, select **`chatbot_agent`**, and start asking questions about your imported data.

---

**Note:**  
This setup and tool are for the **backend (BE)** side only.

--- 

## FastAPI Testing (Backend)

Run the agent endpoints with FastAPI.

```bash
cd backend
uvicorn main:app --reload
```

Then open your local host in the browser, then test `/api/generate` to send request.

Example Payload:
```
{
  "session_id": "string",
  "user_id": "string",
  "input_query": "string"
}
```

To test history on the same session, use same user_id and session_id. To create new chat, use different session_id. 
Put your message in "input_query".