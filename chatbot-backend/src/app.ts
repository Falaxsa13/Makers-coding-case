import express from "express";
import cors from "cors";
import { Server } from "socket.io";
import http from "http";
import inventoryRoutes from "./routes/inventory.routes";

const app = express();
const server = http.createServer(app);
const io = new Server(server, { cors: { origin: "*" } });

app.use(cors());
app.use(express.json());
app.use("/api/inventory", inventoryRoutes);

// Socket.io for real-time communication
io.on("connection", (socket) => {
  console.log("A client connected");

  // Handle messages from the frontend
  socket.on("chat message", (msg) => {
    console.log("Message received:", msg);

    // Example: Respond with an inventory update
    const inventory = require("./data/inventory.json");
    socket.emit(
      "bot message",
      `We currently have ${inventory.computers.length} computers in stock.`
    );
  });

  socket.on("disconnect", () => {
    console.log("A client disconnected");
  });
});

const PORT = 3000;
server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
