import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def joint_probability(people, one_gene, two_genes, have_trait):
    #sorry !

    prbl = 1
    zero_gene = people.keys() - (one_gene | two_genes)

    for prsn in zero_gene:
        if people[prsn]["mother"] is None:
            prbl *= PROBS["gene"][0]
        
        elif people[prsn]["mother"] is not None:
            mama = people[prsn]["mother"]
            papino = people[prsn]["father"]

            if mama in one_gene and papino in two_genes:
                prbl *= 0.5 * PROBS["mutation"]

            if mama in two_genes and papino in zero_gene:
                prbl *= PROBS["mutation"] * (1 - PROBS["mutation"])
            
            if mama in two_genes and papino in one_gene:
                prbl *= PROBS["mutation"] * 0.5
            
            if mama in two_genes and papino in two_genes:
                prbl *= PROBS["mutation"] ** 2

            if mama in zero_gene and papino in zero_gene:
                prbl *= (1 - PROBS["mutation"]) ** 2
            
            if mama in zero_gene and papino in one_gene:
                prbl *= (1 - PROBS["mutation"]) * 0.5
            
            if mama in zero_gene and papino in two_genes:
                prbl *= (1 - PROBS["mutation"]) * PROBS["mutation"]

            if mama in one_gene and papino in zero_gene:
                prbl *= 0.5 * (1 - PROBS["mutation"])
            
            if mama in one_gene and papino in one_gene:
                prbl *= 0.5 ** 2
            

        prbl *= PROBS["trait"][0][prsn in have_trait]
    
    for prsn in two_genes:
        
        if people[prsn]["mother"] is None:
            prbl *= PROBS["gene"][2]
        
        elif people[prsn]["mother"] is not None:
            mama = people[prsn]["mother"]
            papino = people[prsn]["father"]

            if mama in zero_gene and papino in two_genes:
                prbl *= PROBS["mutation"] * (1 - PROBS["mutation"])

            if mama in one_gene and papino in zero_gene:
                prbl *= 0.5 * PROBS["mutation"]
        
            if mama in one_gene and papino in one_gene:
                prbl *= 0.5 * 0.5
        
            if mama in one_gene and papino in two_genes:
                prbl *= 0.5 * (1 - PROBS["mutation"])

            if mama in zero_gene and papino in zero_gene:
                prbl *= PROBS["mutation"] ** 2
        
            if mama in zero_gene and papino in one_gene:
                prbl *= PROBS["mutation"] * 0.5

        
            if mama in two_genes and papino in zero_gene:
                prbl *= (1 - PROBS["mutation"]) * PROBS["mutation"]
        
            if mama in two_genes and papino in one_gene:
                prbl *= (1 - PROBS["mutation"]) * 0.5
        
            if mama in two_genes and papino in two_genes:
        
                prbl *= (1 - PROBS["mutation"]) ** 2

        prbl *= PROBS["trait"][2][prsn in have_trait]

    for prsn in one_gene:
        if people[prsn]["mother"] is None:
            prbl *= PROBS["gene"][1]
        
        elif people[prsn]["mother"] is not None:
            mama = people[prsn]["mother"]
            papino = people[prsn]["father"]

            if mama in zero_gene and papino in zero_gene:
                prbl *= (1 - PROBS["mutation"]) ** 2 + PROBS["mutation"] ** 2
        
            if mama in zero_gene and papino in one_gene:
                prbl *= (1 - PROBS["mutation"]) * 0.5 + PROBS["mutation"] * 0.5
        
            if mama in zero_gene and papino in two_genes:
                prbl *= (1 - PROBS["mutation"]) * PROBS["mutation"] + (1 - PROBS["mutation"]) * PROBS["mutation"]


        
            if mama in two_genes and papino in one_gene:
                prbl *= (1 - PROBS["mutation"]) * 0.5 + PROBS["mutation"] * 0.5
        
            if mama in two_genes and papino in two_genes:
                prbl *= (1 - PROBS["mutation"]) ** 2 + PROBS["mutation"] ** 2
            
            if mama in two_genes and papino in zero_gene:
                prbl *= (1 - PROBS["mutation"]) ** 2 + PROBS["mutation"] ** 2

            if mama in one_gene and papino in zero_gene:
                prbl *= 0.5 * (1 - PROBS["mutation"]) + 0.5 * PROBS["mutation"]
        
            if mama in one_gene and papino in one_gene:
                prbl *= 0.5 ** 2 + 0.5 ** 2
        
            if mama in one_gene and papino in two_genes:
                prbl *= 0.5 * (1 - PROBS["mutation"]) + 0.5 * PROBS["mutation"]
        
            

        prbl *= PROBS["trait"][1][prsn in have_trait]

    


    return prbl

def update(probabilities, one_gene, two_genes, have_trait, p):

    for prsn in probabilities:
        if prsn in one_gene:
            probabilities[prsn]["gene"][1] += p

        elif prsn in two_genes:
            probabilities[prsn]["gene"][2] += p

        else:
            probabilities[prsn]["gene"][0] += p

        probabilities[prsn]["trait"][prsn in have_trait] += p



def normalize(probabilities):

    for prsn in probabilities:
        gns = sum(probabilities[prsn]["gene"].values())

        for vl in range(0, 3):
            probabilities[prsn]["gene"][vl]/= gns

        trts = sum(probabilities[prsn]["trait"].values())

        for vl in range(0, 2):
            probabilities[prsn]["trait"][vl]/= trts


if __name__ == "__main__":
    main()
