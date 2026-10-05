import glob
import os
import os.path
import shutil
import subprocess
import sys

from gtts import gTTS
import yt_dlp

# yt-dlp needs a JavaScript runtime (deno, installed in the venv) to decode YouTube streams
os.environ["PATH"] = os.path.dirname(sys.executable) + os.pathsep + os.environ.get("PATH", "")


class Audio(object):
    def __init__(self):
        """audio functions (output, volume etc)"""
        self.volume = 50

    def get_sink_indexes(self) -> list:
        indexes = []
        for line in self.get_info().split("\n"):
            if line:
                indexes.append(line.split()[0])
        return indexes

    def get_info(self) -> str:
        p = subprocess.run(
            ['pactl', 'list', 'short', 'sinks'], capture_output=True)
        return p.stdout.decode('utf-8')

    def set_output(self, index: int) -> str:
        p = subprocess.run(['pactl', 'set-default-sink', str(index)])
        if p.returncode == 0:
            return f"sink {index} has been set"
        else:
            return f"sink {index} does not exist"

    def volume_set(self, volume_pct: int) -> int:
        volume_pct = max(min(volume_pct, 100), 0)
        for index in self.get_sink_indexes():
            _ = subprocess.run(['pactl', 'set-sink-volume',
                               str(index), f"{volume_pct}%"])
        return volume_pct


class MediaPlayer(object):
    record_dir = "data/MediaPlayer/record"
    speak_dir = "data/MediaPlayer/speak"
    subprocess.run(["mkdir", "-p", record_dir])
    subprocess.run(["mkdir", "-p", speak_dir])

    def play(self, url: str, stop_before_play: bool = True):
        if stop_before_play:
            self.stop()
        path = f"{self.record_dir}/{url}.wav"
        if os.path.exists(path):
            url = path
        elif url.startswith(("http://", "https://")):
            url = self.get_audio_stream_url(url)
        if shutil.which("cvlc"):
            cmd = ["cvlc", "--quiet", "--no-loop", "--play-and-exit", "--no-video"]
        else:
            cmd = ["mpv", "--really-quiet", "--no-video", "--ytdl=no"]
        subprocess.Popen(cmd + [url])

    @staticmethod
    def get_audio_stream_url(url: str) -> str:
        """resolve a web page (youtube etc) to a direct audio stream url,
        players' own youtube support is slow or broken"""
        opts = {"format": "bestaudio/best", "quiet": True, "no_warnings": True,
                "noplaylist": True}
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                return ydl.extract_info(url, download=False)["url"]
        except yt_dlp.utils.DownloadError:
            # not a supported site: let the player try the url as is
            return url

    def record(self, file_name: str):
        cmd = f"arecord -D hw:2,0 -f S16_LE -r44100 -t wav -d 5"
        print(cmd.split() + [f"{self.record_dir}/{file_name}.wav"])
        subprocess.Popen(cmd.split() + [f"{self.record_dir}/{file_name}.wav"])

    def list_records(self) -> list[str]:
        r = []
        for path in glob.glob(f"{self.record_dir}/*.wav"):
            filename = path.split('/')[-1]
            r.append(filename.removesuffix('.wav'))
        return r

    def stop(self):
        subprocess.run(['pkill', 'vlc'])
        subprocess.run(['pkill', '-f', 'mpv --really-quiet'])

    def speak(self, text: str, language: str = 'en'):
        file_name = f"{self.speak_dir}/speak.mp3"
        myobj = gTTS(text=text, lang=language, slow=False)
        myobj.save(file_name)
        self.play(file_name, stop_before_play=False)
