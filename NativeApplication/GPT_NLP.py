import openai, time, functools
API_KEY = "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"
def timer(func): 
    @functools.wraps(func) 
    def wrapper(*args, **kwargs): 
        start = time.perf_counter() 
        ret = func(*args, **kwargs) 
        print(f'Time taken to execute: {time.perf_counter() - start}s') 
        return ret 
    return wrapper
class NLP:
    def __init__(self, apikey=API_KEY, model="gpt-3.5-turbo"):
        # Setting the API key to use the OpenAI API
        openai.api_key = apikey
        self.model = model
        self.origin_message = {
            "role": "assistant",
            "content": "Your role is to correct and create various incorrect sentences in a IT business meeting context, addressing issues like grammar, incorrect words, or missing words. Give only the corrected sentence."
            }
        self.messages = [self.origin_message,]
    #@timer
    def correction_raw(self, message):
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[self.origin_message , {"role": "user", "content": message}]
        )
        self.messages.append({"role": "assistant", "content": response["choices"][0]["message"].content})
        return response
    def correction(self, message):
        return self.correction_raw(message)["choices"][0]["message"]['content']
    def addcontext(self, context):
        """Add Context"""
        self.messages.append({"role": "assistant", "content": context})
    def chat_raw(self, message):
        self.messages.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
            )
        return response
    def chat(self, message):
        return self.chat(message)["choices"][0]["message"]

def nlp_file(filename, _inst = NLP()) -> None:
    with open(filename, 'r') as file:
        text = file.read()
    if text.strip() == "": return ""
    newText = _inst.correction(text)
    with open(filename, 'w+') as file:
        file.write(newText)
    return newText
if __name__ == "__main__":
    nlp_file('transcript.txt')
    # while True:
    #     nlp = NLP()
    #     prompt = input("What is your input: ")
    #     print(nlp.correction(prompt))
