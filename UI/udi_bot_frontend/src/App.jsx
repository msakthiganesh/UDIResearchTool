import {useEffect, useState} from "react";
import "./App.css";
import lens from "./assets/lens.png";
import loadingGif from "./assets/loadingGif.gif";
import "react-pdf/dist/esm/Page/TextLayer.css";
import {Document, Page, pdfjs} from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

export default function App() {
    const [prompt, updatePrompt] = useState(undefined);
    const [loading, setLoading] = useState(false);
    const [answer, setAnswer] = useState(undefined);

    const [showPDF, setShowPDF] = useState(undefined)
    const handlePdfRender = () => {
        setShowPDF(true);
    };

    const handlePdfHide = () => {
        setShowPDF(false);
    };
    const [numPages, setNumPages] = useState(null);
    const [pageNumber, setPageNumber] = useState(1);

    const onDocumentLoadSuccess = ({numPages}) => {
        setNumPages(numPages);
    };

    const goToPrevPage = () => setPageNumber((prevPage) => prevPage - 1);
    const goToNextPage = () => setPageNumber((prevPage) => prevPage + 1);


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
            const message = await res.json();
            setAnswer(message);
        } catch (err) {
            console.error(err, "err");
        } finally {
            setLoading(false);
        }
    };

    return (<div className="screen">
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
                        <div className="spotlight__answer">{answer && <p>{answer}</p>}</div>
                    </div>
                </div>
            </div>

            {showPDF ? (<div className="pdf-renderer">
                    <nav>
                        <button onClick={goToPrevPage}>Prev</button>
                        <button onClick={goToNextPage}>Next</button>
                    </nav>
                    <div>
                        <Document
                            file="./datastore/UDI Philippines Strategic Intelligence report_v2.3.pdf"
                            onLoadSuccess={onDocumentLoadSuccess}
                        >
                            <Page pageNumber={pageNumber} renderAnnotationLayer={false} renderTextLayer={false}/>
                        </Document>
                    </div>

                    <p>
                        Page {pageNumber} of {numPages}
                    </p>
                    <button onClick={handlePdfHide}>Hide PDF</button>
                </div>) : (<button onClick={handlePdfRender}>Show PDF</button>)}


        </div>

    );
}

function PdfRender() {
    return <div className={"pdf-renderer"}></div>
}

// export default App;