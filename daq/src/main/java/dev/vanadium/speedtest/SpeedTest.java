package dev.vanadium.speedtest;

import java.io.File;

public class SpeedTest {

    public static void main(String[] args) {
        if (Session.checkSessionLock()) {
            Log.log("The session is locked.");
            return;
        }

        if (args.length != 1) {
            Log.log("Expected two arguments: <filename>");
            return;
        }

        Session.sessionLock(true);

        File f = new File(args[0]);
        ResultsFile resf = new ResultsFile();
        if (!f.exists())
            resf.write(f);

        SpeedTestResult rslt = Testing.runTestRetry(2);

        resf.read(f);

        double lastPing; // Just for emergency situations

        if (resf.getResults().size() == 0)
            lastPing = 0.0;
        else lastPing = resf.getResults().get(resf.getResults().size() - 1).getPing();

        if (rslt == null) {
            Log.log("Encountered an error while executing the speed test. Assuming network is down, therefore 0 Mb/s in both directions.");
            resf.add(new SpeedTestResult(0.0, 0.0, lastPing, Util.timeNow()));
        } else {
            resf.add(rslt);
        }

        resf.write(f);

        Log.log("Results written to '" + args[0] + "'");

        Session.sessionLock(false);
    }

}
