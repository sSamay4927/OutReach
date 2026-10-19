# Deploying Outreach Tool to Render (100% Free, No Credit Card)

This guide walks you through deploying your Outreach Tool to Render's free tier.

---

## 🌟 What We Have Pre-Configured

1. **Unified Docker Container**:
   - The React frontend (`frontend/dist`) and Flask backend are bundled into a single web service.
   - You only need **one single Render service** (and one URL).
2. **Autonomous Background Worker**:
   - `batch_worker.py` starts automatically in the background alongside Gunicorn.
3. **HTTP Basic Auth Protection**:
   - The app has no built-in login screen. You can set `AUTH_USERNAME` and `AUTH_PASSWORD` in Render's environment variables to require a password before anyone can open the page.
4. **Zero-Sleep Keep-Alive Endpoint**:
   - `/api/health` allows free external pingers (like [cron-job.org](https://cron-job.org)) to keep your free Render instance awake 24/7 without needing authentication.

---

## 🚀 Step 1: Push Changes to GitHub

From your local project directory, commit and push the new setup:

```bash
git add .
git commit -m "Configure codebase for Render deployment"
git push origin main
```

---

## 🛠️ Step 2: Deploy on Render

1. Go to [Render.com](https://render.com) and click **Sign Up** (use your GitHub or Google account — **no credit/debit card is required**).
2. On your Render Dashboard, click **New +** and select **Web Service**.
3. Choose **Build and deploy from a Git repository**, click **Next**, and connect your GitHub repository (`outreach-tool`).
4. Configure the service settings:
   - **Name**: `outreach-tool` (or any name you choose)
   - **Region**: Choose the closest region (e.g. `Singapore`, `Frankfurt`, or `Oregon`)
   - **Language / Runtime**: **Docker**
   - **Instance Type**: **Free** ($0 / month)
5. Under **Environment Variables**, add:
   | Key | Value | Description |
   |---|---|---|
   | `AUTH_USERNAME` | `your_chosen_username` | Username to lock the UI |
   | `AUTH_PASSWORD` | `your_chosen_password` | Password to lock the UI |
   | `GMAIL_ADDRESS` | `your_email@gmail.com` | *(Optional)* Pre-fills Gmail |
   | `GMAIL_APP_PASSWORD` | `your_16_char_app_password` | *(Optional)* Pre-fills Gmail password |
   | `GROQ_API_KEY` | `gsk_...` | *(Optional)* Pre-fills primary Groq key |
   | `GEMINI_API_KEY` | `AIza...` | *(Optional)* Pre-fills Gemini key |

6. Click **Create Web Service**.

Render will now automatically:
- Download Node.js and build the React frontend.
- Install Python dependencies.
- Initialize the SQLite database.
- Start the API and the background email worker.

Once deployment finishes, Render will give you a public URL (e.g. `https://outreach-tool-xxxx.onrender.com`).

---

## ⏰ Step 3: Keep It Awake 24/7 (Prevent 15-min Sleep)

Render's free tier goes to sleep after 15 minutes of inactivity. To keep your batch worker and email monitor active 24/7:

1. Sign up for a free account at [cron-job.org](https://cron-job.org) (**100% free, no credit card**).
2. Click **Create Cronjob**:
   - **Title**: `Outreach Tool Keep-Alive`
   - **URL**: `https://<YOUR-RENDER-URL>.onrender.com/api/health`
   - **Schedule**: **Every 10 minutes**
   - **Request Method**: `GET`
3. Click **Save**.

This pings your health check every 10 minutes, keeping your Render container running around the clock!

---

## 💡 Important Note on Free Tier Storage

- On the free tier, Render uses an **ephemeral disk**. If Render restarts or you redeploy code, the database resets.
- Because we added environment variable pre-seeding, your Gmail and API keys will **never be lost** across restarts as long as you add them in the Render Environment Variables!
- When you are ready to send campaigns, upload your recipient CSV, let the worker process it, and monitor progress right from the web dashboard.
