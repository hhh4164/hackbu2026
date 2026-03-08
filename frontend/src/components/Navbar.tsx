import { Link } from "react-router"

export default function Navbar() {
  return (
    <nav className="w-full flex items-center justify-between py-3 px-6 sticky top-0 bg-white border-b border-gray-200 shadow-sm z-50">
      
      <Link 
        to="/" 
        className="text-2xl font-semibold text-gray-900 hover:text-blue-500 transition-colors duration-300"
        >
          ClearDocs
      </Link>

      <a 
        href="https://github.com/hhh4164/hackbu2026"
        target="_blank"
        rel="noreferrer"
        className="text-gray-600 hover:text-blue-500 font-medium transition-colors duration-300"
      >
        GitHub
      </a>
    </nav>
  )
}