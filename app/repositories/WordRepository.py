from app.models.Word import Word
from app.repositories.BaseRepository import BaseRepository

class WordRepository(BaseRepository):
    def find_like(self, word):
        return self.class_.query.filter(Word.word.like(f'{word}%')).all()