# Doctor Website Customization Guide

Welcome to the Django-based Orthopaedic Specialist website! Since the backend was migrated to Django, you no longer need to edit HTML files to change text, configurations, or images. You can manage everything through a visual admin interface!

## Project Structure Overview
- `appointments/templates/index.html` — The template structure of the page.
- `appointments/static/css/styles.css` — The styling rules (colors, fonts, sizes).
- `appointments/static/js/script.js` — Client-side interaction (validations, animations, lightboxes).
- `appointments/models.py` — Database schema/structure.
- `orthocare_project/settings.py` — Core Django configuration.

---

## 1. How to Customize Text & Config via Django Admin

Instead of modifying code, you can use the built-in Django Admin portal.

1. **Start the server:** `python manage.py runserver`
2. **Create an admin user (first time only):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to enter a username, email, and password.
3. **Log in:** Open `http://127.0.0.1:8000/admin/` in your browser and enter your credentials.
4. **Customizations:**
   * **Clinic Information:** Edit the single configuration entry to update the phone numbers, address, working hours, social media links, notification methods (Email, WhatsApp, or both), Google Map links, and the main doctor's profile image.
   * **Credentials:** Add, edit, or reorder the doctor's board certifications and qualifications.
   * **Reviews:** Manage patient reviews, star ratings, quotes, and upload patient photos (avatars) directly.

---

## 2. Dynamic Google Maps Embed
You can paste *any* standard Google Maps address, query, or share link into the `map_link` field in the Admin dashboard:
* **Short links:** `https://maps.app.goo.gl/xxxx`
* **Direct queries:** `Empire State Building, NY` or `1600 Amphitheatre Pkwy, Mountain View, CA`
The backend automatically resolves the address and generates a fully interactive, responsive map frame.

---

## 3. How to Customize Styles (Colors, Fonts)

To modify the theme colors, font choices, or sizing:

1. Open `appointments/static/css/styles.css`.
2. Locate the `:root` element at the top:
   ```css
   :root {
       --primary-color: #0b4f6c; /* Elegant Medical Blue */
       --secondary-color: #01baef; /* Bright Teal Accent */
       --transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
       ...
   }
   ```
3. Change the Hex color code (e.g., `#0b4f6c`) to your preference. The entire site (buttons, background accents, icons) will instantly update.

---

## 4. Local Setup & Testing

If you want to run the project locally and test forms/notifications:

1. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Apply migrations & seed default data:**
   ```bash
   python manage.py migrate
   python manage.py seed_content   # Optional: Seeds default content if database is empty
   ```
3. **Environment Setup:**
   * Copy `.env.example` to `.env`.
   * Configure SMTP settings for email notifications or WhatsApp API details for instant text notifications.
4. **Run Server:**
   ```bash
   python manage.py runserver
   ```
5. **View Website:** Visit `http://127.0.0.1:8000/` in your browser.
