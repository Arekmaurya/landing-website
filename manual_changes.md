# Doctor Website Customization Guide

Welcome to your new Orthopaedic Specialist webpage! This document will explain how you can freely edit the website's text, images, and configuration even if you don't know much about coding. 

## Project Structure Overview
- `public/index.html` — The main structure of the page (where all text lives).
- `public/styles.css` — The styling rules (colors, fonts, sizes).
- `public/script.js` — Functionality (form submission and animations).
- `public/assets/images/` — Folder containing the background and doctor images.
- `server.js` — The backend server handling the contact form.

---

## 1. How to Change Text Elements

All text shown on the website exists within the `public/index.html` file. 

**Steps:**
1. Open `public/index.html` in an editor (like VSCode or Notepad).
2. Press `Ctrl + F` to find the text you want to change (e.g., "Dr. John Doe").
3. Delete the text and type your new text.
4. Save the file.

### Specific Examples:
- **Changing the Name:** Search for `Dr. John Doe` or `Move Freely, Live Fully.` in the `<section id="home">` and modify it.
- **Modifying Phone Number / Email:** Scroll to the bottom or search for `+1 (555) 123-4567` and `appointments@orthocare.com` and replace them with real details.
- **Updating the Working Hours:** Scroll down to the Footer section near the very end of the file.

---

## 2. How to Change Images

### Background/Hero Image
1. Prepare your new image (preferably a wide, high-resolution image).
2. Name the file `hero_bg.png` (or `.jpg`).
3. Place the file inside the `public/assets/images/` folder.
4. If it's a `.jpg`, you must open `public/styles.css`, find `.hero`, and change `.png` to `.jpg` in `background: url('assets/images/hero_bg.png')`.

### Doctor Portrait Image
1. Get an image of the doctor.
2. Name it `doctor.png`.
3. Replace the existing `doctor.png` file in the `public/assets/images/` folder.

### Specialty Icons/Images
Inside `public/index.html`, under `<section id="specialties">`, there are standard Unsplash sample images linked via URLs. 
Like this:
`src="https://images.unsplash.com/photo-..."`
You can replace that whole `http` address with local paths (like `assets/images/new_image.jpg`) or a different web address.

---

## 3. How to Change Colors

If you want the base theme color to change from Medical Blue to something else, you only need to change it in one place!

1. Open `public/styles.css`.
2. Look at the very top under `:root`.
   ```css
   :root {
       --primary-color: #0b4f6c; /* Elegant Medical Blue */
       --secondary-color: #01baef; /* Bright Teal for accents */
   }
   ```
3. Change `#0b4f6c` to any HEX code string representing the color you want. All buttons, titles, and backgrounds will automatically update to match!

---

## 4. Setting Up & Running the Site

If you want to view the website locally and test the contact form:

1. Open your terminal in the directory of this project.
2. Make sure you have downloaded all libraries:
   ```bash
   npm install
   ```
3. Start the server:
   ```bash
   node server.js
   ```
4. Open your browser and go to `http://localhost:3000`.

When users submit the contact form on that page, the backend receives the information and prints it to this terminal window. In the future, a developer can edit `server.js` to hook it up to a database or send you an email notification instead of just logging it. 
