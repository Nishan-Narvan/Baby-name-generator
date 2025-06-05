# File: langchain_helper.py

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# Load API key from .env file
load_dotenv() # This will look for a .env file in the same directory
api_token = os.getenv("GOOGLE_API_KEY")

if not api_token:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")

# Initialize Gemini Model
# Model options: "gemini-1.5-flash-latest" (faster, more cost-effective) or "gemini-1.5-pro-latest" (more powerful)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    google_api_key=api_token,
    temperature=0.7 # Adjust for more creative (higher) or more deterministic (lower) responses
)

# Defining function for LLM
def generate_baby_name(personality_type, gender_type, religion_type, country_type):
    prompt_template_name = PromptTemplate(
        input_variables=['personality_type', 'gender_type', 'religion_type', 'country_type'],
        template=(
            "You are an experienced linguist and cultural enthusiast with over 15 years of expertise in onomastics (the study of names). "
            "Your goal is to suggest thoughtful and cool names that will resonate with both the child as they grow and their parents. "
            "First, please acknowledge the user's care and thoughtfulness in seeking a meaningful name, perhaps saying something like: "
            "'It's wonderful that you're putting so much thought into choosing the perfect name for your child. This journey is a special part of parenting, and I'm here to help you find some beautiful options.'\n\n"
            "Now, based on the following preferences:\n"
            "- Personality trait inspiration: '{personality_type}'\n"
            "- Gender: {gender_type}\n"
            "- Religious/Cultural influence: {religion_type}\n"
            "- Country of parents/child: {country_type}\n\n"
            "Please suggest 10 unique and meaningful names. "
            "These names should reflect '{personality_type}' characteristics. "
            "They can be inspired by or be synonyms of deities, revered figures, or historical personalities relevant to the {religion_type} culture and history, including those associated with {country_type} if applicable. "
            "Ensure at least 4 of the names have a modern or 'cool' vibe, without explicitly labeling them as 'cool'. "
            "For each name, provide a brief, insightful description (1-2 sentences) explaining its meaning, origin, or the reason for its suggestion in this context. "
            "Present the names as a list."
        )
    )

    # Create LLM Chain
    # The output key for LLMChain is 'text' by default when the prompt output is directly fed to an LLM
    chain = LLMChain(llm=llm, prompt=prompt_template_name)

    # Invoke LLM with input parameters
    try:
        response = chain.invoke({
            "personality_type": personality_type,
            "gender_type": gender_type,
            "religion_type": religion_type,
            "country_type": country_type
        })
        # The actual generated text is in the 'text' field of the response dictionary
        return response.get('text', "Sorry, I couldn't generate names at this moment. Please try again.")
    except Exception as e:
        print(f"Error during LLM invocation: {e}")
        return "An error occurred while generating names. Please check the logs or try again later."

# **Test Function Call (Corrected)**
if __name__ == "__main__":
    print("Testing baby name generation...")
    # Example test call - ensure you have GOOGLE_API_KEY in your .env for this to run
    if api_token:
        # Provide all four arguments for the test
        test_response = generate_baby_name(
            personality_type="Leader",
            gender_type="Girl",
            religion_type="Hinduism",
            country_type="India"
        )
        print("\n--- Generated Names (Test) ---")
        print(test_response)
        
        test_response_2 = generate_baby_name(
            personality_type="Charming",
            gender_type="Boy",
            religion_type="Christianity",
            country_type="USA"
        )
        print("\n--- Generated Names (Test 2) ---")
        print(test_response_2)
    else:
        print("Skipping test because GOOGLE_API_KEY is not set.")