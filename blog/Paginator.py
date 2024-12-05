class Pagination:
    def __init__(self, posts, per_page):
        self.lst = posts
        self.per_page = per_page
        self.resultbek = self.paginator()
        self.pager = len(self.resultbek)


    def paginator(self):
        nimadir = []
        for i in range(0,len(self.lst),self.per_page):
            qanaqadir = []
            for j in range(i, i + self.per_page):
                if j >= len(self.lst):
                    break
                qanaqadir.append(self.lst[j])
            nimadir.append(qanaqadir)
        return nimadir

    def get_page(self, page_numba):
        if page_numba >= self.pager:
            return self.resultbek[-1]
        if page_numba <= 1:
            return self.resultbek[0]
        return self.resultbek[page_numba - 1]

    def the_first(self, page_numba):
        if page_numba == 1:
            return True
        return False
    def the_last(self, page_numba):
        if page_numba == self.pager:
            return True
        return False

