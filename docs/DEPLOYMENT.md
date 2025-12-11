# Deployment Guide

This guide covers how to deploy the ProctoriaX application to popular PaaS platforms.

## Prerequisites

1.  **Git Repository**: Ensure your code is pushed to GitHub (completed).
2.  **Configuration**: exact files `Procfile` and `requirements.txt` must act correctly (completed).

## Option 1: Render (Recommended for Free Tier)

1.  Create an account at [render.com](https://render.com).
2.  Click **New +** and select **Web Service**.
3.  Connect your GitHub repository (`jackheretoday/ProctoriaX`).
4.  **Configure the service:**
    *   **Name**: `proctoriax-platform` (or similar)
    *   **Region**: Closest to you (e.g., Singapore or Oregon)
    *   **Branch**: `main`
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn run:app`
5.  **Environment Variables**:
    *   Add `FLASK_ENV` = `production`
    *   Add `SECRET_KEY` = (generate a random string)
6.  Click **Create Web Service**.

## Option 2: Railway

1.  Create an account at [railway.app](https://railway.app).
2.  Click **New Project** -> **Deploy from GitHub repo**.
3.  Select your repository.
4.  Railway will automatically detect the `Procfile` and python requirements.
5.  Go to **Settings** -> **Variables** to add:
    *   `FLASK_ENV` = `production`
    *   `SECRET_KEY` = (random string)

## Option 3: Heroku

1.  Install Heroku CLI and login.
2.  Run:
    ```bash
    heroku create proctoriax-app
    git push heroku main
    heroku config:set FLASK_ENV=production SECRET_KEY=your_secret_key
    ```

## Local Verification

To test the production build locally:

```bash
pip install gunicorn
gunicorn run:app
```
