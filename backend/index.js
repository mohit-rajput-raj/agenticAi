import express from "express";
const app = express();
app.use(express.json());
app.get("/", (req, res) => {
    res.send("Backend is running");
});
app.listen(5432, () => {
    console.log("Server is running on port 5000");
});