import csv
import itertools

PROBS = {
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        2: {True: 0.65, False: 0.35},
        1: {True: 0.56, False: 0.44},
        0: {True: 0.01, False: 0.99},
    },
    "mutation": 0.01,
}

def load_data(filename):
    with open(filename) as f:
        reader = csv.DictReader(f)
        return {
            row["name"]: {
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": None if row["trait"] == "" else row["trait"] == "1",
            }
            for row in reader
        }

def powerset(s):
    return [set(combo) for r in range(len(s) + 1) for combo in itertools.combinations(s, r)]

def joint_probability(people, one_gene, two_genes, have_trait):
    prob = 1
    
    for person in people:
        mother, father = people[person]["mother"], people[person]["father"]
        gene_count = (2 if person in two_genes else 1 if person in one_gene else 0)
        
        if mother and father:
            def get_prob(parent):
                return PROBS["mutation"] if parent in one_gene else (1 - PROBS["mutation"] if parent in two_genes else 0.5)
            prob *= (get_prob(mother) * get_prob(father) if gene_count == 2 else
                     (get_prob(mother) * (1 - get_prob(father)) + get_prob(father) * (1 - get_prob(mother))) if gene_count == 1 else
                     (1 - get_prob(mother)) * (1 - get_prob(father)))
        else:
            prob *= PROBS["gene"][gene_count]
        
        prob *= PROBS["trait"][gene_count][person in have_trait]
    
    return prob

def update(probabilities, one_gene, two_genes, have_trait, p):
    for person in probabilities:
        gene_count = 2 if person in two_genes else 1 if person in one_gene else 0
        probabilities[person]["gene"][gene_count] += p
        probabilities[person]["trait"][person in have_trait] += p

def normalize(probabilities):
    for person in probabilities:
        for key in ["gene", "trait"]:
            total = sum(probabilities[person][key].values())
            for value in probabilities[person][key]:
                probabilities[person][key][value] /= total

def main():
    people = load_data("data/family0.csv")
    probabilities = {person: {"gene": {0: 0, 1: 0, 2: 0}, "trait": {True: 0, False: 0}} for person in people}
    
    for have_trait in powerset(people):
        if any(people[p]["trait"] is not None and people[p]["trait"] != (p in have_trait) for p in people):
            continue
        for one_gene in powerset(people):
            for two_genes in powerset(people - one_gene):
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)
    
    normalize(probabilities)
    for person in probabilities:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}: {', '.join(f'{v}: {probabilities[person][field][v]:.4f}' for v in probabilities[person][field])}")

if __name__ == "__main__":
    main()
