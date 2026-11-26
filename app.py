from google import genai
import streamlit as st

st.set_page_config(
    page_title="Our Story-to-AI Studio ✨", page_icon="📖", layout="centered"
)

st.title("📖 Our Story-to-AI Studio")
st.write(
    "Turn a quick memory, inside joke, or prompt into a custom story and AI"
    " comic prompts!"
)

with st.sidebar:
  st.header("⚙️ AI Settings")
  api_key = st.text_input(
      "Google AI Studio API Key (Optional)",
      type="password",
      help="Leave blank to use the built-in instant story generator!",
  )
  st.caption(
      "Works immediately with no key! Add a free key from ://google.com"
      " anytime for custom AI stories."
  )

col1, col2 = st.columns(2)
with col1:
  hero_name = st.text_input("His Name / Nickname:", value="Babe")
with col2:
  genre = st.selectbox(
      "Choose Story Vibe:",
      [
          "Comedy Adventure",
          "Dark Fantasy Quest",
          "Romantic Sci-Fi",
          "Action Heist",
      ],
  )

story_seed = st.text_area(
    "What is the story about? (A memory, inside joke, or random idea):",
    value=(
        "We went out looking for the best food in town, got lost, and ended"
        " up saving the city."
    ),
    height=100,
)

def generate_offline_story(name, style, prompt):
  openings = {
      "Comedy Adventure": (
          f"It started as a completely normal afternoon for {name}, until"
          " things went hilariously off-script."
      ),
      "Dark Fantasy Quest": (
          f"Beneath a shadowed sky, {name} stood at the edge of the realm,"
          " holding the only map that mattered."
      ),
      "Romantic Sci-Fi": (
          f"Across the neon skyline of Neo-Nairobi, {name} locked in the"
          " coordinates for one unforgettable night."
      ),
      "Action Heist": (
          f"With five minutes on the clock and zero backup, {name} adjusted"
          " the plan and smirked."
      ),
  }

  story = (
      f"{openings[style]}\n\n"
      f"The mission was simple: {prompt.strip()}\n\n"
      f"Naturally, chaos showed up right on schedule. Instead of panicking,"
      f" {name} turned a near-disaster into an iconic win—proving once again"
      " why we make the ultimate duo. By the time the dust settled, there"
      " was only one thing left to do: celebrate like legends."
  )

  image_prompts = (
      f"1. [Panel 1]: Cinematic {style.lower()} illustration of {name}"
      f" starting an adventure, {prompt.strip()}, expressive lighting,"
      " digital art.\n"
      f"2. [Panel 2]: Dramatic close-up of {name} laughing through"
      " unexpected chaos, dynamic comic book style, vibrant colors.\n"
      f"3. [Panel 3]: Triumph scene at sunset, {name} celebrating victory,"
      " detailed background, warm cinematic glow."
  )
  return story, image_prompts

def generate_gemini_story(key, name, style, prompt):
  client = genai.Client(api_key=key)
  full_prompt = (
      f"Write a short, entertaining 3-paragraph {style} story starring"
      f" {name} based on this idea: '{prompt}'. Keep it fun, engaging, and"
      " personal. After the story, add a section labeled 'IMAGE PROMPTS:'"
      " with 3 short comic-panel image prompts I can paste into an AI image"
      " generator."
  )
  response = client.models.generate_content(
      model="gemini-2.5-flash", contents=full_prompt
  )
  text = response.text or ""
  if "IMAGE PROMPTS:" in text:
    parts = text.split("IMAGE PROMPTS:", 1)
    return parts[0].strip(), parts[1].strip()
  return text.strip(), (
      f"Cinematic {style} scene featuring {name}: {prompt}, digital comic"
      " art style."
  )

if st.button("✨ Generate Story & AI Prompts", type="primary"):
  with st.spinner("Crafting your story..."):
    try:
      if api_key.strip():
        story_out, img_out = generate_gemini_story(
            api_key.strip(), hero_name, genre, story_seed
        )
      else:
        story_out, img_out = generate_offline_story(
            hero_name, genre, story_seed
        )

      st.subheader("📜 Your Generated Story")
      st.info("Tap the copy icon in the top-right corner of the box below!")
      st.code(story_out, language=None)

      st.subheader("🎨 AI Comic Image Prompts")
      st.caption(
          "Copy these into any free AI image tool to illustrate the story:"
      )
      st.code(img_out, language=None)

    except Exception as e:
      st.error(f"API error: {e}")
      st.info(
          "Tip: Clear the API key box in the sidebar to use the built-in"
          " generator!"
      )
