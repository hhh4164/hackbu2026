import { Link } from "react-router"

export default function Footer() {
  return (
    <footer className="w-full flex items-center justify-between py-4 px-6 border-t border-gray-200 shadow-sm">
      
      <Link 
        to="/" 
        className="text-gray-900 font-semibold hover:text-blue-500 transition-colors duration-300"
      >
        ClearDocs
      </Link>

      <span className="text-gray-600 text-sm">
        Built for HackBU Spring 2026
      </span>

      <a 
        href="https://github.com/hhh4164/hackbu2026"
        target="_blank"
        rel="noreferrer"
        className="text-gray-600 hover:text-blue-500 font-medium transition-colors duration-300"
      >
        GitHub
      </a>
    </footer>
  )
}