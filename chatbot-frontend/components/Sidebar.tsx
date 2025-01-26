import Link from 'next/link'
import React from 'react'

const Sidebar = () => {
  return (
    
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
  

  )
}

export default Sidebar