import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    #code for the transition model function
    dstrbprob = {}
    pttialpages = corpus[page]
    if len(pttialpages) <= 0:
        pb = 1 / len(corpus)
        for cpspage in corpus:
            dstrbprob[cpspage] = pb
        return dstrbprob
    dmpgprob = damping_factor / len(pttialpages)
    dmpgprobrdm = (1 - damping_factor) / len(corpus)
    for potpage in pttialpages:
        dstrbprob[potpage] = dmpgprob
    for corpus_page in corpus:
        if corpus_page in pttialpages:
            dstrbprob[corpus_page] += dmpgprobrdm
        else:
            dstrbprob[corpus_page] = dmpgprobrdm
    return dstrbprob


def sample_pagerank(corpus, damping_factor, n):
    #code for the sample_pagerank function
    nxtpg = random.choice(list(corpus))
    pgrnk = {}
    for i in range(n - 1):
        nxtpg = random.choices(list(transition_model(corpus, nxtpg, damping_factor)), weights=transition_model(corpus, nxtpg, damping_factor).values(), k=1).pop()
        if nxtpg in pgrnk:
            pgrnk[nxtpg] += 1
        else:
            pgrnk[nxtpg] = 1
    for pg in pgrnk:
        pgrnk[pg] = pgrnk[pg] / n

    return pgrnk


def iterate_pagerank(corpus, damping_factor):
    pgrk = {}
    pgrk={pg : 1/len(corpus) for pg in corpus}
    cv = False
    while not cv:
        pgrcp = {a: b for a, b in pgrk.items()}
        pgrdif = {}
        for page in corpus.keys():
            pb = 0
            for pI, pgs in corpus.items():
                if page in pgs:
                    pb+=pgrcp[pI]/len(pgs)
                elif len(pgs)==0:
                    pb+=1/len(corpus)
            valuen1=1-damping_factor
            valuen2=damping_factor*pb
            pgrk[page]=(valuen1)/len(corpus)+(valuen2)
            percent=pgrcp[page]-pgrk[page]
            pgrdif[page] = abs(percent)
        cv = True
        for pg in pgrdif:
            if pgrdif[pg] > 0.001: #it is still not it
                cv = False
        #if cv is still True the while loop ends 
    smpgrk = 0
    for elt in pgrk:
        smpgrk += pgrk[elt]
    for eltbis in pgrk:
        pgrk[eltbis]=pgrk[eltbis]/smpgrk
    return pgrk
if __name__ == "__main__":
    main()
