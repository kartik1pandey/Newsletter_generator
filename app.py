import os
from crewai import LLM, Agent, Task, Crew, Process
from dotenv import load_dotenv
import re
import requests
import streamlit as st


# Load environment variables
load_dotenv()

# Initialize the LLM
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.environ.get("GROG_API_KEY"),
)

# Define Agents and their Roles

# 1. Topic Discovery Agent
topic_discovery = Agent(
    role="Topic Discovery",
    goal="Identify trending topics in {topic} by analyzing sources like news platforms, social media, and research repositories.",
    backstory="Specialized in identifying emerging trends in {topic} using advanced data collection techniques.",
    llm=llm,
)

# 2. Content Aggregation Agent
content_aggregator = Agent(
    role="Content Aggregator",
    goal="Gather and curate content related to the {topic} topics from reliable sources.",
    backstory="An expert in sourcing high-quality content from reputable platforms and organizing it for further processing.",
    llm=llm,
)

# 3. Content Relevancy Agent
content_relevancy = Agent(
    role="Content Relevancy Checker",
    goal="Evaluate the aggregated content for relevancy, ensuring it aligns with the newsletter's goals and target audience.",
    backstory="Specialized in content evaluation, ensuring only the most relevant and impactful content is selected for use.",
    llm=llm,
)

# 4. Summary Generation Agent
summary_generator = Agent(
    role="Summary Generator",
    goal="Produce concise and engaging summaries of aggregated content.",
    backstory="Proficient in using NLP models to create summaries tailored for technical and non-technical audiences.",
    llm=llm,
)

# 5. Design and Layout Agent
design_layout = Agent(
    role="Design and Layout",
    goal="Create a visually appealing and responsive HTML newsletter layout with inline CSS.",
    backstory="Skilled in crafting professional designs optimized for user engagement.",
    llm=llm,
)
# 6. Image and Media Generator Agent
image_generator = Agent(
    role="Image and Media Generator",
    goal="Place images from the implementation function enhance the layout with visuals.",
    backstory="Ensures images are appropriately sourced and placed in the newsletter.",
    llm=llm,
)



# Define Tasks for Agents

discover = Task(
    description="Identify trending topics in {topic}.",
    expected_output="A list of trending {topic} topics.",
    agent=topic_discovery,
)

aggregator = Task(
    description="Gather content related to {topic}.",
    expected_output="Curated content with key points and links.",
    agent=content_aggregator,
)

relevancy_check_task = Task(
    description="Review and filter the aggregated content for relevancy.",
    expected_output="A refined list of relevant and impactful content.",
    agent=content_relevancy,
)

summary = Task(
    description="Generate summaries of the aggregated content.",
    expected_output="Engaging and concise summaries for each topic.",
    agent=summary_generator,
)

design_layout_task = Task(
    description="Create the HTML layout for the newsletter with inline CSS.",
    expected_output="A responsive HTML file with integrated content and visuals.",
    agent=design_layout,
)

image_generation_task = Task(
    description="Place image in the img tag by the implementation function.",
    expected_output="HTML with updated images and an enhanced layout.",
    agent=image_generator,
    implementation=lambda inputs: replace_images_in_html(inputs),
)

def fetch_pexels_image(query, per_page=1, page=1):
    """
    Fetch an image URL from the Pexels API based on a search query.
    """
    url = f"https://api.pexels.com/v1/search?query={query}&per_page={per_page}&page={page}"
    headers = {"Authorization": os.environ.get("PEXELS_API_KEY")}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data["photos"]:
            return data["photos"][0]["src"]["medium"]  # Get the medium-quality image URL
    return None

def extract_search_queries_from_img_tags(html_content):
    """
    Extract search queries based on nearby text around existing <img> tags.
    """
    img_tags = re.findall(r"<img[^>]*>", html_content)
    queries = []
    for tag in img_tags:
        # Extract surrounding text to form a context-based query
        context = html_content[max(0, html_content.find(tag) - 50): html_content.find(tag) + 50]
        keywords = re.findall(r"\b[a-zA-Z]{4,}\b", context)  # Words with 4+ characters
        if keywords:
            queries.append(" ".join(keywords[:3]))  # Use the first three keywords as the query
        else:
            queries.append("default")  # Fallback query if no meaningful text is found
    return img_tags, queries

def replace_images_in_html(html_content):
    """
    Replace existing <img> tags with new images fetched from the Pexels API.
    """
    img_tags, search_queries = extract_search_queries_from_img_tags(html_content)

    for i, (tag, query) in enumerate(zip(img_tags, search_queries)):
        # Fetch a relevant image based on the search query
        image_url = fetch_pexels_image(query)
        if image_url:
            # Replace the existing <img> tag with a new one
            new_img_tag = f"<img src='{image_url}' alt='Relevant Image {i + 1}' style='max-width: 100%; height: auto;' />"
            html_content = html_content.replace(tag, new_img_tag, 1)

    return {"html_content": html_content}


# Define Crew and Workflow

crew = Crew(
    agents=[
        topic_discovery,
        content_aggregator,
        content_relevancy,
        summary_generator,
        design_layout,
        image_generator,
    ],
    tasks=[
        discover,
        aggregator,
        relevancy_check_task,
        summary,
        design_layout_task,
        image_generation_task,
    ],
    verbose=True,
    process=Process.sequential,  # Execute tasks in sequence
)

# Streamlit UI


st.title("Newsletter Generator")
topic = st.text_input("Enter the newsletter topic:")

if st.button("Generate Newsletter") and topic:
    inputs = {"topic": topic}

    # File names for output files
    image_generation_task.output_file = f"./page/{topic}_newsletter_final2.html"

    # Run the Crew workflow
    crew.kickoff(inputs=inputs)

    try:
        # Read the generated HTML template
        with open(f"./page/{topic}_newsletter_final2.html", "r") as file:
            html_template = file.read()

        # Process the HTML content
        final_html_content = replace_images_in_html(html_template)["html_content"]

        # Save the updated HTML content
        file_name = f"./page/{topic}_updated_template.html"
        with open(file_name, "w") as file:
            file.write(final_html_content)

        # Provide user feedback and link to download or view
        st.success("Newsletter generated successfully!")
        st.download_button(
            label="Download Updated Newsletter",
            data=final_html_content,
            file_name=f"./page/{topic}_updated_template.html",
            mime="text/html",
        )
        st.components.v1.html(final_html_content, height=600)



    except FileNotFoundError:
        st.error(f"The expected HTML file was not generated: {topic}_newsletter_final2.html")