import { AreaComponent } from "@/components/dashboard/AreaChart";
import { BarComponent } from "@/components/dashboard/Bar";
// import { AreaChart } from "lucide-react";
import React from "react";
// import { Bar } from "recharts";

const Dashboard = () => {
  return (
    <div className="flex flex-col items-center justify-center gap-5">
      <header className="flex flex-col items-center justify-center gap-5">
      <h1 className="text-6xl font-bold">Dashboard</h1>
      <p className="text-lg">Showing data for analysis</p> 
      </header>
    
    <div className="grid gap-5 md:grid-cols-2 mt-8 mx-7">
        <BarComponent />
        <AreaComponent />
           
    </div>  
    </div>
  );
};

export default Dashboard;