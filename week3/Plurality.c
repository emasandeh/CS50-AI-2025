#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX_CANDIDATES 9
#define MAX_VOTERS 100

// Candidates have a name and vote count
typedef struct
{
    char name[100];
    int votes;
} candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Number of candidates
int candidate_count = 0;

// Function prototypes
bool vote(char *name);
void print_winner(void);

int main(void)
{
    // Ask for the number of candidates
    printf("Enter number of candidates: ");
    scanf("%d", &candidate_count);

    // Ensure there are no more than MAX_CANDIDATES candidates
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Too many candidates.\n");
        return 1;
    }

    // Get candidate names
    for (int i = 0; i < candidate_count; i++)
    {
        printf("Enter candidate %d name: ", i + 1);
        scanf("%s", candidates[i].name);
        candidates[i].votes = 0; // Initialize vote count to zero
    }

    // Ask for the number of voters
    int voter_count;
    printf("Enter number of voters: ");
    scanf("%d", &voter_count);

    // Ensure there are no more than MAX_VOTERS voters
    if (voter_count > MAX_VOTERS)
    {
        printf("Too many voters.\n");
        return 1;
    }

    // Get votes from each voter
    for (int i = 0; i < voter_count; i++)
    {
        char vote_name[100];
        printf("Voter %d, enter your vote: ", i + 1);
        scanf("%s", vote_name);

        // Record the vote, ensuring it's a valid candidate
        if (!vote(vote_name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Print the winner(s)
    print_winner();
    return 0;
}

// This function records a vote for a candidate
bool vote(char *name)
{
    // Check if the candidate is on the ballot
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes++;  // Increment the vote count
            return true;
        }
    }
    return false;  // Invalid vote
}

// This function prints the winner(s) of the election
void print_winner(void)
{
    int max_votes = 0;

    // Find the maximum number of votes
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > max_votes)
        {
            max_votes = candidates[i].votes;
        }
    }

    // Print all candidates with the maximum number of votes
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes == max_votes)
        {
            printf("%s\n", candidates[i].name);
        }
    }
}
