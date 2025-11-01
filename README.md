# 🍳 AI Recipe Generator

A Streamlit web application that uses a fine-tuned **GPT-2 model** to generate complete cooking recipes from either a recipe title or a list of ingredients.

This project was built by fine-tuning the model in a Kaggle Notebook and is deployed using Streamlit Community Cloud.

![Streamlit App Demo]

## ✨ Features

* **Generate from Title:** Give the model a title like "Spicy Chicken Curry" and get a full ingredients list and step-by-step instructions.
* **Generate from Ingredients:** Provide a list of ingredients like "chicken, onions, curry powder" and let the AI create a recipe title and the steps.
* **Interactive UI:** A simple and clean web interface built with Streamlit.

## ⚙️ Tech Stack

* **Model:** GPT-2 (fine-tuned using Hugging Face `transformers` and `PyTorch`)
* **Dataset:** [3a2mext Recipe Dataset](https://www.kaggle.com/datasets/nazmussakibrupol/3a2mext/data) on Kaggle
* **App:** Streamlit
* **Deployment:** Streamlit Community Cloud
* **Model Hosting:** Hugging Face Hub

## 🚀 How to Run Locally

You can run this application on your local machine by following these steps:

**1. Clone the Repository:**
```bash
git clone [https://github.com/Usman3660/ai-recipe-generator.git][Usman3660]/ai-recipe-generator.git
cd ai-recipe-generator
```

**2. Create a Virtual Environment (Recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the Streamlit App:**
```bash
streamlit run app.py
```
The app will open in your browser at `http://localhost:8501`.

## 🤖 The Model

The core of this application is a GPT-2 model fine-tuned on a massive recipe dataset.

* **Base Model:** `gpt2`
* **Training:** The model was trained to understand a specific structure using special tokens:
    * `<|startofrecipe|>`: Marks the beginning of a recipe.
    * `[TITLE]`: Indicates the recipe title.
    * `[INGREDIENTS]`: Indicates the start of the ingredient list.
    * `[STEPS]`: Indicates the start of the instructions.
    * `<|endofrecipe|>`: Marks the end of a recipe.
* **Hosting:** The fine-tuned model and tokenizer are hosted on the Hugging Face Hub at:
    **[https://huggingface.co/[YOUR-USERNAME]/[YOUR-HF-REPO-NAME]](https://huggingface.co/[YOUR-USERNAME]/[YOUR-HF-REPO-NAME])**

## ☁️ Deployment

This app is designed for easy deployment on Streamlit Community Cloud.

1.  **Model:** The fine-tuned model (files like `model.safetensors`, `config.json`, etc.) is uploaded to a public Hugging Face Hub repository.
2.  **Code:** This GitHub repository contains the `app.py` script and the `requirements.txt` file.
3.  **Streamlit Cloud:** The Streamlit app is deployed by linking this GitHub repository. The `app.py` script automatically downloads the model from the Hugging Face Hub on startup.
