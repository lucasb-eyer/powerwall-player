#!/usr/bin/env python

import pyglet

class PlayerWindow(pyglet.window.Window):
    def __init__(self, player):
        options = {
            'caption': "Lucas' powerwall player",
            'visible': False,
            'resizable': False,
        }
        super(PlayerWindow, self).__init__(**options)

        self.player = player
        self.player.push_handlers(self)

    def on_eos(self):
        self.recompute_sizes()
        print('ON EOS')

    def get_video_size(self):
        """ Returns the width and height the current video needs.

            This might differ from the video pixel w/h if a pixel is not square.
        """
        if not self.player.source or not self.player.source.video_format:
            return 0, 0

        f = self.player.source.video_format
        if f.sample_aspect > 1.:
            return f.width * f.sample_aspect, f.height
        elif f.sample_aspect < 1.:
            return f.width, f.height / f.sample_aspect
        else:
            return f.width, f.height

    def recompute_sizes(self):
        self.w, self.h = self.get_video_size()

    def on_close(self):
        self.player.pause()
        self.close()

    def on_draw(self):
        self.clear()

        if self.player.source and self.player.source.video_format:
            self.player.get_texture().blit(0,0,width=self.w,height=self.h)

def main(filenames):
    videos = [pyglet.media.load(filename) for filename in filenames]

    player = pyglet.media.Player()
    for video in videos:
        player.queue(video)

    window = PlayerWindow(player)
    window.recompute_sizes()
    window.set_visible(True)
    player.play()
    pyglet.app.run()

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('Usage: player.py <filename> [<filename> ...]')
        sys.exit(1)

    main(sys.argv)

