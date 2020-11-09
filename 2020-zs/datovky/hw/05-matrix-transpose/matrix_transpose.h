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

void transpose_and_swap(unsigned i1, unsigned j1, unsigned w1, unsigned h1, unsigned i2, unsigned j2, unsigned w2, unsigned h2) {
    
    if(w1 == 0 || h1 == 0)
        return;
    if(w1 == 1 && h1 == 1) {
        swap(i1, j1, i2, j2);
        return;
    }


    // A_1,1 <-> B_1,1
    transpose_and_swap(i1       , j1       , w1/2     , h1/2     , i2       , j2       , w2/2     , h2/2     );

    // A_2,2 <-> B_2,2
    transpose_and_swap(i1 + h1/2, j1 + w1/2, w1 - w1/2, h1 - h1/2, i2 + h2/2, j2 + w2/2, w2 - w2/2, h2 - h2/2);

    // A_2,1 <-> B_1,2
    transpose_and_swap(i1 + h1/2, j1       , w1/2     , h1 - h1/2, i2       , j2 + w2/2, w2 - w2/2, h2/2     );

    // A_1,2 <-> B_2,1
    transpose_and_swap(i1       , j1 + w1/2, w1 - w1/2, h1/2     , i2 + h2/2, j2       , w2/2     , h2 - h2/2);

}


// transpose square submatrix
void transpose(unsigned i, unsigned j, unsigned n) {
    if(n < 2)
        return;

    transpose(i, j, n/2);
    transpose(i + n/2 , j + n/2, n - n/2);
    
    transpose_and_swap(i + n/2, j, n/2, n - n/2, i, j + n/2, n - n/2, n/2);
}

void transpose()
{
    transpose(0, 0, N);

    // TODO: Implement this efficiently 

    // for (unsigned i=0; i<N; i++)
    //     for (unsigned j=0; j<i; j++)
    //         swap(i, j, j, i);
}
