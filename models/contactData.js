const mongoose = require('mongoose');

const ContactFormSchema = new mongoose.Schema({
    fullName: { type: String, default: "None" },
    phoneNumber: { type: String, default: "None" },
    email: { type: String, default: "None" },
    companyName: { type: String, default: "None" },
    register: {  // Changed from 'Plan' to match frontend name
        type: String,
        enum: ["Sole Proprietor", "Partnership", "None"],
        default: "None"
    },
    message: { type: String, default: "None" },
}, {
    timestamps: true
});

// Properly export the ContactForm model
module.exports = mongoose.model('ContactForm', ContactFormSchema);