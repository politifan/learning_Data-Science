from progress.bar import IncrementalBar
from time import sleep
from sys import stderr


class DownloadBar(IncrementalBar):
    failed = 0

    suffix = (
        "%(index)d/%(max)d | "
        "%(percent).1f%% | "
        "%(speed).2f it/s | "
        "Failed: %(failed)d | "
        "Elapsed: %(elapsed_td)s | "
        "ETA: %(eta_td)s"
    )
    fill = "█"
    empty_fill = "░"
    width = 40
    color = "green"
    
    @property
    def speed(self):
        return 1 / self.avg if self.avg > 0 else 0

# USAGE
# with DownloadBar("Downloading", max=20, file=stderr) as bar:
#     for _ in range(20):
#         sleep(0.3)
#         bar.next()
#         bar.file.flush()