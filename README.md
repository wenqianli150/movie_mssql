# movie_mssql
Movie DB App through Django &amp; Python


### Install Instructions (Tested on Debian):
1. Install Anaconda [Anaconda](https://www.anaconda.com/products/distribution/download-success-2)
2. Clone this repository

     ```git clone https://github.com/SoloNick/Movies_MSSQL.git```
3. Install [ODBC Driver](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15)     

4. Create a new conda environment. In Start menu search for Anaconda Prompt.
In console / Anaconda prompt enter:

    ```conda create -n movies python=3.8```
    
5. Activate the newly created environment

    ```conda activate movies```
     
6. Navigate to the project root directory and install required python packages

     ```pip3 install -r requirements.txt```


### Local Use Instructions
1. Navigate to ```/movies_backend/``` and execute

     ```python3 manage.py runserver```
     
2. Open ```/movies_frontend/www/index.html``` in a browser of your choice
