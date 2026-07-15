const mongoose = require('mongoose');

// Singleton document that stores the website's public contact information.
// The admin panel updates these values and the frontend reads them.
const siteSettingsSchema = new mongoose.Schema({
    phone: {
        type: String,
        default: "210-201-6321"
    },
    email: {
        type: String,
        default: "dispatch@freightflowsolutions.co"
    },
    address: {
        type: String,
        default: "100 Lorenz Rd, San Antonio, TX 78209"
    }
}, { timestamps: true });

module.exports = mongoose.model('SiteSettings', siteSettingsSchema);
