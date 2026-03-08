import { useState } from "react"

export default function Home() {
  const [docType, setDocType] = useState("")
  const [pdfFile, setPdfFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState({ issue: "", description: "" })

  const handleFileChange = (e) => {
    setPdfFile(e.target.files?.[0] || null)
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
    } catch (err) {
      console.error(err)
    }

    setLoading(false);
  }

  return (
    <div className="min-h-screen max-w-6xl mx-auto p-6 mt-20">
      <header className="text-center mb-12">
        <h1 className="text-5xl font-bold text-gray-800">ClearDocs</h1>
        <p className="text-gray-600 mt-2">
          Instantly analyze contracts and medical bills with AI.
        </p>
      </header>

      <section className="flex flex-col items-center gap-8 text-center">
        {/* Document Type */}
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
      </section>
    </div>
  )
}