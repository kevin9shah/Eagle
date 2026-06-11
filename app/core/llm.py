import ollama

class LLMClient:
    def __init__(self, model_name: str = "llama3"):
        """
        Initializes the local LLM Client using Ollama.
        Make sure you have pulled the model using `ollama pull <model_name>`
        """
        self.model_name = model_name

    def generate(self, prompt: str, system_instruction: str = None) -> str:
        """
        Generates a response from the local LLM.
        """
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        
        messages.append({"role": "user", "content": prompt})

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            print(f"LLM Connection Error: {e}")
            return f"Error connecting to local LLM: {str(e)}"