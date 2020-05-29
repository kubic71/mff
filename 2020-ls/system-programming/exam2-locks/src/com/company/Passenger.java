package com.company;

/*
 * Name: Jakub
 * Surname: Hejhal
 */
class Passenger extends Thread {
	private PassengerType type;
	private int id;
	private Bus b;

	Passenger(Bus b, PassengerType pasType, int id) {
		this.type = pasType;
		this.id = id;
		this.b = b;
	}

	@Override
	public void run() {
		b.waitDisinfection();
		b.onBoardAmbulance(this.type, id);
	}
}
