// 'use client'
import React, { useState } from 'react'
import Sidebar from './Sidebar'
import Link from 'next/link'
// import { Menu, X } from 'lucide-react'

const Navbar = () => {
    // const [sidebarOpen, setSidebarOpen] = useState(false);
  return (
    <>
        <div className="bg-foreground sticky  top-0 text-background w-full h-16 flex justify-between items-center p-4">

            <p className='italic'>Makers tech</p>
        
        <ul className='flex gap-4  justify-betweem'>
          <li>
          <Link href="/" className="block p-4 hover:bg-secondary-200">
              Chatbot
            </Link>
          </li>
          <li>
          <Link href="/dashboard" className="block p-4 hover:bg-secondary-200">
              Dashboard
            </Link>
          </li>
        </ul>
            
       </div> 

    </>
    
  )
}   

export default Navbar