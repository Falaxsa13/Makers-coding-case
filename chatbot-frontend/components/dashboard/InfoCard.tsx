import { Item } from "@/index";
import { getInventory } from "@/services/backend/data";
import React from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const InfoCard = async () => {
  const response = await getInventory();
  const inventory = await response.computers;
  console.log(inventory);

  const totalProducts = inventory.length;
  const totalBrands = new Set(inventory.map((item: Item) => item.brand)).size;

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle>Total Products</CardTitle>
          <CardDescription className="text-2xl">
            {totalProducts}
          </CardDescription>
        </CardHeader>
        <CardContent></CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Total Brands</CardTitle>
          <CardDescription className="text-2xl">{totalBrands}</CardDescription>
        </CardHeader>
        <CardContent></CardContent>
      </Card>
    </>
  );
};

export default InfoCard;
