import re

def remove_duplicate_sentences(text: str):
    # Split text into sentences using basic punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    seen = set()
    unique_sentences = []

    for sentence in sentences:
        normalized = sentence.strip()
        if normalized.lower() not in seen:
            seen.add(normalized.lower())  # Use lower() for case-insensitive deduplication
            unique_sentences.append(normalized)

    return ' '.join(unique_sentences)

# text = "Hello world. This is a test. Hello world. This is only a test."
# remove_duplicate_sentences(text)


def clean_vtt_file(input_path: str, output_path: str):

    with open(input_path, 'r', encoding='utf-8') as file:
        vtt_content = file.read()

    # Remove WEBVTT header, cue numbers, and timestamp lines
    vtt_content = re.sub(
        r'^(WEBVTT.*|(\d{2}:)?\d{2}:\d{2}\.\d{3} --> (\d{2}:)?\d{2}:\d{2}\.\d{3}.*|\d+\s*)$',
        '',
        vtt_content,
        flags=re.MULTILINE
    )

    # Remove HTML-like tags
    vtt_content = re.sub(r'<[^>]+>', '', vtt_content)

    # Clean up extra spaces and empty lines
    lines = [line.strip() for line in vtt_content.strip().splitlines() if line.strip()]

    # Remove duplicate lines (case-insensitive)
    seen = set()
    unique_lines = []

    for line in lines:
        normalized = line.lower()
        if normalized not in seen:
            seen.add(normalized)
            unique_lines.append(line)

    # Join and save the cleaned text
    cleaned_text = '\n'.join(unique_lines)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

# Example usage:
clean_vtt_file('file.vtt', 'output_cleaned.txt')
