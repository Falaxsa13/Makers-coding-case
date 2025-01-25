import Link from 'next/link'
import React from 'react'

const Sidebar = () => {
  return (
    <nav>
    <ul>
      <li>
       <Link href="/" className="block p-4 hover:bg-gray-200">
          Chatbot
        </Link>
      </li>
      <li>
       <Link href="/dashboard" className="block p-4 hover:bg-gray-200">
          Dashboard
        </Link>
      </li>
    </ul>
  </nav>

  )
}

export default Sidebar