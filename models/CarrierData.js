const mongoose = require('mongoose');

const CarrierDataSchema = new mongoose.Schema({
    MC: { type: String, default: "None" },
    Email: { type: String, default: "None" },
    Legal_Name: { type: String, default: "None" },
    Phone: { type: String, default: "None" },
    USDOT_Number: { type: String, default: "None" },
    Physical_Address: { type: String, default: "None" },
    plan: { type: String, default: "None" },
    // Mailing_Address: { type: String, default: "None" },
    signature: { type: String, default: "None" },
    MCAuthFile: { type: String, default: "None" },  // Field for MC Authority file path
    COLFile: { type: String, default: "None" },      // Field for Certificate of Liability file path
    W9File: { type: String, default: "None" },       // Field for W9 file path
    NOVFile: { type: String, default: "None" },
    isActive: {
        type: String,
        enum : ["active" , "inActive"],
        default: "active"
    }       // Field for Notice of Violation file path
}, {
    timestamps: true // This enables `createdAt` and `updatedAt` fields
});

// Properly export the Carrier model
module.exports = mongoose.model('Carrier', CarrierDataSchema);
