require('dotenv').config();
const express = require('express');
const cors = require('cors');
const path = require('path');
const nodemailer = require('nodemailer');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
// Parse JSON and URL-encoded bodies
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Mock database (in-memory array) to hold requested appointments
const appointments = [];

// Configure Nodemailer Transporter
const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST || 'smtp.gmail.com',
    port: process.env.SMTP_PORT || 587,
    secure: false, // true for 465, false for other ports
    auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
    }
});

// API Endpoint to handle appointment submissions
app.post('/api/appointments', async (req, res) => {
    try {
        const { firstName, lastName, email, phone, service, message } = req.body;

        // Basic validation
        if (!firstName || !lastName || !email || !phone) {
            return res.status(400).json({ error: 'Please fill in all required fields.' });
        }

        const newAppointment = {
            id: Date.now(),
            firstName,
            lastName,
            email,
            phone,
            service,
            message,
            submittedAt: new Date()
        };

        appointments.push(newAppointment);

        // Send Email Notification
        if (process.env.SMTP_USER && process.env.SMTP_PASS && process.env.RECEIVER_EMAIL) {
            try {
                await transporter.sendMail({
                    from: `"Orthocare Website" <${process.env.SMTP_USER}>`,
                    to: process.env.RECEIVER_EMAIL,
                    subject: `New Appointment Request: ${firstName} ${lastName}`,
                    text: `You have received a new appointment request.\n\nName: ${firstName} ${lastName}\nEmail: ${email}\nPhone: ${phone}\nService: ${service}\nMessage: ${message || 'None provided'}\n`,
                    html: `<h3>New Appointment Request</h3>
                           <p><b>Name:</b> ${firstName} ${lastName}</p>
                           <p><b>Email:</b> ${email}</p>
                           <p><b>Phone:</b> ${phone}</p>
                           <p><b>Service:</b> ${service}</p>
                           <p><b>Message:</b><br/>${message || 'None provided'}</p>`
                });
                console.log('Notification email sent successfully.');
            } catch (emailError) {
                console.error('Failed to send notification email:', emailError);
            }
        } else {
            console.log('Skipping email notification: Credentials not set in .env file.');
        }
        
        console.log('New Appointment Received:', newAppointment);

        return res.status(200).json({
            message: 'Appointment successfully requested! Our clinic will contact you shortly to confirm the scheduled time.',
            data: newAppointment
        });
    } catch (error) {
        console.error('Error handling appointment:', error);
        return res.status(500).json({ error: 'Internal server error. Please try again later.' });
    }
});

// Fallback route to serve index.html for any remaining requests (SPA behavior)
app.use((req, res, next) => {
    if (req.method === 'GET') {
        res.sendFile(path.join(__dirname, 'public', 'index.html'));
    } else {
        next();
    }
});

// Start Server
app.listen(PORT, () => {
    console.log(`=================================`);
    console.log(`Server is running on port ${PORT}`);
    console.log(`Visit http://localhost:${PORT}`);
    console.log(`=================================`);
});
