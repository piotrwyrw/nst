package dev.vanadium.nst;

public class Log {

    public static void log(String msg) {
        System.out.println("[" + Util.timeNow() +  "] " + msg);
    }

}
