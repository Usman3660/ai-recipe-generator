import streamlit as st
import torch
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer

# --- CONFIGURATION ---
# THIS IS THE ONLY CHANGE: Point to your local folder
MODEL_PATH = "./my_model_files" 

# Define the special tokens
SPECIAL_TOKENS = {
    "bos_token": "<|startofrecipe|>",
    "eos_token": "<|endofrecipe|>",
    "pad_token": "<|pad|>",
    "additional_special_tokens": ["[TITLE]", "[INGREDIENTS]", "[STEPS]"]
}

# --- MODEL LOADING ---

@st.cache_resource
def load_model_and_tokenizer():
    """Loads the model and tokenizer from the local folder."""
    try:
        # Load tokenizer from the local path
        tokenizer = GPT2Tokenizer.from_pretrained(MODEL_PATH)
        
        # Load model from the local path
        model = GPT2LMHeadModel.from_pretrained(MODEL_PATH)
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        
        generator = pipeline(
            'text-generation',
            model=model,
            tokenizer=tokenizer,
            device=0 if torch.cuda.is_available() else -1 
        )
        return generator, tokenizer
    except Exception as e:
        st.error(f"Error loading model from {MODEL_PATH}: {e}")
        return None, None

generator, tokenizer = load_model_and_tokenizer()

# --- HELPER FUNCTION (Unchanged) ---

def clean_output(full_text, input_type):
    """Cleans the raw model output for display."""
    if input_type == "Title":
        try:
            clean_output = full_text.split("[INGREDIENTS]\n", 1)[1]
            clean_output = "[INGREDIENTS]\n" + clean_output 
        except IndexError:
            clean_output = full_text 
    else:
        try:
            clean_output = full_text.split("[STEPS]\n", 1)[1]
            clean_output = "[STEPS]\n" + clean_output 
        except IndexError:
            clean_output = full_text 

    clean_output = clean_output.replace(SPECIAL_TOKENS['eos_token'], "").strip()
    return clean_output

# --- STREAMLIT UI (Unchanged) ---

st.set_page_config(page_title="AI Recipe Generator", page_icon="🍳", layout="centered")

st.title("🍳 AI Recipe Generator")
st.markdown("Enter a recipe title or a list of ingredients and let the AI write a recipe for you!")

# ... (The rest of the UI code is identical to my previous message) ...
# (Add the example buttons, radio button, text area, and generate button here)

# --- USER INPUT ---
input_type = st.radio(
    "1. What do you want to provide?",
    ("Title", "Ingredients"),
    horizontal=True
)

text_input = st.text_area(
    "2. Enter your text here:",
    placeholder="e.g., 'Spicy Chicken Curry' or 'chicken, onions, curry powder...'",
    height=100
)

# --- GENERATE BUTTON & OUTPUT ---
if st.button("Generate Recipe", type="primary"):
    if not text_input:
        st.warning("Please enter a title or ingredients.")
    elif generator is None or tokenizer is None:
        st.error("Model is not loaded. Cannot generate.")
    else:
        # 1. Format the prompt
        if input_type == "Title":
            prompt = (
                f"{SPECIAL_TOKENS['bos_token']}\n"
                f"[TITLE]\n{text_input}\n"
                f"[INGREDIENTS]\n"
            )
        else:
            prompt = (
                f"{SPECIAL_TOKENS['bos_token']}\n"
                f"[TITLE]\n"
                f"[INGREDIENTS]\n{text_input}\n"
                f"[STEPS]\n"
            )

        # 2. Generate text
        with st.spinner("Conjuring up your recipe... 🪄"):
            generation = generator(
                prompt,
                max_new_tokens=350,
                num_return_sequences=1,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=0.8,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id
            )
        
        full_text = generation[0]['generated_text']
        
        # 3. Clean and display the output
        recipe_output = clean_output(full_text, input_type)
        
        st.subheader("Here's your AI-generated recipe:")
        st.markdown(recipe_output)