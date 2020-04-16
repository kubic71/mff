/*
 * List.h
 *
 *  Created on: 5 abr. 2020
 *      Author: galvez
 */

#ifndef LIST_H_
#define LIST_H_


typedef struct _Data {
	double value;
	struct _Data * next;
} T_Data;

typedef T_Data * T_List;

void create(T_List * list);
void insert(T_List * list, double value);
void destroy(T_List * list);

#endif /* LIST_H_ */
