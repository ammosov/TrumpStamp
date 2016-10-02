from kivy.core.audio import SoundLoader

class SoundManager(object):

    cache = dict()

    @staticmethod
    def play_audio(url):
        if url not in SoundManager.cache:
            SoundManager.cache[url] = SoundLoader.load(url)
        SoundManager.cache[url].play()
