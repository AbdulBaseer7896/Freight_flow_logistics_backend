require("dotenv").config();
const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");
const User = require("./models/user");

async function createAdmin() {
  await mongoose.connect(process.env.URI);

  const username = "admin11";
  const email = "admin1@gamil.com";
  const password = "admin";
  const address = "HQ";

  const existing = await User.findOne({ username });
  if (existing) {
    console.log("User already exists");
    return mongoose.disconnect();
  }

  const hashPass = await bcrypt.hash(password, 10);
  const admin = new User({
    username,
    email,
    password: hashPass,
    address,
    role: "admin",
  });

  await admin.save();
  console.log("Admin created:", username);
  await mongoose.disconnect();
}

createAdmin().catch((err) => {
  console.error(err);
  mongoose.disconnect();
});