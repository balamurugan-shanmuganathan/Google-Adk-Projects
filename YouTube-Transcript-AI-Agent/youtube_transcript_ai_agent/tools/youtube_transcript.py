
from langchain_community.document_loaders import YoutubeLoader

def get_youtube_transcript(url:str) -> str:
    """ Get the transcript of the youtube video by using url"""
    loader = YoutubeLoader.from_youtube_url(url)
    transcript = loader.load()
    return {"youtube_transcript" : transcript}