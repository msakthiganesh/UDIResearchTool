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
    const [pdfFile, setPdfFile] = useState(null);
    const [isMessageFromAPI, setIsMessageFromAPI] = useState(false);
    const [isFileUploaded, setIsFileUploaded] = useState(false);
    const [showFileInput, setShowFileInput] = useState(false);
    const [pdffilename, setPdfFilename] = useState('');

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


    const goToPrevPage = () => {
        setPageNumber((prevPage) => Math.max(prevPage - 1, 1)); // Limit to not go below page 1
    };

    const goToNextPage = () => {
        setPageNumber((prevPage) => Math.min(prevPage + 1, numPages)); // Limit to not go above numPages
    };

    const handleFileChange = (e) => {
        setPdfFile(e.target.files);
    };

    const handleFileUpload = async () => {
        try {
            setLoading(true);
            setIsFileUploaded(true);
            setShowFileInput(true);
            const formData = new FormData();
            for (let i = 0; i < pdfFile.length; i++) {
                formData.append("file", pdfFile[i]);  // Append each file to the form data
            }

            // Call the /upload API
            const uploadResponse = await fetch("/api/upload", {
                method: "POST",
                body: formData,
            });


            if (!uploadResponse.status) {
                throw new Error("Failed to upload file");
            }
            else {
                // Call the /ingest API
                const ingestResponse = await fetch("/api/ingest", {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });

                if (!ingestResponse.ok) {
                    throw new Error("Failed to ingest file");
                }

                // Handle the response from /ingest API
                const result = await ingestResponse.json();
                console.log("Ingest response:", result);

                // Set the answer or perform other actions based on the response
                setAnswer("File uploaded and ingested successfully");
                setIsMessageFromAPI(false);

            }
            setShowFileInput(false);
        }

        catch (error) {
            console.error("Error:", error);
            setAnswer("An error occurred during file upload and ingestion");
        } finally {
            setLoading(false);
        }


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
            let pdf_filename = '';

            if (sourceMatch) {
                pdf_source = sourceMatch[1]; // This will be your source string
                page = sourceMatch[2]; // This will be your page string
                pdf_filename = pdf_source.split('/').pop();
                setPdfSource(pdf_source)
                setPageNumber(parseInt(page))
                setPdfFilename(pdf_filename)
            }

            // Remove the 'Source' line from the message
            const message = msg_with_source.replace(sourceRegex, '');
            // console.log(message);
            console.log(`PDF Filename: ${pdf_filename}`)
            // console.log(`Source: ${pdf_source}`);
            // console.log(`Page: ${page}`);

            setAnswer(message);
        } catch (err) {
            console.error(err, "err");
        } finally {
            setLoading(false);
            setIsMessageFromAPI(true);
        }
    };

    return (<div className="screen">
        <div className="navbar">
            <button onClick={handleFileUpload}>Upload Files</button>
            {showFileInput && (  // Render the file input based on the state
                <input
                    type="file"
                    id="file"
                    name="file"
                    multiple
                    onChange={handleFileChange}
                />
            )}

            {pdfFile && !isFileUploaded && (
                <button onClick={handleFileUpload} className="submitButton">
                    Submit
                </button>
            )}
        </div>

        <div className="app" >
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
                    {answer && isMessageFromAPI && !showPDF && (
                        <div className="pdf-toggle-button">
                            <button onClick={() => setShowPDF(true)}>Show PDF</button>
                        </div>
                    )}
                </div>
            </div>
        </div>
        {showPDF && (
            <div className="pdf-renderer">
                <div>
                    <div className="pdf-filename">{pdffilename}</div>
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
        )
        }
    </div >
    );
}

function PdfRender() {
    return <div className={"pdf-renderer"}></div>
}