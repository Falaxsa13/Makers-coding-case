'use client'
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
  } from "@/components/ui/table"
import { BrandResponse, CategoriesResponse } from "@/index"
import { countProductsByBrand, countProductsByCategory } from "@/services/backend/data"

  import React, {useState, useEffect} from 'react'
  
    type TableComponentProps = {
        type: 'brand' | 'category';
    }
  const TableComponent = ({type}: TableComponentProps) => {
    const [dataBrand, setDataBrand] = useState<BrandResponse[]>([])
    const [dataCategory, setDataCategory] = useState<CategoriesResponse[]>([])

    useEffect(() => {
        const response = async () => {
           if(type === 'brand'){
            const data = await countProductsByBrand();
            setDataBrand(data)
           } else {
            const data = await countProductsByCategory();
            setDataCategory(data)
           }
        }
        response()
    }, [])

    return (
      <Table>
        
          
          
            
        
       
        <TableBody>

        {type === 'brand' ? (
            dataBrand.map((item: BrandResponse, index: number) => (
                <TableRow key={index}>
                <TableCell>{item.brand}</TableCell>
                <TableCell>{item.products}</TableCell>
                </TableRow>
            ))
            ) : (
            dataCategory.map((item: CategoriesResponse, index: number) => (
                <TableRow key={index}>
                <TableCell>{item.category}</TableCell>
                <TableCell>{item.products}</TableCell>
                </TableRow>
            ))
        )}
       </TableBody>
        </Table>
    )
  }
  
  export default TableComponent