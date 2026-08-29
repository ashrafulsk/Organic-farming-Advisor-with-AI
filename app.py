import gradio as gr


# ============================================================
# 🌱 AI ORGANIC FARMING ADVISOR
# Hugging Face Spaces / Gradio Version
# ============================================================


# ============================================================
# ORGANIC FARMING KNOWLEDGE BASE
# ============================================================

KNOWLEDGE_BASE = [
    {
        "topic": "Organic Fertilizers",
        "keywords": [
            "fertilizer", "compost", "vermicompost",
            "manure", "soil fertility", "neem cake"
        ],
        "content": """
Compost is an organic fertilizer made from decomposed plant
and kitchen waste. Vermicompost is produced using earthworms
and is rich in nutrients. Farmyard manure is made from
decomposed animal dung, urine, bedding material and farm waste.

Green manure crops can be grown and incorporated into the soil
to improve soil fertility. Neem cake can be used as an organic
soil amendment and may also help manage certain soil pests.
"""
    },

    {
        "topic": "Natural Pest Control",
        "keywords": [
            "pest", "insect", "whitefly", "whiteflies",
            "aphid", "aphids", "neem", "bug", "insects"
        ],
        "content": """
Natural pest management can include neem-based products,
yellow sticky traps, removal of severely affected plant parts,
and encouragement of beneficial insects such as ladybirds
and lacewings.

Regular monitoring is important. Crop rotation, field sanitation
and preventive farming practices can reduce pest pressure.
Farmers should follow product labels and locally applicable
organic farming guidelines when using treatments.
"""
    },

    {
        "topic": "Compost Preparation",
        "keywords": [
            "compost", "composting", "kitchen waste",
            "organic waste", "decomposition"
        ],
        "content": """
To prepare compost, collect suitable organic materials such as
dry leaves, vegetable waste, grass clippings and plant residues.

Create alternating layers of dry carbon-rich materials and
green nitrogen-rich materials. Maintain adequate moisture
without making the pile waterlogged.

Turn the compost periodically to provide oxygen and encourage
decomposition. Mature compost is generally dark, crumbly and
has an earthy smell.

Do not add plastic, chemical waste or other unsuitable materials.
"""
    },

    {
        "topic": "Soil Health",
        "keywords": [
            "soil", "soil health", "fertility",
            "organic matter", "rotation", "cover crop"
        ],
        "content": """
Crop rotation can help maintain soil health and reduce the
buildup of certain pests and diseases.

Compost, farmyard manure and green manure can increase organic
matter and improve soil fertility. Cover crops can help protect
soil from erosion and may improve soil organic matter.

Regular soil testing can help farmers understand nutrient
requirements.
"""
    },

    {
        "topic": "Sustainable Farming",
        "keywords": [
            "sustainable", "mulch", "mulching",
            "water", "irrigation", "weed"
        ],
        "content": """
Mulching can help conserve soil moisture, suppress weeds and
moderate soil temperature.

Drip irrigation can improve water-use efficiency.

Crop rotation, cover crops, field sanitation and regular
monitoring are useful components of sustainable farming.
"""
    },

    {
        "topic": "Tomato Farming",
        "keywords": [
            "tomato", "tomatoes", "tomato plant"
        ],
        "content": """
Tomatoes benefit from fertile, well-drained soil enriched with
mature compost.

Mulching can help maintain soil moisture and reduce weed growth.

Regular monitoring is important for detecting pests early.
Organic approaches may include physical removal, sticky traps,
beneficial insects and appropriate approved organic treatments.

Crop rotation can help reduce recurring soil-related pest and
disease problems.
"""
    },

    {
        "topic": "Rice Farming",
        "keywords": [
            "rice", "paddy", "rice crop"
        ],
        "content": """
Organic rice production can use compost, farmyard manure and
green manure to improve soil fertility.

Weed management may include manual weeding, mechanical methods
and suitable water management.

Crop rotation and field sanitation can help manage pest and
disease pressure.
"""
    }
]


# ============================================================
# KNOWLEDGE RETRIEVAL
# ============================================================

def retrieve_knowledge(question):
    """
    Simple keyword-based knowledge retrieval.
    """

    question_lower = question.lower()

    matched_documents = []

    for document in KNOWLEDGE_BASE:

        score = 0

        for keyword in document["keywords"]:

            if keyword.lower() in question_lower:
                score += 1

        if score > 0:
            matched_documents.append(
                (score, document)
            )

    # Sort by relevance
    matched_documents.sort(
        key=lambda x: x[0],
        reverse=True
    )

    # Get top 3 relevant documents
    selected_documents = matched_documents[:3]

    if not selected_documents:
        return """
No specific document was matched in the current knowledge base.

Try asking about:
- Organic fertilizers
- Natural pest control
- Compost preparation
- Soil health
- Tomato farming
- Rice farming
- Sustainable farming
"""

    context = ""

    for score, document in selected_documents:

        context += (
            f"\n### 📚 {document['topic']}\n"
            f"{document['content']}\n"
        )

    return context


# ============================================================
# GENERATE FARMING RESPONSE
# ============================================================

