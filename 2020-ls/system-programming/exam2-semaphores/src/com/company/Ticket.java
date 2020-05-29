package com.company;

/*
 * Name: Jakub
 * Surname: Hejhal
 */

import java.util.concurrent.Semaphore;

public class Ticket {
    public Semaphore waitForAmbulance = new Semaphore(0, true);
    public Semaphore ackAmbulance = new Semaphore(0, true);
    public volatile boolean placeFree = true;

}
