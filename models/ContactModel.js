const mongoose = require('mongoose');

const contactSchema = new mongoose.Schema({
    fullName: {
        type: String,
        required: [true, 'Full name is required']
    },
    phoneNumber: {
        type: String,
        required: [true, 'Phone number is required']
    },
    email: {
        type: String,
        required: [true, 'Email is required']
    },
    companyName: {
        type: String,
    },
    message: {
        type: String,
        required: false
    }
}, { timestamps: true });


module.exports = mongoose.model('Contact', contactSchema);
