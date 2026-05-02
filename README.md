# Helping Hands - Community Lost & Found

A warm, community-driven platform to help people find their lost belongings.

## 🎯 Features

- 📝 Report Found Items
- 💔 Report Lost Items
- 🔍 Search for lost items
- 🤝 Mark items as reunited
- 📦 Archive of reunited items
- 📷 Photo upload support

## 🚀 Deployment Instructions

### Option 1: Render (Recommended - Free)

1. **Create a GitHub account** at https://github.com

2. **Push your code to GitHub:**
   - Create a new repository called "helping-hands"
   - Push your code to that repository

3. **Deploy on Render:**
   - Go to https://render.com
   - Sign up with your GitHub account
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Set:
     - **Name:** helping-hands
     - **Region:** Singapore (closest to you)
     - **Branch:** main
     - **Root Directory:** (leave empty)
     - **Runtime:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
   - Click "Create Web Service"

4. **Your site will be live at:** `https://helping-hands.onrender.com`

### Option 2: PythonAnywhere

1. **Create account** at https://www.pythonanywhere.com

2. **Upload files:**
   - Go to Files → Upload
   - Upload all your files

3. **Set up WSGI:**
   - Go to Web → Add a new web app
   - Choose Manual configuration
   - Select Python 3.9+

4. **Configure WSGI file** to point to your app

## 🛠️ Local Development

```bash
pip install flask
python app.py
```

Then visit http://localhost:5000

## 📁 Project Structure

```
helping-hands/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── lostfound.db       # SQLite database
├── static/
│   └── uploads/       # Uploaded photos
└── templates/
    ├── index.html          # Report Found page
    ├── report-lost.html    # Report Lost page
    ├── search.html         # Search page
    ├── archives.html       # Archived items
    ├── success-found.html # Success page (found)
    ├── success-lost.html   # Success page (lost)
    └── success-claimed.html # Success page (claimed)
```

## 🎨 Design

- Color scheme: Purple (#7c3aed), Lavender, Silver, White
- Font: Nunito (Google Fonts)
- Warm, community-focused design

---

Made with ♥ by the Helping Hands Community
