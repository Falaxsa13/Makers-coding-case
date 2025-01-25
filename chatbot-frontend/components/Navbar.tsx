'use client'
import React, { useState } from 'react'
import Sidebar from './Sidebar'
import { Menu, X } from 'lucide-react'

const Navbar = () => {
    const [sidebarOpen, setSidebarOpen] = useState(false);
  return (
    <>
        <div className="flex md:hidden">
        <button
         onClick={() => setSidebarOpen(!sidebarOpen)}
          className="p-2 m-2 focus:outline-none focus:ring"
        >
          {sidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>
      <div
        className={`fixed inset-0 z-40 md:hidden bg-black bg-opacity-50 transition-opacity ${
          sidebarOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
        onClick={() => setSidebarOpen(false)}
      >
        <div
          className={`absolute top-0 left-0 w-64  shadow-md transition-transform transform ${
            sidebarOpen ? 'translate-x-0' : '-translate-x-full'
          }`}
          onClick={(e) => e.stopPropagation()}
        >
          <Sidebar />
        </div> 
       </div> 

    </>
    
  )
}   

export default Navbar