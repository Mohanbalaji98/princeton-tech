from flask import Flask, render_template, request
import openai
import csv

app = Flask(__name__)

APIKEY = "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"
openai.api_key = APIKEY

csv_data = []
with open('/Users/fleet/Downloads/New3.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        csv_data.append(row)
def get_answer(question):
    response = openai.ChatCompletion.create(
        model="gpt-4-0125-preview",
        messages=[
                    {
                        "role": "system",
                        "content": f"""
                            Context: {csv_data}
                            User Query: {question}
                            Follow the instructions given below. Don't reply for questions irrelevant to the context and politely reject."

                            Instructions:
                            1. Ensure the response is focused and directly addresses the user's query.
                            2. If additional information is needed to answer the question, specify what's missing and request the model to provide it.
                            3. Don't answer to questions not relevant to the given context.
                            4. If the question is irrelevant to the context, provide a polite reply that this is irrelevant and whether the user want to know anything related to the given context.
                        """
                    }
                ],
                temperature=0.1,
                top_p=0.1,
                frequency_penalty=0.8,
                presence_penalty=0.2
            )
                
    return response.choices[0].message['content']

@app.route("/", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        question = request.form["question"]
        if question.lower() == 'exit':
            return "Goodbye!"
        answer = get_answer(question)
        print(answer)
        return render_template("index.html", answer=answer)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
