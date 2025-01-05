#include <cs50.h>
#include <stdio.h>

/*
 - all concepts utilised within have been learnt
 - (ie: conditionals, loops, operators, boolean expressions)
 - arrays not used as not yet learnt, or certain libs/functions
 - operators like modulus, division learnt, and were key to this exercise
 */

int main(void)
{
    // (1) get the CC number
    long ccNumber;
    do
    {
        ccNumber = get_long("Number: ");
    }
    while(ccNumber < 1);

    // (2) get length of CC number vars
    int ccLength = 0;
    long ccNumberReduce = ccNumber;

    // (3) CC number checksum vars
    bool isAddSet = true; // digits to be added only, starts last number
    int addSetTotal = 0;
    int timesAddSetTotal = 0;

    // (final) to store 1st and 2nd CC number digits
    // need to assign value, but don't want to use 0 as it's a valid number
    int lastDigit = -1; // 1st CC number digit, as going right-to-left
    int secondLastDigit = -1; // 2nd CC number digit, as above

    // do while loop for (2) and (3)
    do
    {
        // printf("Find CC No. length: %li / %i \n", ccNumberReduce, ccLength);

        // (3) CC number checksum
        int currentDigit = ccNumberReduce % 10; // current digit of CC number
        // which set of number is digit for? addSet or TimesAddSet?
        if (isAddSet)
        {
            // addSet: digits 0-9, only gets added, starts at last number
            addSetTotal = addSetTotal + currentDigit;
            // printf("[isAddSet] %i %i \n", currentDigit, addSetTotal);

            // ready for next digit for TimesAddSet
            isAddSet = false;
        }
        else
        {
            // TimesAddSet: starts second last digit, *2, split digits, sum up
            int digitDoubled = currentDigit * 2;

            // split digitDoubled if now 10+
            if (digitDoubled > 9) {
                // add to total 1st digit: 1 (10-18) & the 2nd digit
                timesAddSetTotal = timesAddSetTotal + 1 + (digitDoubled % 10);
            }
            else
            {
                timesAddSetTotal = timesAddSetTotal + digitDoubled;
            }

            // printf("[isTimesAddSet] %i %i %i \n", currentDigit, digitDoubled, timesAddSetTotal);

            // ready for next digit for addSet
            isAddSet = true;
        }
        // for (final) CC type checks, store last & second last digits
        secondLastDigit = lastDigit;
        lastDigit = currentDigit;

        // (2) get length of CC number
        // reduces cc number by 1 digit as only take integers (ignore decimals)
        ccNumberReduce = ccNumberReduce / 10;
        ccLength++; // count the number of digits
    }
    // at integer 0, ie: (last digit) 4 / 10 = 0.4 = 0, we are done
    while(ccNumberReduce > 0);
    // printf("Find CC No. length: %i \n", ccLength);

    // (3) checksum number continuned: sum the set totals for final modulus
    int checksumSetsTotal = addSetTotal + timesAddSetTotal;
    // printf("Checksum total: %i, 1st 2 digits: %i%i \n", checksumSetsTotal, lastDigit, secondLastDigit);

    // (final) output type of CC or invalid
    if (checksumSetsTotal % 10 == 0)
    {
        // (3) if last digit in checksum total = 0 = passed = here; otherwise fail/exit (else)

        // (4) base on length & 1st 2 digits, work out which type of CC
        if (ccLength == 15 && lastDigit == 3 && (secondLastDigit == 4 || secondLastDigit == 7))
        {
            // AMEX
            printf("AMEX\n");
        }
        else if (lastDigit == 4 && (ccLength == 13 || ccLength == 16))
        {
            // Visa
            printf("VISA\n");
        }
        else if(ccLength == 16 && lastDigit == 5 && (secondLastDigit == 1 || secondLastDigit == 2 || secondLastDigit == 3 || secondLastDigit == 4 || secondLastDigit == 5))
        {
            // MasterCard
            printf("MASTERCARD\n");
        }
        else
        {
            // not any type of CC
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
