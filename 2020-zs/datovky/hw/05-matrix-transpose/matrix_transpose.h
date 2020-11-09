/*
 *  This file is #include'd inside the definition of a matrix class
 *  like this:
 *
 *  	class ClassName {
 *          // Number of rows and columns of the matrix
 *          unsigned N;
 *
 *          // Swap elements (i1,j1) and (i2,j2)
 *          void swap(unsigned i1, unsigned j1, unsigned i2, unsigned j2);
 *
 *          // Your code
 *          #include "matrix_transpose.h"
 *      }
 */


// For linting purposes 
// unsigned N = 0;
// void swap(unsigned i1, unsigned j1, unsigned i2, unsigned j2);

void transpose_and_swap(unsigned i1, unsigned j1, unsigned i2, unsigned j2, unsigned w1, unsigned h1) {
    
    if(w1 == 0 || h1 == 0)
        return;
    if(w1 == 1 && h1 == 1) {
        swap(i1, j1, i2, j2);
        return;
    }

    unsigned w2 = h1;
    unsigned h2 = w1;
    
    // A_1,1 <-> B_1,1
    transpose_and_swap(i1       , j1       , i2       , j2       , w1/2     , h1/2     );

    // A_2,2 <-> B_2,2
    transpose_and_swap(i1 + h1/2, j1 + w1/2, i2 + h2/2, j2 + w2/2, w1 - w1/2, h1 - h1/2);

    // A_2,1 <-> B_1,2                                                                            
    transpose_and_swap(i1 + h1/2, j1       , i2       , j2 + w2/2, w1/2     , h1 - h1/2);

    // A_1,2 <-> B_2,1                                                                        
    transpose_and_swap(i1       , j1 + w1/2, i2 + h2/2, j2       , w1 - w1/2, h1/2     );

}


// transpose square submatrix starting at (i, j) with size n*n
void transpose(unsigned i, unsigned j, unsigned n) {
    if(n < 2)
        return;

    int s1 = n/2;
    int s2 = n - s1;

    transpose(i, j, s1);
    transpose(i + s1 , j + s1, s2);
    
    transpose_and_swap(i + s1, j, i, j + s1, s1, s2);
}

void transpose()
{
    transpose(0, 0, N);
}
