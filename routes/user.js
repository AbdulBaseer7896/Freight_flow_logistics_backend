
const router = require("express").Router();
const bcrypt = require("bcryptjs");
const User = require("../models/user");
const jwt = require("jsonwebtoken")
const { authenticateToken } = require("./userAuth")
const Carrier = require('../models/CarrierData');  // Import the Carrier model
const ContactForm = require('../models/contactData.js');
const Contact = require('../models/ContactModel.js');
// models\contactData.js
// POST route to save the carrier data
const express = require('express');
const multer = require('multer');



// // Sign Up
// router.post("/sign-up", async (req, res) => {
//     try {
//         const { username, email, password, address } = req.body;

//         // Check username length is more than 4
//         if (username.length < 4) {
//             return res.status(400).json({ message: "Username is too short" });
//         }

//         // Check if username already exists
//         const existingUsername = await User.findOne({ username });
//         if (existingUsername) {
//             return res.status(400).json({ message: "Username already exists" });
//         }

//         // Check if email already exists
//         const existingEmail = await User.findOne({ email });
//         if (existingEmail) {
//             return res.status(400).json({ message: "Email already exists" });
//         }

//         // Check password length
//         if (password.length <= 5) {
//             return res.status(400).json({ message: "Password is too short" });
//         }

//         // Hash the password
//         const hashPass = await bcrypt.hash(password, 10);

//         // Create a new user
//         const newUser = new User({ username, email, password: hashPass, address });

//         await newUser.save();
//         return res.status(200).json({ message: "SignUp Successful" });
//     } catch (error) {
//         return res.status(500).json({ message: "Internal Server Error" });
//     }
// });


// Sign In
router.post("/sign-in", async (req, res) => {
    try {
        const { username, password } = req.body;

        // Check if the user exists
        const existingUser = await User.findOne({ username });
        if (!existingUser) {
            return res.status(400).json({ message: "Invalid credentials, user does not exist" });
        }

        // Compare passwords using bcrypt
        const isMatch = await bcrypt.compare(password, existingUser.password);
        if (isMatch) {
            const authClaims = [
                { name: existingUser.username },
                { role: existingUser.role },
            ]
            const token = jwt.sign({ authClaims }, "bookStore", { expiresIn: "30d" })
            return res.status(200).json({
                message: "SignIn Successful",
                id: existingUser._id,
                role: existingUser.role,
                token: token
            });
        } else {
            return res.status(400).json({ message: "Invalid credentials, password does not match" });
        }
    } catch (error) {
        return res.status(500).json({ message: "Internal Server Error" });
    }
});



// ger_user-information
router.get("/get-table-data", authenticateToken, async (req, res) => {
    try {
        const data = await User.findById(id).select('-password');
        return res.status(200).json(data);

    } catch (error) {
        res.status(500).json({ message: "Internal server error" })
    }
});







// ger_user-information
router.get("/get-user-information", authenticateToken, async (req, res) => {
    try {
        const { id } = req.headers;
        const data = await User.findById(id).select('-password');
        return res.status(200).json(data);

    } catch (error) {
        res.status(500).json({ message: "Internal server error" })
    }
});




const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, './uploads'); // Define where to save the file
    },
    filename: function (req, file, cb) {
        cb(null, `${file.originalname}`); // Use the name provided by the frontend
    }
});

const upload = multer({ storage: storage });




// POST route to save the carrier data
router.post('/CarrierData', upload.fields([
    { name: 'MCAuthFile' },
    { name: 'COLFile' },
    { name: 'W9File' },
    { name: 'NOVFile' },
]), async (req, res) => {
    try {
        const carrierData = JSON.parse(req.body.carrierData); // Parse the JSON string from FormData
        const { MCAuthFile, COLFile, W9File, NOVFile } = req.files;

        // Create a new carrier instance with file paths
        const carrier = new Carrier({
            ...carrierData,
            MCAuthFile: MCAuthFile[0].path, // Store the file path
            COLFile: COLFile[0].path,
            W9File: W9File[0].path,
            NOVFile: NOVFile[0].path
        });

        // Save the carrier data to the database
        await carrier.save();
        res.status(201).json({ message: 'Carrier data saved successfully!' });
    } catch (error) {
        console.error('Error saving carrier data:', error);
        res.status(500).json({ message: 'Error saving carrier data', error });
    }
});




