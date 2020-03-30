#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "MemoryManager.h"

int MEM_SIZE = 100; 

void Show (T_handler handler) {
	printf("Dummy show\n");
}

// free space blocks are represented by right half-open intervals, for example:
// 
// block:
//  start = 0
//  end = 10
// 
// this means memory block is of size 10, from byte 0 to byte 9 


void Create(T_handler* handler_ptr) {
    (*handler_ptr) = malloc(sizeof(T_Node));

    // linked-list initialization
    (*handler_ptr)->start = 0;
    (*handler_ptr)->end = MEM_SIZE;
    (*handler_ptr)->next = NULL;
}

// Frees the required structure
void Destroy(T_handler* handler_ptr) {
    // TODO
}

/* Returns in "ad" the memory address where the required block of memory with length "size" starts.
 * If this operation finishes successfully then "ok" holds a TRUE value; FALSE otherwise.
 */
void Allocate(T_handler* handler, unsigned size, unsigned* ad, unsigned* ok) {
    T_Node* list_ptr = (*handler);

    // find free space
    while(true) {
        // reached the end of the linked list
        if(list_ptr == NULL) {
            *ok = false;
            return;
        }

        unsigned free_space = list_ptr->end - list_ptr->start;
        if(free_space >= size) {
            list_ptr->start += size;
            *ok = true;
        }
    }
}


    
static void Collapse(T_Node)

/* Frees a block of memory with length "size" which starts at "ad" address.
 * If needed, can be assumed to be a previous allocated block
 */
void Deallocate(T_handler* handler, unsigned size ,unsigned ad);


