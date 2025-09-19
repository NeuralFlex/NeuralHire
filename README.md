#NeuralHire – Internal Hiring Platform

NeuralHire is an internal recruitment platform built for NeuralFlex.
It helps the team manage job postings, candidate applications, and the full hiring pipeline without relying on paid SaaS solutions like Workable.

# Features
## Admin

Secure Admin Login & Dashboard

Create & Manage Job Postings

Title, Description, Requirements, Benefits, Location (Onsite/Hybrid/Remote)

Status (Open/Closed)

View Applications for each job

Update Pipeline Stage of candidates:

Applied → Screening → Interview → Offer → Hired/Rejected

Download Candidate Resumes

Analytics Overview (Jobs posted, Applications received, Hiring success)

## Candidate

Public Job Listings Page (no login required)

Apply to Jobs with resume upload and personal info (name, email, phone)

Automatic Application Entry into the pipeline with status = Applied

Email acknowledgment/notification (optional in later version)

## Database Design

Admin → manages jobs.

Job → stores job postings.

Candidate → stores candidate information.

Application → links candidate to job + tracks pipeline stage.

## Flow (How It Works)

Admin logs in → creates job.

Candidate visits public page → applies with resume.

Application created → enters pipeline at "Applied".

Admin reviews application → updates stage across pipeline.

Final outcome → Hired ✅ or Rejected ❌.

## Tech Stack (Planned)

Backend: Django + DRF (Python)

Frontend: React (Bootstrap / Tailwind)

Database: PostgreSQL / MySQL

## Deployment:

Backend → PythonAnywhere / Render

Frontend → Netlify / Vercel
