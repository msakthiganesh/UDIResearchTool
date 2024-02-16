# UDIResearchTool

<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot][product-screenshot]

The project is a web application built using React that allows users to upload and view PDF files. It includes features such as file upload, PDF rendering, and an interactive interface for displaying and navigating through the PDF content. The application also integrates with an API to handle file upload and ingestion, and it provides a spotlight-like interface for users to input queries and receive responses.

Disclaimer: The React front-end of the application has been developed using GenAI tools using Chain of Thought and Prompt Engineering.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

This application is built using: 

* [![Python][Python]][Python-url]
* [![Flask][Flask]][Flask-url]
* [![OpenAI][OpenAI]][OpenAI-url]
* [![React][React.js]][React-url]
* [![Vite][Vite]][Vite-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

1. Clone the repository.
``` git clone https://github.com/msakthiganesh/UDIResearchTool.git```
2. Update the environment variables in the ```.env``` file with your OpenAI API key and directories for file upload, vector database (local for FAISS), document datastore, etc.,

### Front-End (UI)

The UI for the application is present under ```UI/udi_bot_frontend``` directory.

#### Installation

To run React + Vite front-end for the application, follow these steps:

1. ``` cd UI/udi_bot_frontend```
2. Install the dependencies using `npm install`.
3. Start the React development server using `npm run dev`.

The React front-end should be available in ```http://localhost:5173/```
### Back-End

The backend (Flask application) is present in the root folder. Python 3.9.18 was used for development.

#### Installation

1. Install python dependencies using ```pip install -r requirements.txt```
2. Start the Flask application using ```python app.py```

The Flask application should be available in ```http://localhost:8001```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] Allow multiple file upload
- [x] Render relevant PDF for the generated content/answer
- [ ] Add conversation history
- [ ] Allow multiple source rendering in UI


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- URLS -->
[issues-shield]: https://img.shields.io/github/issues/msakthiganesh/UDIResearchTool?style=for-the-badge
[issues-url]: https://github.com/msakthiganesh/UDIResearchTool/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/msakthiganesh/UDIResearchTool/blob/c9a9d9392ca6182a2614529416c958f2ba1bf75d/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/msakthiganesh/
[product-screenshot]: images/ui.png
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[Flask]:https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]:https://flask.palletsprojects.com/en/3.0.x/
[OpenAI]: https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white
[OpenAI-url]: https://openai.com/




[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vite]:https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white
[Vite-url]: https://vitejs.dev/




