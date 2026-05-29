# Orthocare Website

This is a Django-based website for Dr. Akhil Agnihotri's Orthopaedic Care clinic.

## Editing Website Content

You can easily edit the doctor's credentials and patient reviews without touching any HTML code. 

1. **Credentials**: Open `appointments/data/credentials.json` and edit the text inside the list.
2. **Reviews**: Open `appointments/data/reviews.json` and edit the quote, name, initial, and star rating.
3. **Contact Info & Map**: Open `appointments/data/contact.json` to change the clinic's address, phone, WhatsApp, working hours, or map link.

*Note for Map Link:* You can paste *any* standard Google Maps link (including share links like `https://maps.app.goo.gl/...`, place search URLs, or even just a plain text address like "Empire State Building, NY") into `map_link`. The website backend will resolve and embed the map automatically.

The website will automatically read these files and update the live page.

## Notification Configuration

When a patient books an appointment, the admin can receive a notification via Email, WhatsApp, or both.

### Toggling Notifications
You can switch the notification method on the fly by editing the `appointments/data/config.json` file. Set the `notification_method` to one of the following:
- `"email"` - Send an email only.
- `"whatsapp"` - Send a WhatsApp message only.
- `"both"` - Send both.

*Note: Changes to this file apply instantly without needing a server restart.*

### Setting up Environment Variables
Before notifications will send, you must copy `.env.example` to `.env` and fill in your credentials.

**For Email:**
- Provide your `SMTP_USER` and `SMTP_PASS` (if using Gmail, generate an App Password).
- Provide the `RECEIVER_EMAIL`.

**For WhatsApp:**
- Create a Meta Developer account and generate a WhatsApp App.
- Provide the `WHATSAPP_PHONE_NUMBER_ID` and a permanent `WHATSAPP_ACCESS_TOKEN`.
- Set the `ADMIN_WHATSAPP_NUMBER` (include country code, e.g., `1234567890`).

## Running the Server

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the development server:
   ```bash
   python manage.py runserver
   ```
3. Visit `http://localhost:8000/` in your browser.
