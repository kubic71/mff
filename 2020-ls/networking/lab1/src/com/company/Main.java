package com.company;

import java.net.NetworkInterface;
import java.net.SocketException;
import java.util.Enumeration;

public class Main {

    private static String hwaddrToString(byte[] bytes) {
        StringBuilder s = new StringBuilder();
        for (byte b : bytes) {
            s.append(String.format("%02X:", b));
        }
        return s.toString().substring(0, s.length()-1);
    }

    public static void main(String[] args) throws SocketException {

        Enumeration<NetworkInterface> interfaces = NetworkInterface.getNetworkInterfaces();

        // iterate over network interfaces
        while (interfaces.hasMoreElements())
        {
            NetworkInterface networkInterface = interfaces.nextElement();
            byte[] hwaddr = networkInterface.getHardwareAddress();
            String mac;
            String global_local;

            if(hwaddr != null) {
                 mac = hwaddrToString(networkInterface.getHardwareAddress());

                 // if 7-th bit is set, hwaddr is locally administered
                if((hwaddr[0] & 0b00000010) != 0) {
                    global_local = "local";
                } else {
                    global_local = "global";
                }
            } else {
                // loopback interface doesn't have hardware addr
                mac = "null";
                global_local = "null";
            }

            // format the info and output it to the console
            System.out.println(networkInterface.getDisplayName() + ": " + mac + " - " + global_local + " - " + (networkInterface.isUp() ? "(up)." : "(down)."));
        }
    }
}
