// import { AreaComponent } from "@/components/dashboard/AreaChart";
import { BarComponent } from "@/components/dashboard/Bar";
// import { AreaChart } from "lucide-react";
import React from "react";
// import { Bar } from "recharts";
// import { PieComponent } from "@/components/dashboard/Pie";
import TableComponent from "@/components/dashboard/Table";
import InfoCard from "@/components/dashboard/InfoCard";

const Dashboard = () => {
  return (
    <div className="flex flex-col  justify-center gap-5 mt-10">
      <header className="flex flex-col items-center justify-center gap-5">
        <h1 className="text-6xl font-bold">Dashboard</h1>
        <p className="text-lg">Showing data for analysis</p>
      </header>

      <div className="grid gap-5 mt-8 mx-7">
        <div className="grid md:grid-cols-2 gap-5">
          <InfoCard />
        </div>
        <div className="grid md:grid-cols-2 gap-5">
          <BarComponent type="price" />
          <BarComponent type="quantity" />
        </div>
        <div className="grid md:grid-cols-2 gap-5">
          <div>
            <h1 className="my-4 text-2xl">
              Quantity of products by brand in stock:
            </h1>
            <TableComponent type="brand" />
          </div>

          <div>
            <h1 className="my-4 text-2xl">
              Quantity of products by category in stock:
            </h1>
            <TableComponent type="category" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
