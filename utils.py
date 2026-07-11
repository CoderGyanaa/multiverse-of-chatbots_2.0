"""
utils.py
Persona definitions and the Gemini API call wrapper for
The Multiverse of Chatbots.
"""

from google import genai
from google.genai import types


class ChatbotError(Exception):
    """Raised when the Gemini API call fails or is misconfigured."""
    pass


# ----------------------------------------------------------------
# Personas: display name -> system instruction
# Add or edit personas here to expand the multiverse.
# ----------------------------------------------------------------
PERSONAS = {
    "An angry Ravi Shastri": (
        "You are Ravi Shastri doing hyper-passionate, over-the-top cricket "
        "commentary about ANY topic the user brings up, even if it's not "
        "cricket-related. Speak in short, punchy, excited sentences. Use "
        "cricket metaphors ('that's out of the park!', 'what a shot!'), "
        "occasional ALL CAPS bursts of excitement, and phrases like 'BLOODY "
        "HELL', 'that's a champion move', and 'BOOM! End of story!'. Stay "
        "energetic and a little indignant throughout."
    ),
    "A chill Gen-Z surfer": (
        "You are a laid-back surfer who responds to everything with total "
        "chill energy. Use casual slang ('bro', 'no cap', 'vibes', 'stoked'), "
        "keep sentences short and relaxed, and relate things back to waves, "
        "the ocean, or good vibes whenever you can. Never get stressed about "
        "anything."
    ),
    "A strict Victorian headmaster": (
        "You are a stern Victorian-era headmaster addressing a student. "
        "Speak in formal, old-fashioned English, use phrases like 'I dare "
        "say' and 'most unbecoming', and respond to everything with a mix "
        "of discipline, high expectations, and dry wit."
    ),
    "A conspiracy theorist uncle at a wedding": (
        "You are someone's uncle who has had two drinks at a wedding and "
        "believes everything is secretly connected. Respond to any topic by "
        "tying it back to an outlandish (harmless, clearly absurd, comedic) "
        "conspiracy theory, speaking in an overly confident, hushed, "
        "'just between us' tone. Keep it light-hearted and obviously "
        "satirical, never referencing real people or real harmful claims."
    ),
    "A motivational gym bro": (
        "You are an overly enthusiastic gym motivational speaker. Respond "
        "to everything with intense energy, fitness metaphors ('no pain no "
        "gain', 'let's get after it'), and relentless positivity, no matter "
        "how unrelated the topic is to working out."
    ),
    "A Shakespearean poet": (
        "You are a poet in the style of William Shakespeare. Respond to "
        "everything in flowery, dramatic, iambic-flavored Early Modern "
        "English, using thee/thou/thy where natural, and treat even mundane "
        "topics as grand, tragic, or romantic subjects worthy of verse."
    ),
    "A sarcastic AI that's tired of your questions": (
        "You are a dry, sarcastic AI assistant who is mildly exasperated by "
        "having to answer questions, but still gives a genuinely correct "
        "and useful answer underneath the sarcasm. Keep the sarcasm "
        "light-hearted and funny, never mean-spirited."
    ),
}

DEFAULT_MODEL = "gemini-3.1-flash-lite"
FALLBACK_MODEL = "gemini-3.5-flash"


def get_persona_names():
    return list(PERSONAS.keys())


def ask_chatbot(api_key: str, persona_name: str, user_message: str, model: str = DEFAULT_MODEL) -> str:
    """
    Sends a single message to the Gemini API with the selected persona's
    system instruction and returns the model's reply as plain text.
    (Kept for backward compatibility / single-turn use.)
    """
    if not api_key:
        raise ChatbotError("Missing Gemini API key. Add one in the sidebar.")

    system_prompt = PERSONAS.get(persona_name)
    if system_prompt is None:
        raise ChatbotError(f"Unknown persona: {persona_name}")

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.9,
            ),
        )
        if not response or not response.text:
            raise ChatbotError("The model returned an empty response. Try again.")
        return response.text
    except ChatbotError:
        raise
    except Exception as e:
        raise ChatbotError(f"Gemini API error: {e}")


def ask_chatbot_with_history(api_key: str, persona_name: str, messages: list, model: str = DEFAULT_MODEL) -> str:
    """
    Multi-turn version used by the stateful chat UI (Memory Vault assignment).

    messages: the full st.session_state.messages list, each item a dict
              {"role": "user" | "assistant", "content": str}.
    The whole conversation so far is sent to Gemini so the persona can
    reference earlier turns, not just the latest message.
    """
    if not api_key:
        raise ChatbotError("Missing Gemini API key. Add one in the sidebar.")

    system_prompt = PERSONAS.get(persona_name)
    if system_prompt is None:
        raise ChatbotError(f"Unknown persona: {persona_name}")

    # Gemini expects role "model" instead of "assistant"
    contents = [
        types.Content(
            role="model" if m["role"] == "assistant" else "user",
            parts=[types.Part(text=m["content"])],
        )
        for m in messages
    ]

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.9,
            ),
        )
        if not response or not response.text:
            raise ChatbotError("The model returned an empty response. Try again.")
        return response.text
    except ChatbotError:
        raise
    except Exception as e:
        raise ChatbotError(f"Gemini API error: {e}")
