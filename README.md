# JobHub: fetching jobs across different platforms

## App purpose

Seamlessly scouring top platforms like LinkedIn, Indeed, and more, the application matches your skills with relevant job listings. Simply input your desired job title, skills, and preferred platforms, and let the app handle the rest, streamlining your search process effortlessly.

## How to run

At the moment, only backend service is available so you will need a web API testing software such as Postman to test the app. Frontend features will be coming in the future.

1. Clone the repo to your local
2. [Install Python](https://www.python.org/downloads/)
3. If you're not already, navigate to `JobHub/api` folder
4. Create and open virtual environment
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
6. Install package requirements
   ```
   pip install -r requirements.txt
   ```
7. Run flask app
   ```
   flask run
   ```
9. Go to your API testing software and make a request to the server `GET POST http://127.0.0.1:5000/api/job?job=<Job Title>&location=<City>&skills=<List of skills separated by comma>&platform=<List of platforms separated by comma>`

   Example:
    ```
    GET POST http://127.0.0.1:5000/api/job?job=software engineer&location=kelowna&skills=python,c++,java&platform=linkedin,indeed
    ```
    ```
    {
    "data": [
        {
            "company": "Global Relay",
            "describ": [
                "experience working with java back end components and docker and kubernetes"
            ],
            "location": "Kelowna, British Columbia, Canada",
            "role": "Intermediate React Developer (React.js/JavaScript)",
            "skills": [
                "java"
            ]
        },
        {
            "company": "Summit",
            "describ": [
                "develop and deploy impactful code using typescript python java html javascript"
            ],
            "location": "Kelowna, British Columbia, Canada",
            "role": "Fullstack Developer",
            "skills": [
                "python",
                "java"
            ]
        },
        {
            "company": "Affirm",
            "describ": [
                "experience with one of the following languages python c c++ java kotlin javascript reactjs and or similar languages"
            ],
            "location": "Kelowna, British Columbia, Canada",
            "role": "Software Engineer I, Backend (Disclosures)",
            "skills": [
                "python"
            ]
        },
      ]
    ...
    }
    ```
