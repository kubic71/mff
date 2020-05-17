package com.company;

import java.io.*;
import java.net.*;
import java.util.*;


import static com.company.Util.bufferToString;

public class BasicServerUDP {
    InetAddress clientIp;
    int clientPort;

    // 20 seems to be very low
    static final int BUFFER_LEN = 20;


    DatagramSocket server;
    int serverPort;

    public BasicServerUDP(int serverPort) {
        this.serverPort = serverPort;


    }

    private void respond(String msg) throws IOException {
        // send response to the last client from whom datagram was received
        byte[] buf = msg.getBytes();
        DatagramPacket packet = new DatagramPacket(buf, buf.length);
        packet.setAddress(clientIp);
        packet.setPort(clientPort);
        server.send(packet);
    }

    public void start() throws IOException {
        System.out.println("Starting server at 0.0.0.0:" + Integer.toString(serverPort));


        try {
            server = new DatagramSocket(null);

            // allow multiple instances of server running on the same port
            server.setOption(StandardSocketOptions.SO_REUSEPORT, Boolean.TRUE);
            server.bind(new InetSocketAddress("0.0.0.0", serverPort));
        } catch (IOException e) {
            System.out.println("Cannot bind to 0.0.0.0.:" + Integer.toString(serverPort));
            return;
        }

        byte[] receive = new byte[BUFFER_LEN];
        DatagramPacket packet = null;
        while (true) {
            System.out.println("Waiting for client datagram...");
            packet = new DatagramPacket(receive, receive.length);

            server.receive(packet);

            clientIp = packet.getAddress();
            clientPort = packet.getPort();
            System.out.println("Incoming data from " + clientIp.toString() + ":" + Integer.toString(clientPort));
            String recvStr = bufferToString(receive);
            System.out.println("Received data:");
            System.out.println(recvStr);

            String[] lines = recvStr.split("\r\n");

            if (lines.length != 2) {
                System.out.println("Invalid message format!");
                respond("Invalid message format!");
                continue;
            }

            String command = lines[0];
            String content = lines[1];


            if (command.equals("L")) {
                System.out.println("Serving L command");
                respond(removeExtraWhiteCharacters(content));
            } else if (command.equals("B")) {

                System.out.println("Serving B command");
                content = removeExtraWhiteCharacters(content);

                // shuffle the words
                String[] words = content.split(" ");
                List<String> wordsList = Arrays.asList(words);
                Collections.shuffle(wordsList);
                respond(String.join(" ", wordsList));

            } else {
                System.out.println("Not supported option");
                respond("Not supported option");
            }

            // Clear the buffer after every message.
            receive = new byte[BUFFER_LEN];
        }
    }


    private String removeExtraWhiteCharacters(String content) {
        content = content.replaceAll("\\s+", " ");
        return content.strip();
    }

}

