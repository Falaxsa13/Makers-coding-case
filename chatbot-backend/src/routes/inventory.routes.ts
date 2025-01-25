import { Router } from "express";
import { getInventory, getItemDetails } from "../services/inventory.service";

const router = Router();

router.get("/", (req, res) => {
  const inventory = getInventory();
  res.json(inventory);
});

router.get("/:brand", (req, res) => {
  const brand = req.params.brand;
  const item = getItemDetails(brand);
  if (item) {
    res.json(item);
  } else {
    res.status(404).json({ error: "Item not found" });
  }
});

export default router;
