require("dotenv").config();
require("./conn");
const cors = require('cors');

const express = require("express");
const User = require("./routes/user");
const MCnumber = require("./routes/mcNumber");
const test = require("./routes/test");

const app = express();


// const cors = require('cors');
// app.use(cors());
// app.use(cors());
app.use(cors({
  // origin: ['https://freightflowsolutions.co','https://dispatchingllc.netlify.app' , 'https://freightflowlogistics.netlify.app'], // Your React app's origin
  // origin: 'https://freightflowlogistics.netlify.app', // Your React app's origin
  origin: 'http://localhost:3000', // Your React app's origin
  // credentials: true
}));


// app.use((req, res, next) => {
//   res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
//   next();
// });

app.use('/uploads', express.static('uploads'));


app.use(express.json());
app.use("/api/v1", User);
app.use("/api/v1", MCnumber);
app.use("/api/v1", test);

// app.listen(process.env.PORT, () => {
//   console.log(`Server Started on port ${process.env.PORT}`);
// });


const PORT = process.env.PORT || 3002;
app.listen(PORT, () => {
    console.log(`Proxy server running on port ${PORT}`);
});