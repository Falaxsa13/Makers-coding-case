"use client"

import { TrendingUp } from "lucide-react"
import { Bar, BarChart, CartesianGrid, LabelList, XAxis, YAxis } from "recharts"

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import { useEffect, useState } from "react"
import { countProductsByBrand, countProductsByCategory, sortByPrice, sortByQuantity } from "@/services/backend/data"
import { BrandResponse, CategoriesResponse } from "@/index"



type BarComponentProps = {
  type: 'price' | 'quantity';
}

export function BarComponent({type}: BarComponentProps) {
  const [data, setData] = useState<BrandResponse[] | CategoriesResponse[]>([])

  useEffect(() => {
    const response = async () => {

      if(type === 'price'){
        const data = await sortByPrice(true);
        setData(data)
      }
      else{
        const data = await sortByQuantity(true);
        setData(data)
      }

    }
    response()
  }, [])


  
  const chartData = data.slice(0, 6);
  
  const chartConfig = {
    count: {
      label: type === 'price' ? 'Price' : 'Quantity',
      color: "hsl(var(--chart-1))",
    },
    label: {
      color: 'white'
    }
  } satisfies ChartConfig

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          {type === 'price' ? 'Products with higher price in stock' : 'Products with more items in stock'} 
        </CardTitle>
      </CardHeader>
      <CardContent>
      <ChartContainer config={chartConfig}>
          <BarChart
            accessibilityLayer
            data={chartData}
            layout="vertical"
            margin={{
              right: 16,
            }}
          >
            <CartesianGrid horizontal={false} />
            <YAxis
              dataKey="name"
              type="category"
              tickLine={false}
              tickMargin={10}
              axisLine={false}
              tickFormatter={(value) => value.slice(0, 3)}
              hide
            />
            <XAxis dataKey={type === 'price' ? 'price' : 'quantity'} type="number" hide />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent indicator="line" />}
            />
            <Bar
              dataKey={type === 'price' ? 'price' : 'quantity'}
              layout="vertical"
              fill="var(--color-count)"
              radius={4}
            >
              <LabelList
                dataKey="name"
                position="insideLeft"
                offset={8}
                className="fill-[--color-label]"
                fontSize={12}
              />
              <LabelList
                dataKey={type === 'price' ? 'price' : 'quantity'}
                position="right"
                offset={8}
                className="fill-foreground"
                fontSize={12}
              />
            </Bar>
          </BarChart>
        </ChartContainer>
      
      </CardContent>
      {/* <CardFooter className="flex-col items-start gap-2 text-sm">
        <div className="flex gap-2 font-medium leading-none">
          Trending up by 5.2% this month <TrendingUp className="h-4 w-4" />
        </div>
        <div className="leading-none text-muted-foreground">
          Showing total visitors for the last 6 months
        </div>
      </CardFooter> */}
    </Card>
  )
}
