import { Routes, Route } from "react-router"
import Home from "./pages/Home"
import Navbar from "./components/Navbar"
import Footer from "./components/Footer"

export default function App() {
  return (
    <>
    <Navbar />
    <Routes>
      <Route path="/" element={<Home />}/>
    </Routes>
    <Footer />
    </>
  )
}
