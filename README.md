# Newsletter_generator
This project generates newsletters using **CrewAI** for task automation and **Pexels API** for image generation. The workflow includes multiple agents working in sequence to gather and refine content, generate summaries, and design a newsletter layout. The generated output is an HTML file that can be directly used to send newsletters via email.

## Prerequisites

Before you begin, make sure you have Python 3.7+ installed on your machine.

### Step 1: Clone the Repository

To get started, clone the repository to your local machine.

```markdown
git clone <your-repository-url>
cd <your-repository-name>
```

### Step 2: Set Up a Virtual Environment

Create a virtual environment for this project to manage dependencies.

```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

Activate the virtual environment:

- On **Windows**:

```bash
.venv\Scripts\activate
```

- On **Mac/Linux**:

```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies

Install all necessary dependencies by running:

```bash
pip install -r requirements.txt
```

### Step 5: Environment Configuration

Create a `.env` file in the root directory and add your **Pexels API key** and **Groq API key** for CrewAI:

```
PEXELS_API_KEY=<your-pexels-api-key>
GROQ_API_KEY=<your-groq-api-key>
```

You can get a Pexels API key by registering on [Pexels API](https://www.pexels.com/api/). Similarly, create a Groq account to get your API key for CrewAI.

---

## Running the Project

There are two methods available to run the project: **using the Streamlit UI** or **using the terminal**.

### Method 1: Using Streamlit UI

1. Once you have activated the virtual environment and installed dependencies, you can start the Streamlit app by running:

    ```bash
    streamlit run app.py
    ```

2. The app will open in your browser where you can enter the topic for your newsletter. After entering the topic, click on the "Generate Newsletter" button, and the newsletter will be generated. You can then download it in HTML format.

### Method 2: Using Terminal (Non-UI)

If you prefer running the script without the UI, you can use the terminal to execute the script:

1. Run the following command:

    ```bash
    python ./main.py
    ```

2. This will execute the backend process of generating the newsletter based on the given topic and output it as an HTML file.

---

## Workflow Explanation

The project uses **CrewAI** to create agents that work in sequence to process the newsletter content. Here's a brief explanation of the workflow:

1. **Topic Discovery Agent**: Identifies trending topics based on news, social media, and research.
2. **Content Aggregator Agent**: Gathers content related to the identified topics from reliable sources.
3. **Content Relevancy Agent**: Filters and refines the aggregated content to ensure it aligns with the newsletter's target audience.
4. **Summary Generator Agent**: Generates concise and engaging summaries for each piece of content.
5. **Design and Layout Agent**: Creates the HTML layout for the newsletter with inline CSS.
6. **Image and Media Generator Agent**: Fetches relevant images from the Pexels API and places them within the newsletter layout.

Once the content is processed by these agents, the output is an HTML file with both content and images, ready to be used in an email newsletter.

---

## Tools and Libraries Used

- **CrewAI**: For automating tasks with agents that work in a sequential manner.
- **Pexels API**: To fetch relevant images for the newsletter.
- **Streamlit**: For creating an easy-to-use platform for interactive web apps.
- **Python**: The primary programming language used for this project.
- **.env**: Used to store API keys for Pexels and Groq securely.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Troubleshooting

If you encounter any issues, ensure that:

- You have the correct API keys set up in the `.env` file.
- All dependencies are correctly installed in the virtual environment.
- The `main.py` or `app.py` file is located in the root directory.

If problems persist, you can check the logs in the terminal or Streamlit's debug logs for additional information.

---

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests with improvements, bug fixes, or enhancements.

---
