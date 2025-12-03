🧓📞 Senior Medication Dashboard

An AI-powered, voice-first medication reminder system designed for senior citizens with a simple, accessible dashboard for caregivers.

🚀 Project Overview

Many seniors miss medications due to forgetfulness, poor vision, or complex apps. This project provides automatic voice call reminders, logs confirmations, and alerts caregivers if doses are missed.

✅ No smartphone skills required
✅ Works with any basic phone
✅ Designed with accessibility-first UX

🎯 Key Features

📞 Automated Voice Reminders via Twilio

🧠 AI-Personalised Messages using Gemini

⏰ Scheduled Daily Calls using n8n Cron

✅ Call Status Tracking (completed, missed, failed)

📊 Google Sheets Integration for live data logging

♿ Senior-Friendly UX (large fonts, minimal steps)

🚨 Caregiver Alerts on missed doses

🧰 Tech Stack

Workflow Automation: n8n

Voice Calling API: Twilio

AI Engine: Google Gemini

Database: Google Sheets

Frontend: HTML, CSS, JavaScript

Hosting: n8n Cloud / Local Server

🏗️ System Architecture

Caregiver adds senior details to Google Sheets

n8n Cron triggers at scheduled time

Gemini generates a polite reminder

Twilio makes a voice call

Call status saved to Google Sheets

If missed → caregiver gets notified

🖥️ Dashboard Features

Add senior details

Enable / Disable reminders

View daily call status

Monitor missed doses

📂 Folder Structure
/frontend
  index.html
  styles.css
/workflows
  senior-reminder.json
README.md

⚙️ Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/yourusername/senior-medication-dashboard.git

2️⃣ Configure n8n

Import workflow JSON

Add:

Twilio Credentials

Google Sheets Credentials

Gemini API Key

3️⃣ Setup Google Sheets

Columns required:

PhoneNumber | Message | ScheduledTime | CallSID | Status

4️⃣ Activate Workflow

Enable Cron Node

Timezone → Asia/Kolkata

🧪 Demo Flow

Add number + message in Google Sheets

Wait for scheduled time

Senior receives voice call

Status auto-updates

Caregiver sees result on Dashboard

📸 Demo Includes

✅ Working Dashboard

✅ Voice Call Proof

✅ Call Status Logs

✅ AI Message Generation

✅ Accessibility UI

🏆 Hackathon Value

Human-centered design

Real-world healthcare impact

Functional AI + Voice integration

Perfect for hospital & elder care deployment

🔮 Future Enhancements

Multi-language support (Telugu, Hindi, Tamil)

Emergency escalation calls

Wearable health monitoring

Family mobile app


Just tell me what you need next 🚀
