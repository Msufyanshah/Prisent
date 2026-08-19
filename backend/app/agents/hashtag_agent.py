# backend/app/agents/hashtag_agent.py
import re
from typing import List, Optional
from openai import OpenAI
from app.config import settings

def _to_camel_hashtag(phrase: str) -> str:
    """Converts a phrase like 'b2b saas' into '#B2BSaas'."""
    words = re.findall(r'[a-zA-Z0-9]+', phrase)
    if not words:
        return ""
    camel = "".join(word.capitalize() for word in words)
    camel = re.sub(r'([0-9])([a-z])', lambda m: m.group(1) + m.group(2).upper(), camel)
    return f"#{camel}"

async def run_hashtag_agent(post_content: str, niche: Optional[str] = None) -> List[str]:
    """
    Extracts 3-5 relevant LinkedIn hashtags directly from the post content.
    Extracts key topical concepts from the post text, normalizes them into CamelCase,
    and returns a list of 3 to 5 formatted hashtags.
    """
    if not post_content or not post_content.strip():
        return ["#LinkedIn", "#Professional", "#ContentStrategy"]

    try:
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        prompt = f"""
        Extract the 4-6 most important topical keywords or key concepts from the following LinkedIn post text.
        Scope to niche: {niche or 'General'}.

        Post text:
        \"\"\"{post_content}\"\"\"

        Output ONLY a JSON array of 4 to 6 short topical phrases (e.g. ["b2b saas", "vector databases", "ai ethics"]). No markdown, no extra text.
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a LinkedIn hashtag strategist. Output only a JSON array of topical phrases."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        content_text = response.choices[0].message.content.strip()
        
        import json
        clean_json = content_text.replace("```json", "").replace("```", "").strip()
        extracted_phrases = json.loads(clean_json)

        hashtags = []
        for phrase in extracted_phrases:
            tag = _to_camel_hashtag(str(phrase))
            if tag and tag not in hashtags:
                hashtags.append(tag)

        # Select 3-5 tags
        final_tags = hashtags[:5]
        if len(final_tags) < 3:
            default_tags = ["#ContentStrategy", "#Leadership", "#Innovation"]
            for dt in default_tags:
                if dt not in final_tags:
                    final_tags.append(dt)
                if len(final_tags) >= 3:
                    break
        return final_tags

    except Exception:
        # Robust fallback keyword extraction
        words = re.findall(r'\b[A-Za-z]{4,}\b', post_content)
        unique_words = list(dict.fromkeys(words))[:5]
        fallback_tags = [_to_camel_hashtag(w) for w in unique_words if len(w) >= 4]
        if len(fallback_tags) < 3:
            fallback_tags.extend(["#ContentStrategy", "#Leadership", "#Innovation"])
        return fallback_tags[:5]

def append_hashtags_to_post(post_content: str, hashtags: List[str]) -> str:
    """Appends hashtags at the end of post content if not already present."""
    if not hashtags:
        return post_content
    
    tags_string = " ".join(hashtags)
    if tags_string in post_content:
        return post_content

    return f"{post_content.rstrip()}\n\n{tags_string}"
