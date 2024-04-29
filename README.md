# antiSMI App

![logo](https://github.com/data-silence/antiSMI-app/blob/master/img/1.png?raw=true)

![Streamlit](https://img.shields.io/badge/Streamlit-black?style=flat-square&logo=Streamlit) ![Docker](https://img.shields.io/badge/docker-%230db7ed?style=flat-square&logo=Docker) ![sklearn](https://img.shields.io/badge/sklearn-black?style=flat-square&logo=sklearn)

## Table of contents
* [About](#about)
* [Self deploy](#self-deploy)
* [Contact info](#contact-info)


## About

The App is a web interface for the [AntiSMI project](https://github.com/data-silence/antiSMI-Project) based on Streamlit framework. 
It's explores and creates new ways of working with media for readers, journalists and researchers. 
You can use it at http://38.242.140.206:8501/

## Self deploy

Important: You will not be able to properly deploy the application due to the need to have access to a properly organized database, backend and other parts of the project.

1. Clone the repository into the empty directory selected for the project:
`git clone https://github.com/data-silence/antiSMI-app`
2. Make sure that docker is installed on the server. Build the image from the destination directory using the command `docker build -t -frontend`
3. Start the container using `docker run -d --rm --name frontend -p 8501:8501 frontend`
4. Your app will start on port 8501


## Contact info
* enjoy-ds@pm.me
