# Orthocare Website - Technical Overview & Implementation Plan

## 1. Project Overview
The Orthocare website is a modern, responsive landing page designed for an orthopedic or medical clinic (featuring Dr. Akhil Agnihotri). It provides patients with essential clinic details, specialty options, and dynamic patient reviews, while offering a seamless way to request appointments online.

## 2. Technology Stack
The project utilizes a clean, scalable Django-based Python backend, removing frontend framework overhead while keeping content fully dynamic.

### Frontend
* **HTML5:** Semantic structure for accessibility and SEO.
* **CSS3:** Custom styling for a responsive, modern, and clean user interface, featuring elegant dark modes, micro-animations, and a media lightbox.
* **Vanilla JavaScript:** Handles client-side interactivity, scroll animation triggers, image lightbox modals, and asynchronous JSON-based API requests to the backend.

### Backend (Django)
* **Python & Django:** A robust framework for routing, template rendering, and database integration.
* **Django Admin:** Provides a secure, user-friendly CMS panel to manage clinic configurations, social media links, doctor portrait images (with live previews), patient credentials, and reviews.
* **SQLite:** Local relational database storing clinic settings, credentials, patient testimonials, and appointment records.
* **Pillow:** Image manipulation library to handle profile and review image uploads.
* **Requests:** Used for dispatching notification webhooks to the WhatsApp Business API.
* **Python-dotenv:** Manages sensitive environment variables (such as SMTP and WhatsApp tokens) securely.

## 3. Key Features & Functions
* **Responsive Design:** Fully optimized across all screen sizes (mobile, tablet, desktop).
* **Django Admin Panel (CMS):** A secure dashboard to manage website copy, social links, credentials, and testimonial reviews with direct image uploading.
* **Live File Upload Validation:** Validates doctor and patient photo extensions (.jpg, .png, .webp) and files sizes (max 2 MB) both on the client side (live preview) and server side.
* **Appointment Booking System:** Allows patients to fill out a reservation form (Name, Age, Sex, and Contact Number).
* **Automated Admin Notifications:** Once an appointment is saved to the database:
  - **Email:** Dispatches email summaries to the clinic admin using Django's SMTP backend.
  - **WhatsApp:** Sends instant message notifications to the admin using the Meta WhatsApp Business API.
  - Both notification modes can be enabled or toggled dynamically in the admin panel.
* **Interactive Lightbox:** Clicking a patient review avatar smoothly expands it in a modern overlay with blur backdrops and escape-key handling.

## 4. System Architecture
1. **Dynamic Homepage (`/`):** The home view retrieves the singleton `ClinicInformation` settings, `Credential` list, and `Review` set from SQLite and renders them into the custom HTML template.
2. **API Endpoint (`POST /api/appointments`):**
   * Receives JSON payload from the frontend.
   * Validates structure, age ranges (1–120), and sex choices.
   * Creates an `Appointment` record in SQLite.
   * Pulls notification preferences from `ClinicInformation` and sends emails/WhatsApp alerts if credentials are configured.
   * Returns a JSON confirmation message to the frontend.

## 5. Deployment & Maintenance
* **Environment variables:** Use a `.env` file to manage secret keys, debug modes, SMTP servers, and API tokens.
* **Media Serving:** Uploaded files are served securely via `/media/` paths, linked with development fallbacks.

---
*Updated for Django/Python architecture.*
