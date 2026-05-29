# Orthocare Website

This is a Django-based website for Dr. Akhil Agnihotri's Orthopaedic Care clinic.

## Editing Website Content & Settings

You can manage all of the website's content and configuration settings from a single, simple file: **`appointments/data/content.json`**.

Open `appointments/data/content.json` to edit:
1. **Credentials**: A list of strings displaying the doctor's board certifications and qualifications.
2. **Reviews**: Patient stories (including names, initials, quotes, and star ratings).
3. **Contact Info & Map**: Clinic address, phone numbers, working hours, and social media links.
   * *Note for Map Link:* You can paste *any* standard Google Maps link (including share links like `https://maps.app.goo.gl/...`, place search URLs, or even just a plain text address like "Empire State Building, NY") into `map_link`. The website backend will resolve and embed the map automatically.
4. **Notification Settings**: Under `notification_method`, you can select:
   * `"email"` - Send an email notification only.
   * `"whatsapp"` - Send a WhatsApp notification only.
   * `"both"` - Send both notifications.

*Note: Any edits made to `content.json` are applied instantly without needing a server restart.*

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
