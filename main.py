import re
import argparse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk

# Download stopwords if not already downloaded - Requires internet connection the first time
nltk.download('stopwords')

# Load WhatsApp conversation
def load_chat(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        chat_data = file.read()
    return chat_data

# remove messages not from the specified user, timestamps etc.
def scrub_chat_messages(chat_data, user:str=None):
    messages = chat_data.split('\n')
    TIMESTAMP_PATTERN = r'\d{1,2}/\d{1,2}/\d{4}, \d{1,2}:\d{2}'
    MESSAGE_PATTERN = r'- ([\w\s]+): (.+)'

    user_messages = []
    messages = re.split(TIMESTAMP_PATTERN, chat_data)

    for message in messages:
        # Messages like <This message has been edited> or <Media omitted> from whatsapp log are removed
        message = re.sub(r"<[\w\s]+>", "", message).strip()

        match = re.search(MESSAGE_PATTERN, message)
        if match:
            sender = match.group(1)
            message_text = match.group(2)

            if user is None:
                # If we don't care about which user, don't filter the message out
                user_messages.append(message_text)
            elif sender == user:
                # Keep only messages from the specified user
                user_messages.append(message_text)

    user_chat = ' '.join(user_messages)
    # Remove non-word characters (like punctuation, etc)
    user_chat = re.sub(r'[^\w\s]', '', user_chat)

    return user_chat


# Remove stopwords (like "the", "and", etc.)
def remove_stopwords(text:str, language:str):
    stop_words = set(stopwords.words(language))
    
    # Add extra words to take into account common "typos" of internet talk
    if language == 'portuguese':
        [stop_words.add(w) for w in [
            "eh", "pra", "q", "pq", "nao", "ta", "n", "tb", "vc","voce",
            "ai","aí","tbm","mt","vcs","pro","la","tao","ja"
        ]]
    elif language == 'english':
        [stop_words.add(w) for w in [
            'one','oh','im','ill','thats','well','dont','ive','cant',
            'need','think','theres','youre','hes','shes','its','didnt','got','bit',
            'theyre','wont','id','youve','youll','doesnt'
        ]]
    words = text.split()
    cleaned_text = ' '.join([word for word in words if word.lower() not in stop_words])
    return cleaned_text


# Generate and display the word cloud
def generate_wordcloud(cleaned_text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(cleaned_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()


def parse_args():
    parser = argparse.ArgumentParser(prog=__file__,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("file")
    parser.add_argument("--user", default=None, type=str)
    parser.add_argument("--language", default='english', type=str)

    return parser.parse_args()


def main(args):
    user = args.user
    file = args.file
    language=args.language

    chat_data = load_chat(file)
    cleaned_chat = scrub_chat_messages(chat_data, user)
    cleaned_chat_no_stopwords = remove_stopwords(cleaned_chat, language)
    generate_wordcloud(cleaned_chat_no_stopwords)



if __name__ == "__main__":
    args = parse_args()
    main(args)
