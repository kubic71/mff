package com.company;

import javax.xml.crypto.Data;
import java.io.IOException;
import java.net.*;

public class Util {

    public static String bufferToString(byte[] a) {
        if (a == null)
            return null;
        StringBuilder ret = new StringBuilder();
        int i = 0;

        while (i < a.length && a[i] != 0) {
            ret.append((char) a[i]);
            i++;
        }
        return ret.toString();
    }
}

