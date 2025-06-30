import os
import re
import nltk
from glob import glob
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from transformers import pipeline

abstractive_summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
nltk.download('punkt_tab')
def load_and_clean(file_path):
    """Load a text file and clean up extra spaces."""
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    text = re.sub(r'\s+', ' ', text)
    return text

def split_text(text, max_chars=1000):
    """Split text into chunks based on sentence endings, with a maximum character count per chunk."""
    sentences = text.split('. ')
    chunks = []
    current_chunk = ''
    for sentence in sentences:
        sentence = sentence.strip() + '.'
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += sentence + ' '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ' '
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def extractive_summary(text, sentence_count=5):
    """Generate an extractive summary using LexRank."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary_sentences = summarizer(parser.document, sentence_count)
    summary = ' '.join(str(sentence) for sentence in summary_sentences)
    return summary

def abstractive_summary(text, max_length=200, min_length=100):
    """Generate an abstractive summary for a given text.
       For long texts, chunking is applied first.
    """
    if len(text) > 1000:
        chunks = split_text(text, max_chars=1000)
        chunk_summaries = []
        for chunk in chunks:
            summarized_chunk = abstractive_summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            chunk_summaries.append(summarized_chunk[0]['summary_text'])
        combined_text = ' '.join(chunk_summaries)
        final_summary = abstractive_summarizer(combined_text, max_length=max_length, min_length=min_length, do_sample=False)
        return final_summary[0]['summary_text']
    else:
        final_summary = abstractive_summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return final_summary[0]['summary_text']

def hybrid_summary(text):
    """Generate a hybrid summary by first applying extractive summarization,
       then refining with an abstractive summarizer.
    """
    extract_summary = extractive_summary(text, sentence_count=7)
    final_summary = abstractive_summary(extract_summary, max_length=150, min_length=75)
    return final_summary

def process_folder(input_folder, output_folder=None):
    """Process all .txt files in a folder and generate summaries."""
    print("hello")
    file_paths = glob(os.path.join(input_folder, '*.txt'))
    print(file_paths)
    summaries = {}
    
    for file_path in file_paths:
        print(file_path)
        text = load_and_clean(file_path)
        summary = hybrid_summary(text)
        file_name = os.path.basename(file_path)
        summaries[file_name] = summary
        print(f"Summary for {file_name}:\n{summary}\n{'-'*50}\n")
        
        if output_folder:
            os.makedirs(output_folder, exist_ok=True)
            summary_file = os.path.join(output_folder, f"summary_{file_name}")
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary)
    return summaries

input_folder = "intuitive_soul_posts"
output_folder = "summaries"  
process_folder(input_folder, output_folder)