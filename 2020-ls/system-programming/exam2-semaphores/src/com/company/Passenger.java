package com.company;

/*
 * Name: Jakub
 * Surname: Hejhal
 */
class Passenger extends Thread {
	private PassengerType type;
	private int id;
	private BusSemaphores b;

	Passenger(BusSemaphores b, PassengerType pasType, int id) {
		this.type = pasType;
		this.id = id;
		this.b = b;
	}

	@Override
	public void run() {
		b.waitDisinfection();

		// I moved the info messages into onBoardAmbulance, and therefore have to pass passanger instance as param, so that I know it's id inside this method
		b.onBoardAmbulance(this.type, id);
	}
}