def generate_advice(crop, category, location, question):

    if not question.strip():

        return (
            "⚠️ Please enter your farming question.",
            ""
        )

    # Combine all user information
    full_question = f"""
Crop: {crop}

Problem Category: {category}

Location: {location}

Farmer Question:
{question}
"""

    # Retrieve relevant knowledge
    retrieved = retrieve_knowledge(full_question)

    # --------------------------------------------------------
    # Rule-based response for the first deployment
    # --------------------------------------------------------

    answer = f"""
# 🌱 AI Organic Farming Advisor

### 👨‍🌾 Your Question

{question}

### 🌾 Crop

{crop}

### 🔍 Problem Category

{category}

"""

    if location.strip():

        answer += f"""
### 📍 Location

{location}

"""

    answer += """
### 🌿 Organic Farming Recommendation

"""

    answer += retrieved

    answer += """

### ⚠️ Important Note

This advisor provides general educational information.
For serious crop diseases, severe pest infestations,
or region-specific agricultural problems, consult a
qualified local agricultural expert or agriculture
department.

Always follow the label instructions and applicable
organic farming regulations when using any agricultural
product.
"""

    return answer, retrieved


# ============================================================
# CLEAR FUNCTION
# ============================================================

def clear_form():

    return (
        "Tomato",
        "Pest Control",
        "",
        "",
        "",
        ""
    )


# ============================================================
# GRADIO INTERFACE
# ============================================================

with gr.Blocks(
    title="AI Organic Farming Advisor"
) as demo:

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    gr.Markdown(
        """
# 🌱 AI Organic Farming Advisor

### Your intelligent assistant for organic and sustainable farming

Get guidance about:

🌾 **Organic Fertilizers**  
🐛 **Natural Pest Control**  
♻️ **Compost Preparation**  
🌱 **Soil Health**  
💧 **Sustainable Farming**
"""
    )

    gr.Markdown("---")

    # --------------------------------------------------------
    # INPUT AREA
    # --------------------------------------------------------

    with gr.Row():

        with gr.Column(scale=1):

            crop = gr.Dropdown(
                choices=[
                    "Tomato",
                    "Rice",
                    "Wheat",
                    "Chilli",
                    "Cotton",
                    "Potato",
                    "Onion",
                    "Vegetables",
                    "Other"
                ],
                value="Tomato",
                label="🌾 Select Crop"
            )

            category = gr.Dropdown(
                choices=[
                    "Pest Control",
                    "Disease Management",
                    "Organic Fertilizer",
                    "Compost Preparation",
                    "Soil Health",
                    "Weed Management",
                    "Water Management",
                    "General Farming"
                ],
                value="Pest Control",
                label="🔍 Problem Category"
            )

            location = gr.Textbox(
                label="📍 Location (Optional)",
                placeholder="Example: Andhra Pradesh, India"
            )

        with gr.Column(scale=2):

            question = gr.Textbox(
                label="👨‍🌾 Ask Your Farming Question",
                placeholder=(
                    "Example: How can I control whiteflies "
                    "on my tomato plants organically?"
                ),
                lines=6
            )

            with gr.Row():

                ask_button = gr.Button(
                    "🌱 Get Organic Advice",
                    variant="primary"
                )

                clear_button = gr.Button(
                    "🗑️ Clear"
                )

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    gr.Markdown("## 🤖 AI Farming Recommendation")

    answer = gr.Markdown(
        value="Your farming recommendation will appear here."
    )

    # --------------------------------------------------------
    # RETRIEVED KNOWLEDGE
    # --------------------------------------------------------

    with gr.Accordion(
        "📚 View Retrieved Knowledge",
        open=False
    ):

        retrieved_context = gr.Markdown(
            value="Retrieved knowledge will appear here."
        )

    # --------------------------------------------------------
    # EXAMPLES
    # --------------------------------------------------------

    gr.Markdown("## 💡 Example Questions")

    gr.Examples(
        examples=[
            [
                "Tomato",
                "Pest Control",
                "Andhra Pradesh, India",
                "How can I control whiteflies on my tomato plants organically?"
            ],
            [
                "Vegetables",
                "Organic Fertilizer",
                "India",
                "What organic fertilizer can I use for vegetables?"
            ],
            [
                "General Farming",
                "Compost Preparation",
                "India",
                "How can I prepare compost at home?"
            ],
            [
                "Rice",
                "Soil Health",
                "Andhra Pradesh, India",
                "How can I improve soil fertility naturally for rice?"
            ],
            [
                "Chilli",
                "Pest Control",
                "India",
                "How can I control aphids naturally?"
            ]
        ],
        inputs=[
            crop,
            category,
            location,
            question
        ]
    )

    # --------------------------------------------------------
    # BUTTON ACTION
    # --------------------------------------------------------

    ask_button.click(
        fn=generate_advice,
        inputs=[
            crop,
            category,
            location,
            question
        ],
        outputs=[
            answer,
            retrieved_context
        ]
    )

    # --------------------------------------------------------
    # CLEAR BUTTON
    # --------------------------------------------------------

    clear_button.click(
        fn=clear_form,
        inputs=[],
        outputs=[
            crop,
            category,
            location,
            question,
            answer,
            retrieved_context
        ]
    )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    gr.Markdown(
        """
---

### 🌱 AI Organic Farming Advisor

**GenAI Concepts:** Knowledge Retrieval • Content Generation

*For educational purposes and general agricultural guidance.*
"""
    )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860
    )