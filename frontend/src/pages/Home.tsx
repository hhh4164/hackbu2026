import { useState, type ChangeEvent } from "react"
import Card from "../components/Card"

export default function Home() {
  const [docType, setDocType] = useState("")
  const [pdfFile, setPdfFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<{issue: string; description: string}[][]>([])

  const handleFileChange = (e : ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files 
    if (files && files.length > 0) {
      setPdfFile(files[0])
    } else {
      setPdfFile(null)
    }
  }

  const analyzePdf = async () => {
    if (!pdfFile || !docType) {
      alert("Please select a document type and upload a PDF.")
      return;
    }
    setLoading(true)

    const formData = new FormData()
    formData.append("file", pdfFile)
    formData.append("type", docType)

    try {
      const response = await fetch("http://127.0.0.1:8000/audit", {
        method: "POST",
        body: formData
      })

      if (!response.ok) {
        throw new Error("Failed to analyze PDF")
      }

      const data = await response.json();
      setResult(data)
    } catch (err) {
      console.error(err)
    }

    setLoading(false);
  }

  return (
    <div className="min-h-screen max-w-6xl mx-auto p-6 mt-20">
      <header className="text-center mb-12" id="hero">
        <h1 className="text-5xl font-bold text-gray-800">ClearDocs</h1>
        <p className="text-gray-600 mt-2">
          Instantly analyze contracts and medical bills with AI.
        </p>
      </header>

      <section className="flex flex-col items-center gap-8 text-center">
        <div className="w-full max-w-md">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">
            1. Select Document Type
          </h2>

          <div className="flex justify-center gap-6">
            <label className="flex items-center gap-2">
              <input
                type="radio"
                value="contract"
                checked={docType === "contract"}
                onChange={(e) => setDocType(e.target.value)}
              />
              Contract
            </label>

            <label className="flex items-center gap-2">
              <input
                type="radio"
                value="medical"
                checked={docType === "medical"}
                onChange={(e) => setDocType(e.target.value)}
              />
              Medical Bill
            </label>
          </div>
        </div>

        <div className="w-full max-w-md">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">
            2. Upload PDF
          </h2>

          <input
            type="file"
            accept="application/pdf"
            onChange={handleFileChange}
            className="w-full border border-gray-300 rounded p-2"
          />

          <button 
          onClick={analyzePdf}
          className="mt-4 px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
            {loading ? "Analyzing..." : "Analyze PDF"}
          </button>
        </div>

        {result.length > 0 && (
          <div className="w-full max-w-4xl mt-10">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Analysis Results</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {result.map((group, i) => 
              group.map((item, j) => (
                <Card
                key={`${i}-${j}`}
                message={item.issue}
                description={item.description}
                />
              )))}
            </div>
          </div>
        )}
      </section>

      <section className="mt-12">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-10">The Problem</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card 
          message="Low Literacy Rates"
          description="Around 21% of U.S. adults struggle with literacy, making complex documents difficult to understand."
          />
          <Card
          message="Hidden Contract Risks" 
          description="Legal contracts often contain confusing clauses, hidden fees, or obligations written in complex language that many people don't fully understand before signing."
          />
          <Card
          message="Confusing Medical Bills" 
          description="Medical bills are filled with unclear codes, duplicate charges, and unexpected fees, making it difficult for patients to know what they actually owe."
          />
        </div>
      </section>

      <section className="mt-12">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-10">The Solution</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card 
          message="Scan PDFs Instantly"
          description="Upload your contracts or medical bills and ClearDocs quickly scans the entire document, making it ready for analysis."
          />
          <Card 
          message="Protect Sensitive Data"
          description="ClearDocs automatically detects and omits sensitive information like names, addresses, and IDs before any analysis, keeping your data private."
          />
          <Card 
          message="Highlight Key Issues"
          description="The AI identifies all important parts, hidden risks, or confusing clauses, so you can understand your contracts or bills at a glance."
          />
        </div>
      </section>
    </div>
  )
}