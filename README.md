# Bewise project services
> 1. Question service
>     * Receiving questions and saving to the database
> 2. Audio service
>     * User creation
>     * For each user - saving the audio recording in wav format, converting it to mp3 format and writing to the database and providing a link to download the audio recording 
>     * Download audio recording in mp3 format
# Installation
> ### Prerequisites
> * installed docker
> * installed git
> ### Run command
> ```
> git clone https://github.com/Acidastro/bewise.git
> ```
# Starting
> ### Service 1
> Run command
> ```
> docker-compose -f bewise/docker-compose.yml up --build question_service
> ```

> ### Service 2
>  Run command
>  ```
>  docker-compose -f bewise/docker-compose.yml up --build audio_service
>  ```
# Examples of using
> ## Service 1
> ### 1. Get questions (POST)
>   * **Request URL** [http://localhost:23000/get_question/]()
>     * Request example
>       ``` 
>       curl -X 'POST' \
>         'http://localhost:23000/get_question/' \
>         -H 'accept: application/json' \
>         -H 'Content-Type: application/json' \
>         -d '{
>         "questions_num": 1    
>       }'
>       ```
>     * Response example
>       ```
>       "This major league team used to take the field at 34 Kirby Puckett Place"
>       ```

>## Service 2
> ### 1. Create user (POST)
>   * **Request URL** [http://localhost:23001/create_user/]()
>     * Request example
>       ```
>       curl -X 'POST' \
>         'http://localhost:23001/create_user/' \
>         -H 'accept: application/json' \
>         -H 'Content-Type: application/json' \
>         -d '{
>         "user_name": "string"
>       }'
>       ```
>     * Response example
>       ```
>       {
>       "user_id": 12,
>       "user_token": "83c18780-32d0-4b4b-8256-0dcefb0360e3"
>       }
>       ```
> ### 2. Upload audio route (POST)
>   * **Request URL** [http://localhost:23001/upload_audio/]()
>     * Request example
>       ```
>       curl -X 'POST' \
>         'http://localhost:23001/upload_audio/?user_id=12&user_token=83c18780-32d0-4b4b-8256-0dcefb0360e3' \
>         -H 'accept: application/json' \
>         -H 'Content-Type: multipart/form-data' \
>         -F 'file=@file_example_WAV_1MG.wav;type=audio/wav'
>       ```
>     * Response example
>       ```
>       http://localhost:23001/record?audio=6&user=12
>       ```
> ### 3. Download audio route
>   * **Request URL** [http://localhost:23001/record/?audio=6&user=12]()
>     * Request example
>       ```
>       curl -X 'GET' \
>         'http://localhost:23001/record/6/12' \
>         -H 'accept: application/json'
>       ```
>     * Response example
>       > * Response body
>       > 
>       >   * [<u>Download file</u>]()
>       > * Response headers
>       >   ```
>       >   content-disposition: attachment;filename=6_12.mp3 
>       >   content-length: 101348 
>       >   content-type: audio/mpeg 
>       >   date: Tue,23 May 2023 10:31:50 GMT 
>       >   server: uvicorn 
>       >   ```
