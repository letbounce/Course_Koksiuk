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
    pages = dict()
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename] if link in pages
        )
    return pages

def transition_model(corpus, page, damping_factor):
    probability_distribution = {}
    links = corpus[page]
    num_pages = len(corpus)
    
    if links:
        for linked_page in links:
            probability_distribution[linked_page] = damping_factor / len(links)
        for p in corpus:
            probability_distribution[p] = probability_distribution.get(p, 0) + (1 - damping_factor) / num_pages
    else:
        for p in corpus:
            probability_distribution[p] = 1 / num_pages
    
    return probability_distribution

def sample_pagerank(corpus, damping_factor, n):
    page = random.choice(list(corpus.keys()))
    page_rank = {p: 0 for p in corpus}
    
    for _ in range(n):
        page_rank[page] += 1
        probabilities = transition_model(corpus, page, damping_factor)
        page = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]
    
    return {p: page_rank[p] / n for p in corpus}

def iterate_pagerank(corpus, damping_factor):
    num_pages = len(corpus)
    ranks = {p: 1 / num_pages for p in corpus}
    threshold = 0.001
    
    while True:
        new_ranks = {}
        for page in corpus:
            rank_sum = sum(ranks[p] / len(corpus[p]) for p in corpus if page in corpus[p])
            new_ranks[page] = (1 - damping_factor) / num_pages + damping_factor * rank_sum
        
        if all(abs(new_ranks[p] - ranks[p]) < threshold for p in corpus):
            break
        ranks = new_ranks
    
    return ranks

if __name__ == "__main__":
    main()