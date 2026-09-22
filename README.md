# Task Management Application

A simple, production-ready task management application built with React, Flask, Supabase, and Google APIs.

## Architecture & Tech Stack
- **Frontend:** React + Vite (deployed on Netlify)
- **Backend:** Python Flask (deployed on Render)
- **Database:** Supabase (PostgreSQL)
- **Authentication:** Google OAuth 2.0
- **Email Notifications:** Gmail API

## Features
- Google Login (No password required)
- Dashboard to view tasks assigned to you or created by you
- Create and assign tasks to other registered users
- Mark tasks as completed
- Email notifications sent via Gmail API:
  - When a task is assigned to a user
  - When a task is marked as completed

## Database Schema (Supabase)

You must create the following tables in your Supabase project using the SQL Editor:

```sql
-- Create Users Table
CREATE TABLE users (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  google_id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_picture TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create Tasks Table
CREATE TABLE tasks (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  created_by UUID REFERENCES users(id) ON DELETE CASCADE,
  assigned_to UUID REFERENCES users(id) ON DELETE CASCADE,
  status TEXT DEFAULT 'Pending' CHECK (status IN ('Pending', 'Completed')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);
```

---

## Local Setup

### 1. Supabase Setup
1. Create a free Supabase project at [supabase.com](https://supabase.com).
2. Go to the SQL Editor and run the schema queries above.
3. Go to Project Settings -> API and copy the **Project URL** and **anon/service_role key**.

### 2. Google OAuth (Frontend)
1. Go to [Google Cloud Console](https://console.cloud.google.com).
2. Create a new project.
3. Configure the OAuth Consent Screen.
4. Go to Credentials -> Create Credentials -> OAuth Client ID (Web Application).
5. Add `http://localhost:5173` to Authorized JavaScript origins.
6. Copy the **Client ID**.

### 3. Gmail API Setup (Backend)
1. In the same Google Cloud Console project, enable the **Gmail API**.
2. Go to Credentials -> Create Credentials -> OAuth Client ID (Desktop App).
3. Download the JSON file, rename it to `credentials.json`, and place it in the `backend/` folder.
4. Run the auth script to generate a token:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python generate_gmail_token.py
   ```
5. A browser window will open asking you to log in and grant Gmail send permissions. After accepting, a `token.json` file will be generated. 
6. For production deployment, you will copy the contents of `token.json` and set it as the `GMAIL_TOKEN_JSON` environment variable in Render.

### 4. Running the Backend (Flask)
1. In the `backend/` directory, copy `.env.example` to `.env`.
2. Fill in the values for `SUPABASE_URL` and `SUPABASE_KEY`.
3. Start the server:
   ```bash
   python app.py
   ```
   *The backend will run on http://localhost:5000*

### 5. Running the Frontend (React)
1. In the `frontend/` directory, copy `.env.example` to `.env.local`.
2. Fill in the values for `VITE_API_URL` (default is `http://localhost:5000`) and `VITE_GOOGLE_CLIENT_ID`.
3. Start the frontend:
   ```bash
   npm install
   npm run dev
   ```
   *The frontend will run on http://localhost:5173*

---

## Deployment Steps

### Backend (Render)
1. Push the `backend/` folder to a GitHub repository.
2. Sign in to Render (render.com) and create a new **Web Service**.
3. Connect your repository and select the `backend` folder as the Root Directory.
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `gunicorn app:app`
6. Add the following Environment Variables:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `GMAIL_TOKEN_JSON` (Paste the exact raw JSON content from your local `token.json` file)
7. Deploy. Copy the production URL (e.g., `https://my-flask-api.onrender.com`).

### Frontend (Netlify)
1. Push the `frontend/` folder to GitHub.
2. Sign in to Netlify (netlify.com) and create a new Site from GitHub.
3. Select the `frontend` folder.
4. Set Build Command: `npm run build`
5. Set Publish Directory: `dist`
6. Add Environment Variables:
   - `VITE_API_URL` (Set to your Render backend URL)
   - `VITE_GOOGLE_CLIENT_ID`
7. Deploy.

**Important Note for Google OAuth in Production:**
After deploying to Netlify, go back to your Google Cloud Console and add your Netlify URL (e.g., `https://my-app.netlify.app`) to the **Authorized JavaScript origins** for your OAuth Client ID!
