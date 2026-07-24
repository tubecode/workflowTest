from google import genai

client = genai.Client(api_key="AIzaSyD4nbhwNJT4ohv9fFrKMUCTfdn3SFlsqs4")

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Hi!"
)

print(response.text)