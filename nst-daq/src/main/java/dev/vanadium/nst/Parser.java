package dev.vanadium.nst;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Parser {

    public static final Pattern DOWNLOAD_PATTERN = Pattern.compile("Download:\\s+([0-9]+\\.[0-9]+)");
    public static final Pattern UPLOAD_PATTERN = Pattern.compile("Upload:\\s+([0-9]+\\.[0-9]+)");
    public static final Pattern PING_PATTERN = Pattern.compile("Ping:\\s+([0-9]+\\.[0-9]+)");

    public static String matchAgainst(String what, final Pattern to) {
        Matcher matcher = to.matcher(what);
        if (!matcher.find())
            return null;
        return matcher.group(1);
    }

    public static SpeedTestResult parse(String input) {
        String up = matchAgainst(input, DOWNLOAD_PATTERN);
        String down = matchAgainst(input, UPLOAD_PATTERN);
        String ping = matchAgainst(input, PING_PATTERN);

        double dUp = Double.parseDouble(up);
        double dDown = Double.parseDouble(down);
        double dPing = Double.parseDouble(ping);

        return new SpeedTestResult(dUp, dDown, dPing, Util.timeNow());
    }

}
