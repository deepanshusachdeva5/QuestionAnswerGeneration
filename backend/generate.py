from fastapi import FastAPI, Query
from openai import OpenAI
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

load_dotenv()

KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=KEY)
app = FastAPI()


# @app.get("/login")
# async def loginGPT():
#     return
origins = [
    "http://localhost:3000",  # Your React app's origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/generate_question/")
async def generateQues(
    text: str = Query(
        ..., title="Text", description="The input text for question generation"
    )
):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a Muliple Choice Question Generator Robot, who generates questions based on the information given, first all the questions come and then the answers  at the end separted by the questions by----------",
            },
            {
                "role": "user",
                "content": "Generate 10 MCQ for the following: \n" + text,
            },
        ],
    )
    print(
        "=========================RESPONSE======================================",
        response,
    )
    questions, answerKey = response.choices[0].message.content.split(
        "--------------------------------------"
    )

    # print(answerKey)
    answerKey = answerKey.split("\n\n")[1]
    answerKey = answerKey.split("\n")
    questions_list = questions.split("\n\n")
    questions_with_options_and_id = []
    print(questions_list)
    for i in range(len(questions_list) - 1):
        print(questions_list[i].split("\n"))

        question_and_options = questions_list[i].split("\n")
        txt = question_and_options[0]
        options_lst = []
        for j in range(1, len(question_and_options)):
            options_lst.append([j, question_and_options[j]])
        questions_with_options_and_id.append([i + 1, txt, options_lst])

    answers_options = []

    alphabet_key_to_number = {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "A": 1,
        "B": 2,
        "C": 3,
        "D": 4,
    }
    for i in range(len(answerKey)):
        currAns = alphabet_key_to_number[answerKey[i].split(")")[0].split(". ")[1]]
        answers_options.append(str(i + 1) + "_" + str(currAns))

    return {"Questions": questions_with_options_and_id, "Answers": answers_options}


if __name__ == "__main__":
    uvicorn.run("generate:app", host="localhost", port=8000)
