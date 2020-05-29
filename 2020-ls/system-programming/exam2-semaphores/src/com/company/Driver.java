package com.company;

/*
 * Name: Jakub
 * Surname: Hejhal
 */
public class Driver {
	public static final int NUM_PASSENGERS = 50;
	public static final int NUM_CRITICAL = 6;
	public static final int NUM_MINOR = 30;
	public static final int NUM_UNHARMED = 14;
	public static final int CAPACITY = 5;

	public static void main(String[] args) {
		BusSemaphores b = new BusSemaphores();
		Ambulance a = new Ambulance(b, CAPACITY);
		Passenger[] p = new Passenger[NUM_PASSENGERS];
		int i = 0;
		for (int j = 0; j < NUM_CRITICAL; j++, i++)
			p[i] = new Passenger(b, PassengerType.CRITICAL, j);
		for (int j = 0; j < NUM_MINOR; j++, i++)
			p[i] = new Passenger(b, PassengerType.MINOR, j);
		for (int j = 0; j < NUM_UNHARMED; j++, i++)
			p[i] = new Passenger(b, PassengerType.UNHARMED, j);
		a.start();
		for (int j = 0; j < NUM_PASSENGERS; j++, i++)
			p[j].start();
	}
}
