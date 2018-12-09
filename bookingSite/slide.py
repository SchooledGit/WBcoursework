class Slide:
    source = ''
    index = 0
    text = ''
    caption = ''

    def __init__(self, src, indx, txt, cptn):
        self.source = src
        self.index = indx
        self.text = txt
        self.caption = cptn
