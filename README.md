# Orthocare Website

This is a Django-based website for Dr. Akhil Agnihotri's Orthopaedic Care clinic, featuring dynamic content management, real-time validations, and automatic notification dispatching.

## Editing Website Content & Settings

All of the website's content, text, doctor profile images, patient reviews, credentials, and configuration settings are stored in the SQLite database and can be managed visually from the **Django Admin Panel** (`/admin/`).

To customize settings:
1. **Access the Admin:** Open `http://localhost:8000/admin/` in your browser.
2. **Authenticate:** Log in using your admin superuser account (see setup steps below).
3. **Manage Content:**
   * **Clinic Information:** Update address, phone numbers, WhatsApp contacts, social links, and upload/preview the doctor's profile picture.
   * **Credentials:** Add or reorder professional certifications.
   * **Testimonials:** Manage patient reviews, star ratings, and upload patient photos (avatars) which support a fallback to initials and an interactive lightbox.
   * **Notification preferences:** Choose to send appointment notifications to the admin via email, WhatsApp, or both.

---

### Setting up Environment Variables

Before notifications will send, you must copy `.env.example` to `.env` and fill in your credentials.

**For Email:**
- Provide your `SMTP_USER` and `SMTP_PASS` (if using Gmail, generate an App Password).
- Provide the `RECEIVER_EMAIL`.

**For WhatsApp:**
- Create a Meta Developer account and generate a WhatsApp App.
- Provide the `WHATSAPP_PHONE_NUMBER_ID` and a permanent `WHATSAPP_ACCESS_TOKEN`.
- Set the `ADMIN_WHATSAPP_NUMBER` (include country code, e.g., `1234567890`).

---

## Local Setup & Development

1. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```
3. **Create an Admin account:**
   ```bash
   python manage.py createsuperuser
   ```
4. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
5. **Visit the page:** Go to `http://localhost:8000/` in your browser.

## Running Tests
To run the comprehensive test suite (which tests views, models, API logic, validations, and notifications):
```bash
python manage.py test
```
