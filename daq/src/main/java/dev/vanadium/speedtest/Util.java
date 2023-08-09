package dev.vanadium.speedtest;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Util {

    public static String timeNow() {
        DateTimeFormatter fmt = DateTimeFormatter.ofPattern("HH:mm");
        LocalDateTime now = LocalDateTime.now();
        return fmt.format(now);
    }

}
