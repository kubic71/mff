package com.company;

class Ambulance extends Thread {
	private int capacity;
	private Bus b;

	Ambulance(Bus b, int cap) {
		this.capacity = cap;
		this.b = b;
		setDaemon(true);
	}

	@Override
	public void run() {
		while (true) {
			b.performTrip(capacity);
			System.out.println("Performing trip...");
			b.waitDisinfection();
			System.out.println("Ready to take patients.");
		}
	}
}
