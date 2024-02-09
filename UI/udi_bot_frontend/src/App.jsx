import { useEffect, useState } from "react";
import "./App.css";
import lens from "./assets/lens.png";
import loadingGif from "./assets/loadingGif.gif";
import "react-pdf/dist/esm/Page/TextLayer.css";
import { Document, Page, pdfjs } from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

export default function App() {
    const [prompt, updatePrompt] = useState(undefined);
    const [loading, setLoading] = useState(false);
    const [answer, setAnswer] = useState(undefined);
    const [pdfSource, setPdfSource] = useState('')
    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1);

    const handlePdfRender = () => {
        if (answer) {
            setShowPDF(true);
        }
    };

    const handlePdfHide = () => {
        setShowPDF(false);
    };


    const onDocumentLoadSuccess = ({ numPages }) => {
        setNumPages(numPages);
    };
    const [showPDF, setShowPDF] = useState(false);

    // const [showPDF, setShowPDF] = useState(answer !== undefined);

    const goToPrevPage = () => {
        setPageNumber((prevPage) => Math.max(prevPage - 1, 1)); // Limit to not go below page 1
    };

    const goToNextPage = () => {
        setPageNumber((prevPage) => Math.min(prevPage + 1, numPages)); // Limit to not go above numPages
    };


    useEffect(() => {
        if (prompt != null && prompt.trim() === "") {
            setAnswer(undefined);
        }
    }, [prompt]);

    const sendPrompt = async (event) => {
        if (event.key !== "Enter") {
            return;
        }

        try {
            setLoading(true);
            const formData = new FormData();
            formData.append("query", JSON.stringify(prompt));
            const requestOptions = {
                method: "POST", body: formData,
            };
            const res = await fetch("/api/generate", requestOptions)
            if (!res.ok) {
                throw new Error(res.toString());
            }
            const msg_with_source = await res.json();
            console.log(msg_with_source)
            // Extract the source and page information
            const sourceRegex = /Source: \{'source': '([^']+)', 'page': (\d+)\}/;
            const sourceMatch = msg_with_source.match(sourceRegex);

            let pdf_source = '';
            let page = '';

            if (sourceMatch) {
                pdf_source = sourceMatch[1]; // This will be your source string
                page = sourceMatch[2]; // This will be your page string
                setPdfSource(pdf_source)
                setPageNumber(parseInt(page))
            }

            // Remove the 'Source' line from the message
            const message = msg_with_source.replace(sourceRegex, '');
            // console.log(message);
            // console.log(`Source: ${pdf_source}`);
            // console.log(`Page: ${page}`);

            setAnswer(message);
        } catch (err) {
            console.error(err, "err");
        } finally {
            setLoading(false);
        }
    };

    return (<div className="screen">
        <div className="navbar">Navbar content here</div>
        <div className="app">
            <div className="app-container">
                <div className="spotlight__wrapper">
                    <input
                        type="text"
                        className="spotlight__input"
                        placeholder="Ask me anything..."
                        disabled={loading}
                        style={{
                            backgroundImage: loading ? `url(${loadingGif})` : `url(${lens})`,
                        }}
                        onChange={(e) => updatePrompt(e.target.value)}
                        onKeyDown={(e) => sendPrompt(e)}
                    />
                    <div className="spotlight__answer">
                        {answer && (
                            <p dangerouslySetInnerHTML={{ __html: JSON.parse(JSON.stringify(answer)).replace(/\n/g, '<br />') }} />
                        )}
                    </div>
                    {answer && !showPDF && (
                        <div className="pdf-toggle-button">
                            <button onClick={handlePdfRender}>Show PDF</button>
                        </div>
                    )}
                </div>
            </div>
        </div>
        {showPDF && (
            <div className="pdf-renderer">
                <div>
                    <Document
                        file={pdfSource}
                        onLoadSuccess={onDocumentLoadSuccess}
                    >
                        <Page pageNumber={pageNumber} renderAnnotationLayer={false} renderTextLayer={false} width={700} />
                    </Document>
                </div>

                <p>
                    Page {pageNumber} of {numPages}
                </p>
                <nav className="nav">
                    <button onClick={goToPrevPage}>Prev</button>
                    <button onClick={goToNextPage}>Next</button>
                </nav>
                <div className="pdf-toggle-button">
                    <button onClick={handlePdfHide}>Hide PDF</button>
                </div>
            </div>
        )}
    </div>
    );
}

function PdfRender() {
    return <div className={"pdf-renderer"}></div>
}