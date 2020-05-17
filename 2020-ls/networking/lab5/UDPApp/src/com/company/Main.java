package com.company;

import java.io.IOException;

public class Main {
    public  static void printUsage() {
        System.out.println("Usage:\nClient mode: java ClientUDP IP PORT");
        System.out.println("Server mode: java ServerUDP PORT");
    }

    public static void main(String[] args) throws IOException {

        // need to init ip and port to make compiler happy
        String ip="";
        int port=0;
        if(args[0].equals("ClientUDP")) {
            try {
               ip = args[1];
               port = Integer.parseInt(args[2]);
            } catch (Exception e) {
                printUsage();
                System.exit(1);
            }

            BasicClientUDP client = new BasicClientUDP(ip, port);
            client.start();


        } else if (args[0].equals("ServerUDP")) {
            try {
                port = Integer.parseInt(args[1]);
            } catch (Exception e) {
                printUsage();
                System.exit(1);
            }

            BasicServerUDP server = new BasicServerUDP(port);
            server.start();

        } else {
            printUsage();
        }
    }
}