// Example route handler
router.post('/general-contact-us', async (req, res) => {
    try {
        const formData = new ContactForm(req.body);
        await formData.save();
        res.status(201).json({ message: 'Form submitted successfully' });
    } catch (error) {
        res.status(500).json({ error: 'Server error' });
    }
});



router.post('/justcontactus', async (req, res) => {
    try {
        const { fullName, phoneNumber, email, companyName, message } = req.body;

        const newContact = new Contact({
            fullName,
            phoneNumber,
            email,
            companyName,
            message
        });

        await newContact.save();

        res.status(201).json({
            success: true,
            message: 'Contact form submitted successfully'
        });
    } catch (error) {
        console.error('Error submitting contact form:', error);
        res.status(500).json({
            success: false,
            message: 'Internal server error',
            error: error.message
        });
    }
});



router.get('/carriersData', async (req, res) => {
    try {
        const carriers = await Carrier.find().sort({ _id: -1 });  // Fetch all records from the Carrier collection
        res.status(200).json(carriers);  // Send the result as JSON
    } catch (error) {
        res.status(500).json({ message: "Error fetching data", error });
    }
});

router.get('/ContactData', async (req, res) => {
    try {
        const ContactForms = await ContactForm.find().sort({ _id: -1 });  // Fetch all records from the Carrier collection
        res.status(200).json(ContactForms);  // Send the result as JSON
    } catch (error) {
        res.status(500).json({ message: "Error fetching data", error });
    }
});


router.get('/justcontactus', async (req, res) => {
    try {
        const contact = await Contact.find().sort({ _id: -1 });  // Fetch all records from the Carrier collection
        res.status(200).json(contact);  // Send the result as JSON
    } catch (error) {
        res.status(500).json({ message: "Error fetching data", error });
    }
});

router.put('/toggleStatus/:id', authenticateToken, async (req, res) => {
    try {
        const carrier = await Carrier.findById(req.params.id);
        if (!carrier) return res.status(404).json({ message: "Carrier not found" });

        // Toggle status
        carrier.isActive = carrier.isActive === 'active' ? 'inActive' : 'active';
        await carrier.save();

        res.status(200).json({ message: "Status updated successfully", carrier });
    } catch (error) {
        res.status(500).json({ message: "Error updating status", error });
    }

});


// Add these delete routes to your existing router
// Move these delete routes outside the toggleStatus route
router.delete('/deleteCarrier/:id', authenticateToken, async (req, res) => {
    try {
        await Carrier.findByIdAndDelete(req.params.id);
        res.status(200).json({ message: "Carrier deleted successfully" });
    } catch (error) {
        res.status(500).json({ message: "Error deleting carrier", error });
    }

    router.delete('/deleteContactForm/:id', authenticateToken, async (req, res) => {
        try {
            await ContactForm.findByIdAndDelete(req.params.id);
            res.status(200).json({ message: "Contact form deleted successfully" });
        } catch (error) {
            res.status(500).json({ message: "Error deleting contact form", error });
        }
    });

});


router.delete('/deleteContact/:id', authenticateToken, async (req, res) => {
    try {
        const carrier = await Contact.findById(req.params.id);
        if (!carrier) {
            return res.status(404).json({ message: 'Carrier not found' });
        }

        // Delete database record
        await Contact.findByIdAndDelete(req.params.id);

        res.status(200).json({ message: 'Carrier deleted successfully' });
    } catch (error) {
        console.error('Delete error:', error);
        res.status(500).json({
            message: 'Error deleting carrier',
            error: error.message
        });
    }
});






module.exports = router;
