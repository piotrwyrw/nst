package dev.vanadium.speedtest;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.time.Instant;

public class Session {

    public static final String SESSION_LOCK = "nst.lock";
    public static final int SESSION_LOCK_EXPIRATION = 60 * 2; // A session lock expires after 2 Minutes

    // Test for a session lock
    public static boolean checkSessionLock() {
        File sl = new File(SESSION_LOCK);

        if (!sl.exists())
            return false; // No session lock at all

        String s;

        try {
            s = Files.readString(sl.toPath());
        } catch (IOException e) {
            Log.log("Cannot read session lock. Removing ...");
            sessionLock(false);
            return false; // Session lock has been removed -> Nothing to worry about (at lest in theory)
        }

        long unix;

        try {
            unix = Long.parseLong(s);
        } catch (NumberFormatException e) {
            Log.log("Cannot parse session lock time stamp. Removing ...");
            sessionLock(false);
            return false; // Session lock has been removed -> Nothing to worry about (at lest in theory)
            // Same as above
        }

        if (Instant.now().getEpochSecond() - unix < SESSION_LOCK_EXPIRATION) {
            Log.log("A valid session lock is still present.");
            return true;
        }

        Log.log("A session lock is present, but it had already expired. Therefore, it will be removed.");
        sessionLock(false);
        return false;

    }

    // Create or remove a session lock
    public static boolean sessionLock(boolean locked) {
        File sl = new File(SESSION_LOCK);

        // Remove the session lock
        if (!locked) {
            if (sl.exists())
                sl.delete();
            return true;
        }

        // Create a session lock
        try {
            Files.write(sl.toPath(), String.valueOf(Instant.now().getEpochSecond()).getBytes());
        } catch (IOException e) {
            Log.log("Failed to create a session lock. Aborting.");
            return false;
        }

        return true;
    }

}
